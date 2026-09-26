---
tags:
  - networking
ordre: 4
---

# Proxys

---

Beaucoup de gens ont des opinions différentes sur ce qu'est un proxy :

- Les professionnels de la sécurité pensent immédiatement aux `proxys HTTP` (BurpSuite) ou au pivotement avec un `proxy SOCKS/SSH` (`Chisel`, `ptunnel`, `sshuttle`).
- Les développeurs web utilisent des proxys comme Cloudflare ou ModSecurity pour bloquer le trafic malveillant.
- Le grand public peut penser qu'un proxy est utilisé pour masquer sa localisation et accéder au catalogue Netflix d'un autre pays.
- Les forces de l'ordre attribuent souvent les proxys à des activités illégales.

Tous les exemples ci-dessus ne sont pas corrects. Un proxy est un appareil ou un service qui se place au milieu d'une connexion et agit comme un médiateur. Le terme `médiateur` est l'information essentielle, car il signifie que l'appareil intermédiaire doit être capable d'inspecter le contenu du trafic. Sans la capacité d'être un `médiateur`, l'appareil est techniquement une `passerelle (gateway)`, et non un proxy.

Pour en revenir à la question ci-dessus, le grand public a une idée fausse de ce qu'est un proxy, car il utilise très probablement un VPN pour masquer sa localisation, ce qui n'est techniquement pas un proxy. La plupart des gens pensent que dès qu'une adresse IP change, il s'agit d'un proxy, et dans la plupart des cas, il est probablement préférable de ne pas les corriger, car c'est une idée fausse courante et inoffensive. Les corriger pourrait mener à une conversation plus longue qui dériverait sur les tabulations contre les espaces, `emacs` contre `vim`, ou à la découverte qu'ils sont un utilisateur de `nano`.

Si vous avez du mal à vous en souvenir, les proxys fonctionnent presque toujours à la Couche 7 du modèle OSI. Il existe de nombreux types de services de proxy, mais les principaux sont :

- `Proxy dédié` / `Proxy direct (Forward Proxy)`
- `Proxy inverse (Reverse Proxy)`
- `Proxy transparent (Transparent Proxy)`

---

## Proxy dédié / Proxy direct

Le `proxy direct (Forward Proxy)` est ce que la plupart des gens imaginent être un proxy. Un proxy direct est un ordinateur qui reçoit une requête d'un client et exécute cette requête en son nom.

Par exemple, dans un réseau d'entreprise, les ordinateurs sensibles peuvent ne pas avoir un accès direct à Internet. Pour accéder à un site web, ils doivent passer par un proxy (ou un filtre web). Cela peut être une ligne de défense incroyablement puissante contre les malwares, car non seulement le malware doit contourner le filtre web (facile), mais il doit également être `conscient de la présence du proxy (proxy aware)` ou utiliser un C2 non traditionnel (un moyen pour un malware de recevoir des instructions). Si l'organisation n'utilise que `FireFox`, la probabilité de rencontrer un malware conscient de la présence d'un proxy est faible.

Les navigateurs web comme Internet Explorer, Edge ou Chrome respectent tous par défaut les paramètres de "Proxy système". Si le malware utilise WinSock (API native de Windows), il sera probablement conscient de la présence du proxy sans aucun code supplémentaire. Firefox n'utilise pas `WinSock` mais `libcurl`, ce qui lui permet d'utiliser le même code sur n'importe quel système d'exploitation. Cela signifie que le malware devrait rechercher Firefox et extraire ses paramètres de proxy, ce qu'un malware a très peu de chances de faire.

Alternativement, un malware pourrait utiliser le DNS comme mécanisme de C2, mais si une organisation surveille le DNS (ce qui se fait facilement avec [Sysmon](https://medium.com/falconforce/sysmon-11-dns-improvements-and-filedelete-events-7a74f17ca842)), ce type de trafic devrait être rapidement détecté.

Un autre exemple de proxy direct est Burp Suite, que la plupart des gens utilisent pour transférer des requêtes HTTP. Cependant, cette application est le couteau suisse des proxys HTTP et peut être configurée pour être un proxy inverse ou transparent !

#### Proxy direct

![Schéma montrant l'hôte A envoyant une requête HTTP via un proxy direct vers Internet, atteignant un serveur web. L'hôte B est également connecté.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/forward_proxy.png)

---

## Proxy inverse

Comme vous l'avez peut-être deviné, un `proxy inverse (reverse proxy)` est l'inverse d'un `proxy direct (Forward Proxy)`. Au lieu d'être conçu pour filtrer les requêtes sortantes, il filtre les requêtes entrantes. L'objectif le plus courant d'un `proxy inverse` est d'écouter sur une adresse et de transférer le trafic vers un réseau fermé.

De nombreuses organisations utilisent CloudFlare car leur réseau robuste peut résister à la plupart des attaques DDOS. En utilisant Cloudflare, les organisations disposent d'un moyen de filtrer la quantité (et le type) de trafic envoyé à leurs serveurs web.

Les testeurs d'intrusion (Penetration Testers) configureront des proxys inverses sur les points de terminaison infectés. Le point de terminaison infecté écoutera sur un port et renverra tout client qui s'y connecte à l'attaquant à travers le point de terminaison infecté. C'est utile pour contourner les pare-feux ou échapper à la journalisation. Les organisations peuvent avoir des `systèmes de détection d'intrusion (IDS)`, qui surveillent les requêtes web externes. Si l'attaquant accède à l'organisation via SSH, un proxy inverse peut envoyer des requêtes web à travers le tunnel SSH et échapper à l'IDS.

Un autre proxy inverse courant est `ModSecurity`, un `pare-feu applicatif web (WAF)`. Les pare-feux applicatifs web inspectent les requêtes web à la recherche de contenu malveillant et bloquent la requête si elle l'est. Si vous voulez en savoir plus à ce sujet, nous vous recommandons de lire la documentation du [ModSecurity Core Rule Set](https://owasp.org/www-project-modsecurity-core-rule-set/), car c'est un excellent point de départ. Cloudflare peut également agir comme un WAF, mais cela nécessite de les autoriser à déchiffrer le trafic HTTPS, ce que certaines organisations peuvent ne pas souhaiter.

#### Proxy inverse

![Schéma montrant l'hôte A envoyant une requête HTTP via Internet, passant par des pare-feux, un proxy inverse et atteignant un serveur web. L'hôte B est également connecté.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/reverse_proxy.png)

---

## Proxy transparent (ou non)

Tous ces services de proxy agissent de manière `transparente` ou `non transparente`.

Avec un `proxy transparent`, le client n'a pas connaissance de son existence. Le proxy transparent intercepte les requêtes de communication du client vers Internet et agit comme une instance de substitution. Vers l'extérieur, le proxy transparent, tout comme le proxy non transparent, agit comme un partenaire de communication.

S'il s'agit d'un `proxy non transparent`, nous devons être informés de son existence. À cette fin, nous et le logiciel que nous voulons utiliser recevons une configuration de proxy spéciale qui garantit que le trafic vers Internet est d'abord adressé au proxy. Si cette configuration n'existe pas, nous ne pouvons pas communiquer via le proxy. Cependant, comme le proxy fournit généralement la seule voie de communication vers d'autres réseaux, la communication vers Internet est généralement coupée sans une configuration de proxy correspondante.
---

← [[03 - Topologies Réseau]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[05 - Modèles Réseau]] →
