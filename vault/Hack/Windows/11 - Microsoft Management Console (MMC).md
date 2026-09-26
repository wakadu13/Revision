---
tags:
  - windows
ordre: 11
---

# Microsoft Management Console (MMC)

---

La MMC peut être utilisée pour regrouper des composants logiciel enfichables (snap-ins), ou outils d'administration, afin de gérer les composants matériels, logiciels et réseau au sein d'un hôte Windows. Elle existe depuis Windows Server 2000 et fonctionne sur toutes les versions de Windows. Nous pouvons également utiliser la MMC pour créer des outils personnalisés et les distribuer aux utilisateurs. La MMC fonctionne sur le concept de composants logiciel enfichables, permettant aux administrateurs de créer une console personnalisée avec uniquement les outils d'administration nécessaires pour gérer plusieurs services. Ces composants logiciel enfichables peuvent être ajoutés pour gérer à la fois les systèmes locaux et distants.

Nous pouvons ouvrir la MMC en tapant simplement `mmc` dans le menu Démarrer. Lorsque nous ouvrons la MMC pour la première fois, elle est vide.

![Fenêtre de la console sans aucun élément affiché, montrant la Racine de la console et le volet Actions.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/MMC.png)

À partir de là, nous pouvons naviguer vers Fichier --> `Ajouter/Supprimer un composant logiciel enfichable`, et commencer à personnaliser notre console d'administration.

![Fenêtre Ajouter/Supprimer un composant logiciel enfichable montrant les composants logiciel enfichables disponibles comme Contrôle ActiveX et les composants logiciel enfichables sélectionnés comme Racine de la console.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/MMC_add_remove.png)

Lorsque nous commençons à ajouter des composants logiciel enfichables, il nous sera demandé si nous voulons ajouter le composant pour gérer uniquement l'ordinateur local ou s'il sera utilisé pour gérer un autre ordinateur sur le réseau.

![Fenêtre de sélection du composant logiciel enfichable Services avec les options pour gérer l'ordinateur local ou un autre ordinateur.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/MMC_services.png)

Une fois que nous avons fini d'ajouter les composants logiciel enfichables, ils apparaîtront sur le côté gauche de la MMC. À partir de là, nous pouvons enregistrer l'ensemble des composants logiciel enfichables sous forme de fichier .msc, afin qu'ils soient tous chargés la prochaine fois que nous ouvrirons la MMC. Par défaut, ils sont enregistrés dans le répertoire Outils d'administration Windows sous le menu Démarrer. La prochaine fois que nous ouvrirons la MMC, nous pourrons choisir de charger n'importe laquelle des vues que nous avons créées.

![Boîte de dialogue Ouvrir montrant le dossier Outils d'administration Windows avec le fichier management.msc.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/saved_msc.png)
---

← [[10 - Windows Management Instrumentation (WMI)]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[12 - Sous-système Windows pour Linux (WSL)]] →
