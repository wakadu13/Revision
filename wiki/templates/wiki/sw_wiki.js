{% load static %}// Service worker du wiki (portée : tout le site) : lecture hors ligne.
// - Les pages visitées, les images et les fichiers statiques sont gardés en cache
//   (réseau d'abord, cache ensuite) : sans connexion, une page déjà lue s'affiche.
// - « Garder ce dossier hors ligne » (sommaire) met en cache d'un coup les pages
//   et les PDF d'un dossier (hors_ligne_wiki.js, même cache).
// - Sans réseau ni cache, la page « hors connexion » liste ce qui est disponible.
// Les QCM hors ligne ont leur propre service worker sur /qcm/ (sw.js).
const CACHE = "wiki-hors-ligne-v1";
const HORS_CONNEXION = "{% url 'wiki:hors_connexion' %}";
const CDN = "https://cdn.jsdelivr.net/npm/";
const A_PRECHARGER = [
  HORS_CONNEXION,
  "{% url 'wiki:manifest_wiki' %}",
  "{% static 'wiki/wiki.css' %}",
  "{% static 'wiki/wiki.js' %}",
  "{% static 'wiki/plein_ecran.js' %}",
  "{% static 'wiki/palette.js' %}",
  "{% static 'wiki/tuteur.js' %}",
  "{% static 'wiki/hors_ligne_wiki.js' %}",
  "{% static 'wiki/rappel_web.js' %}",
  "{% static 'wiki/icone-192.png' %}",
  "{% static 'wiki/icone-512.png' %}",
  CDN + "katex@0.16.47/dist/katex.min.css",
  CDN + "katex@0.16.47/dist/katex.min.js",
  CDN + "@highlightjs/cdn-assets@11.12.0/styles/github.min.css",
  CDN + "@highlightjs/cdn-assets@11.12.0/styles/github-dark.min.css",
];
// Pages jamais mises en cache : édition, comptes, API, et le QCM (autre service worker).
const EXCLUS = [/^\/modifier\//, /^\/apercu\//, /^\/nouvelle\//, /^\/importer\//, /^\/transformations/, /^\/claude\//,
  /^\/historique\//, /^\/admin\//, /^\/connexion/, /^\/deconnexion/, /^\/compte/, /^\/utilisateurs/, /^\/inscription/,
  /^\/api\//, /^\/qcm\//, /^\/hors-ligne\//, /^\/palette\.json/, /^\/recherche\//, /^\/demander\//, /^\/copie\//];
const DELAI_RESEAU_MS = 5000;

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await Promise.all(A_PRECHARGER.map(async (url) => {
      try {
        const r = await fetch(url, { mode: url.startsWith("http") ? "cors" : "same-origin", credentials: "same-origin" });
        if (r.ok && !r.redirected) await cache.put(url, r);
      } catch (e) { /* hors ligne pendant l'installation */ }
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    for (const nom of await caches.keys()) {
      if (nom.startsWith("wiki-hors-ligne") && nom !== CACHE) await caches.delete(nom);
    }
    await self.clients.claim();
  })());
});

const exclu = (pathname) => EXCLUS.some((re) => re.test(pathname));

async function reseauPuisCache(request) {
  const cache = await caches.open(CACHE);
  try {
    const reponse = await Promise.race([
      fetch(request),
      new Promise((_, rej) => setTimeout(() => rej(new Error("délai dépassé")), DELAI_RESEAU_MS)),
    ]);
    // Une page de connexion (session expirée) ne remplace pas la page en cache.
    if (reponse.ok && !reponse.redirected && reponse.type !== "opaqueredirect") await cache.put(request, reponse.clone());
    return reponse;
  } catch (e) {
    const enCache = await cache.match(request);
    if (enCache) return enCache;
    throw e;
  }
}

async function navigation(request) {
  const url = new URL(request.url);
  if (exclu(url.pathname)) {
    try {
      return await fetch(request);
    } catch (e) {
      return (await caches.match(HORS_CONNEXION)) || Response.error();
    }
  }
  try {
    return await reseauPuisCache(request);
  } catch (e) {
    const page = await caches.match(HORS_CONNEXION);
    return page || Response.error();
  }
}

// Notifications web (rappel quotidien, commande envoyer_rappels) : affichées par le
// service worker ; un clic ouvre (ou ramène au premier plan) la page indiquée.
self.addEventListener("push", (event) => {
  let d = {};
  try { d = event.data ? event.data.json() : {}; } catch (e) { d = { texte: event.data ? event.data.text() : "" }; }
  event.waitUntil(self.registration.showNotification(d.titre || "ProjetPluri", {
    body: d.texte || "C'est l'heure de réviser un peu.",
    icon: "{% static 'wiki/icone-192.png' %}",
    badge: "{% static 'wiki/icone-192.png' %}",
    tag: "rappel-quotidien",
    data: { url: d.url || "/aujourdhui/" },
  }));
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = new URL((event.notification.data && event.notification.data.url) || "/", self.location.origin).href;
  event.waitUntil((async () => {
    for (const c of await self.clients.matchAll({ type: "window", includeUncontrolled: true })) {
      if (c.url === url && "focus" in c) return c.focus();
    }
    return self.clients.openWindow(url);
  })());
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (request.mode === "navigate") {
    event.respondWith(navigation(request));
    return;
  }
  const local = url.origin === self.location.origin;
  if (local && exclu(url.pathname)) return;
  if (local && url.pathname.startsWith("/fichiers/") && /\.pdf$/i.test(url.pathname)) {
    // PDF : servis depuis le cache s'ils ont été gardés (dossier hors ligne), jamais
    // mis en cache au passage (trop gros).
    event.respondWith(caches.match(request).then((r) => r || fetch(request)));
    return;
  }
  if ((local && (url.pathname.startsWith("/static/") || url.pathname.startsWith("/fichiers/"))) || request.url.startsWith(CDN)) {
    event.respondWith(reseauPuisCache(request));
  }
});
