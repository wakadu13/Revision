---
tags:
  - getting-started
ordre: 23
---

# Bilan des connaissances

---

Mettons en pratique tout ce que nous avons appris dans ce module et attaquons notre première machine sans guide.

---

## Astuces

Rappelez-vous que l'énumération est un processus itératif. Après avoir effectué nos scans de ports avec `Nmap`, assurez-vous de réaliser une énumération détaillée de tous les ports ouverts en fonction de ce qui s'y exécute. Suivez le même processus que celui que nous avons utilisé avec `Nibbles` :

- Énumération/Scan avec `Nmap` - effectuez un scan rapide des ports ouverts, suivi d'un scan complet de tous les ports
- Prise d'empreinte web (Web Footprinting) - vérifiez tous les ports web identifiés à la recherche d'applications web en cours d'exécution et de fichiers/répertoires cachés. Parmi les outils utiles pour cette phase, on trouve `whatweb` et `Gobuster`
- Si vous identifiez l'URL du site web, vous pouvez l'ajouter à votre fichier `/etc/hosts` avec l'adresse IP que vous obtiendrez dans la question ci-dessous pour le charger normalement, bien que cela ne soit pas nécessaire.
- Après avoir identifié les technologies utilisées, utilisez un outil tel que `Searchsploit` pour trouver des exploits publics ou recherchez sur Google des techniques d'exploitation manuelle
- Après avoir obtenu un accès initial (initial foothold), utilisez l'astuce `Python3 pty` pour passer à un pseudo TTY
- Effectuez une énumération manuelle et automatisée du système de fichiers, à la recherche de mauvaises configurations, de services présentant des vulnérabilités connues et de données sensibles en clair telles que des identifiants
- Organisez ces données hors ligne pour déterminer les différentes manières d'élever les privilèges au niveau root sur cette cible

Il existe deux façons d'obtenir un accès initial : l'une à l'aide de `Metasploit` et l'autre via un processus manuel. Mettez-vous au défi de les essayer toutes les deux pour bien comprendre chaque méthode.

Il y a deux façons d'élever les privilèges au niveau root sur la cible après avoir obtenu un accès initial. Utilisez des scripts d'aide comme [LinEnum](https://github.com/rebootuser/LinEnum) et [LinPEAS](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS) pour vous assister. Triez les informations à la recherche de deux techniques d'élévation de privilèges (privilege escalation) bien connues.

Amusez-vous bien, n'arrêtez jamais d'apprendre, et n'oubliez pas de `think outside of the box`
---

← [[22 - Prochaines Étapes]] | [[00 - Sommaire Getting Started|Sommaire]]
