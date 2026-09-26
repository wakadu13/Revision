---
tags:
  - linux
ordre: 15
---

# Gestion des utilisateurs

Une gestion efficace des utilisateurs est un aspect fondamental de l'administration système Linux. Les administrateurs doivent fréquemment créer de nouveaux comptes utilisateurs ou affecter des utilisateurs existants à des groupes spécifiques pour appliquer les contrôles d'accès appropriés. De plus, l'exécution de commandes en tant qu'un autre utilisateur est souvent nécessaire pour des tâches qui requièrent des privilèges différents. Par exemple, certains groupes peuvent avoir des permissions exclusives pour afficher ou modifier des fichiers ou des répertoires spécifiques, ce qui est essentiel pour maintenir la sécurité et l'intégrité du système. Cette capacité nous permet de recueillir des informations plus détaillées localement sur la machine, ce qui peut être d'une importance capitale à des fins de dépannage ou d'audit.

Par exemple, imaginez qu'un nouvel employé nommé Alex rejoigne votre entreprise et reçoive un poste de travail sous Linux pour effectuer ses tâches. En tant qu'administrateur système, vous devez créer un compte utilisateur pour Alex et l'ajouter aux groupes appropriés qui lui donnent accès aux ressources nécessaires, telles que les fichiers de projet ou les outils de développement. De plus, il peut y avoir des situations où Alex a besoin d'exécuter des commandes avec des privilèges élevés ou en tant qu'un autre utilisateur pour accomplir certaines tâches.

## Exécution en tant qu'utilisateur

```bash
Hiterof13@htb[/htb]$ cat /etc/shadow
cat: /etc/shadow: Permission denied
```

Le fichier `/etc/shadow` est un fichier système critique qui stocke les informations de mot de passe chiffrées pour tous les comptes utilisateurs. Pour des raisons de sécurité, il n'est lisible et modifiable que par l'utilisateur root afin d'empêcher tout accès non autorisé aux données d'authentification sensibles.

Pour effectuer des tâches nécessitant des privilèges élevés, les utilisateurs peuvent utiliser la commande `sudo`. La commande `sudo`, abréviation de « superuser do », permet aux utilisateurs autorisés d'exécuter des commandes avec les privilèges de sécurité d'un autre utilisateur, généralement le superutilisateur ou root. Cela permet aux utilisateurs d'effectuer des tâches administratives sans se connecter en tant qu'utilisateur root, ce qui est une meilleure pratique pour maintenir la sécurité du système. Nous explorerons les permissions de sudo plus en détail dans la section `Linux Security`.

## Exécution en tant que root

```bash
Hiterof13@htb[/htb]$ sudo cat /etc/shadow
root:<SNIP>:18395:0:99999:7:::
daemon:*:17737:0:99999:7:::
bin:*:17737:0:99999:7:::
<SNIP>
```

Voici une liste qui nous aidera à mieux comprendre et à gérer la gestion des utilisateurs.

|**Commande**|**Description**|
|---|---|
|`sudo`|Exécute une commande en tant qu'un autre utilisateur.|
|`su`|L'utilitaire `su` demande les informations d'identification de l'utilisateur approprié via PAM et bascule sur cet ID utilisateur (l'utilisateur par défaut est le superutilisateur). Un shell est ensuite exécuté.|
|`useradd`|Crée un nouvel utilisateur ou met à jour les informations par défaut des nouveaux utilisateurs.|
|`userdel`|Supprime un compte utilisateur et les fichiers associés.|
|`usermod`|Modifie un compte utilisateur.|
|`addgroup`|Ajoute un groupe au système.|
|`delgroup`|Supprime un groupe du système.|
|`passwd`|Change le mot de passe d'un utilisateur.|

Comprendre comment fonctionnent les comptes utilisateurs, les permissions et les mécanismes d'authentification nous permet d'identifier les vulnérabilités, d'exploiter les erreurs de configuration et d'évaluer efficacement la posture de sécurité d'un système. La manière la plus efficace d'acquérir des compétences en gestion des utilisateurs est de s'entraîner à utiliser les commandes individuelles avec leurs différentes options dans un environnement contrôlé.

N'hésitez pas à expérimenter avec les différentes commandes et à explorer leurs fonctionnalités. Il est important de laisser votre créativité vous guider pour décider de ce que vous voulez accomplir. En combinant ces outils de gestion des utilisateurs avec les connaissances que vous avez acquises dans les sections précédentes, vous réaliserez tout ce que vous avez déjà appris. Mettez en pratique votre compréhension du système Linux : créez de nouveaux comptes utilisateurs, configurez des fichiers et des répertoires pour ces utilisateurs, sélectionnez des fichiers, lisez et filtrez des éléments spécifiques, et redirigez-les vers les fichiers et répertoires des nouveaux utilisateurs que vous avez créés. N'hésitez pas à explorer en profondeur. Sur votre système cible, il n'y a rien qui ne puisse être réparé, et même si quelque chose ne va pas, vous avez la possibilité de réinitialiser la cible et de recommencer jusqu'à ce que vous vous sentiez en confiance.

---

← [[14 - Gestion des permissions]] | [[00 - Sommaire Linux|Sommaire]] | [[16 - Gestion de paquets]] →
