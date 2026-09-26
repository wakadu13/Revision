---
tags:
  - windows
ordre: 15
---

# Évaluation des compétences - Principes fondamentaux de Windows

---

Inlanefreight a récemment connu un incident au cours duquel un employé mécontent du service marketing a accédé à un partage RH hébergé en interne et a supprimé plusieurs fichiers et dossiers confidentiels. Heureusement, l'équipe informatique disposait de bonnes sauvegardes et a restauré toutes les données supprimées. On s'inquiète maintenant du fait que cet employé mécontent ait pu, en premier lieu, accéder au partage RH. Après avoir réalisé une évaluation de la sécurité, vous avez découvert que l'équipe IT ne comprend peut-être pas entièrement le fonctionnement des autorisations (permissions) dans Windows. Vous organisez une formation et une démonstration pour montrer au service les bonnes pratiques de sécurité en matière de partage de fichiers dans un environnement Windows, ainsi que la consultation des services depuis la ligne de commande pour vérifier toute manipulation potentielle.

Remarque : Il est important que chaque étape soit réalisée dans l'ordre de présentation. Commencez par l'étape 1 et progressez jusqu'à l'étape 8, en incluant toutes les spécifications associées à chaque étape. Sachez que chaque étape est conçue pour vous donner l'occasion d'appliquer les compétences et les concepts enseignés tout au long de ce module. Prenez votre temps, amusez-vous et n'hésitez pas à demander de l'aide si vous êtes bloqué.

Dans cette démonstration, vous allez :

## 1. Créer un dossier partagé nommé Company Data

## 2. Créer un sous-dossier nommé HR à l'intérieur du dossier Company Data

## 3. Créer un utilisateur nommé Jim

- `Décocher : L'utilisateur doit changer le mot de passe à la prochaine ouverture de session`

## 4. Créer un groupe de sécurité nommé HR

## 5. Ajouter Jim au groupe de sécurité HR

## 6. Ajouter le groupe de sécurité HR au dossier partagé Company Data et à la liste des autorisations NTFS

- `Supprimer le groupe présent par défaut`
- `Autorisations de partage : Autoriser Modifier et Lecture`
- `Désactiver l'héritage avant d'attribuer des autorisations NTFS spécifiques`
- `Autorisations NTFS : Modification, Lecture et exécution, Affichage du contenu du dossier, Lecture, Écriture`

## 7. Ajouter le groupe de sécurité HR à la liste des autorisations NTFS du sous-dossier HR

- `Supprimer le groupe présent par défaut`
- `Désactiver l'héritage avant d'attribuer des autorisations NTFS spécifiques`
- `Autorisations NTFS : Modification, Lecture et exécution, Affichage du contenu du dossier, Lecture, et Écriture`

## 8. Utiliser PowerShell pour lister les détails d'un service
---

← [[14 - Sécurité Windows]] | [[00 - Sommaire Windows Fundamentals|Sommaire]]
