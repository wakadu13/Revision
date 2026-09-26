---
tags:
  - web-applications
ordre: 9
---

# Script inter-sites (Cross-Site Scripting - XSS)

---

Les vulnérabilités d'injection HTML (`HTML Injection`) peuvent souvent être exploitées pour réaliser des attaques de [script inter-sites (Cross-Site Scripting - XSS)](https://owasp.org/www-community/attacks/xss/) en injectant du code `JavaScript` à exécuter côté client. Une fois que nous pouvons exécuter du code sur la machine de la victime, nous pouvons potentiellement obtenir l'accès au compte de la victime ou même à sa machine. En pratique, le `XSS` est très similaire à l'injection HTML. Cependant, le `XSS` implique l'injection de code `JavaScript` pour effectuer des attaques plus avancées côté client, au lieu de se contenter d'injecter du code HTML. Il existe trois principaux types de `XSS` :

|Type|Description|
|---|---|
|`Reflected XSS`|Se produit lorsqu'une entrée utilisateur est affichée sur la page après traitement (p. ex., un résultat de recherche ou un message d'erreur).|
|`Stored XSS`|Se produit lorsqu'une entrée utilisateur est stockée dans la base de données back-end, puis affichée lors de sa récupération (p. ex., des publications ou des commentaires).|
|`DOM XSS`|Se produit lorsqu'une entrée utilisateur est directement affichée dans le navigateur et est écrite dans un objet `DOM` `HTML` (p. ex., un nom d'utilisateur ou un titre de page vulnérable).|

Dans l'exemple que nous avons vu pour l'injection HTML, il n'y avait aucun assainissement des entrées. Par conséquent, il est possible que la même page soit vulnérable aux attaques `XSS`. Nous pouvons essayer d'injecter le code `JavaScript` `DOM XSS` suivant comme charge utile (payload), ce qui devrait nous montrer la valeur du cookie de l'utilisateur actuel :

```javascript
#"><img src=/ onerror=alert(document.cookie)>
```

Une fois que nous avons saisi notre charge utile et cliqué sur `ok`, nous voyons qu'une fenêtre d'alerte apparaît avec la valeur du cookie :

![Boîte de dialogue affichant une valeur de cookie et un bouton « Fermer ».](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/web_apps_xss_2.jpg)

Cette charge utile accède à l'arborescence du document `HTML` et récupère la valeur de l'objet `cookie`. Lorsque le navigateur traite notre entrée, elle sera considérée comme un nouveau `DOM`, et notre `JavaScript` sera exécuté, nous affichant en retour la valeur du cookie dans une fenêtre contextuelle (popup).

Un attaquant peut exploiter cela pour voler des sessions de cookie, se les envoyer à lui-même et tenter d'utiliser la valeur du cookie pour s'authentifier sur le compte de la victime. La même attaque peut être utilisée pour mener divers autres types d'attaques contre les utilisateurs d'une application web. Le `XSS` est un vaste sujet qui sera traité en profondeur dans des modules ultérieurs.
---

← [[08 - Injection HTML]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[10 - Falsification de requête inter-site (Cross-Site Request Forgery - CSRF)]] →
