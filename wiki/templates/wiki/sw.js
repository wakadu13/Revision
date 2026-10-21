{% load static %}// Service worker des QCM hors ligne (portée : /qcm/).
// - Garde en cache la page hors ligne, ses scripts, styles et KaTeX : la page
//   s'ouvre sans connexion (sinon, toute page de /qcm/ y renvoie).
// - Envoie les réponses en attente dès que la connexion revient (Background Sync).
importScripts("{% static 'wiki/qcm_attente.js' %}");

const CACHE = QcmAttente.CACHE;
const COQUILLE = "{% url 'wiki:quiz_offline' %}";
const KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.47/dist/";
const A_PRECHARGER = [
  COQUILLE,
  "{% url 'wiki:quiz_manifest' %}",
  "{% static 'wiki/wiki.css' %}",
  "{% static 'wiki/quiz.js' %}",
  "{% static 'wiki/qcm_attente.js' %}",
  "{% static 'wiki/qcm_hors_ligne.js' %}",
  "{% static 'wiki/icone-192.png' %}",
  KATEX + "katex.min.css",
  KATEX + "katex.min.js",
];
// Réponses de l'API : jamais mises en cache (les données sont dans IndexedDB).
const API = "{% url 'wiki:quiz_offline' %}";
const DELAI_RESEAU_MS = 4000;

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    // Une à une : un fichier indisponible n'empêche pas d'installer le reste.
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
      if (nom.startsWith("qcm-hors-ligne") && nom !== CACHE) await caches.delete(nom);
    }
    await self.clients.claim();
  })());
});

// Réseau d'abord (avec délai : une connexion très faible ne bloque pas la page),
// puis le cache. Les bonnes réponses sont gardées en cache pour la prochaine fois.
async function reseauPuisCache(request, cleCache) {
  const cache = await caches.open(CACHE);
  try {
    const reponse = await Promise.race([
      fetch(request),
      new Promise((_, rej) => setTimeout(() => rej(new Error("délai dépassé")), DELAI_RESEAU_MS)),
    ]);
    // Une page de connexion (session expirée) ne remplace pas la page en cache.
    if (reponse.ok && !reponse.redirected && reponse.type !== "opaqueredirect") {
      await cache.put(cleCache || request, reponse.clone());
    }
    return reponse;
  } catch (e) {
    const enCache = await cache.match(cleCache || request, { ignoreSearch: !!cleCache });
    if (enCache) return enCache;
    throw e;
  }
}

// Page hors ligne et autres pages du QCM : si le réseau ne répond pas, la page
// hors ligne en cache prend le relais.
async function navigation(request) {
  const url = new URL(request.url);
  if (url.pathname === COQUILLE) return reseauPuisCache(request, COQUILLE);
  try {
    return await fetch(request);
  } catch (e) {
    const enCache = await caches.match(COQUILLE);
    if (enCache) return enCache;
    throw e;
  }
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (request.mode === "navigate") {
    event.respondWith(navigation(request));
    return;
  }
  const local = url.origin === self.location.origin;
  if (local && url.pathname.startsWith(API) && url.pathname !== COQUILLE) return;
  // Fichiers statiques, images des questions (/fichiers/), KaTeX et ses polices.
  if ((local && (url.pathname.startsWith("/static/") || url.pathname.startsWith("/fichiers/")
      || url.pathname === "{% url 'wiki:quiz_manifest' %}")) || request.url.startsWith(KATEX)) {
    event.respondWith(reseauPuisCache(request));
  }
});

self.addEventListener("sync", (event) => {
  if (event.tag === "qcm-envoi") event.waitUntil(QcmAttente.envoyer());
});
