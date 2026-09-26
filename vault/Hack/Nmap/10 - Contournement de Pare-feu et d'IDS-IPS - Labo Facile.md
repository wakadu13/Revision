---
tags:
  - nmap
ordre: 10
---

# Contournement de Pare-feu et d'IDS/IPS - Labo Facile

---

Passons maintenant à la pratique. Une entreprise nous a engagés pour tester ses défenses de sécurité informatique, y compris ses systèmes de détection d'intrusion (`IDS`) et de prévention d'intrusion (`IPS`). Notre client souhaite renforcer sa sécurité informatique et apportera donc des améliorations spécifiques à ses systèmes `IDS/IPS` après chaque test réussi. Cependant, nous ne savons pas selon quelles directives ces changements seront effectués. Notre objectif est de découvrir des informations spécifiques à partir des situations données.

On nous fournit uniquement une machine protégée par des systèmes `IDS/IPS` et qui peut être testée. À des fins d'apprentissage et pour avoir une idée du comportement des `IDS/IPS`, nous avons accès à une page web d'état à l'adresse suivante :

http://<target>/status.php

![](https://academy.hackthebox.com/app/module/19/section/117)

Cette page nous montre le nombre d'alertes. Nous savons que si nous recevons un certain nombre d'alertes, nous serons `bannis`. Par conséquent, nous devons tester le système cible aussi `discrètement` que possible.
---

← [[09 - Évasion de Pare-feu et d'IDS-IPS]] | [[00 - Sommaire Nmap|Sommaire]] | [[11 - Contournement de Pare-feu et d'IDS-IPS - Labo Moyen]] →
