---
tags:
  - getting-started
ordre: 3
---

# Rester Organisé

---

Que nous réalisions des évaluations pour des clients, que nous participions à des CTFs, que nous suivions un cours sur Academy ou ailleurs, ou que nous jouions sur des boxes/labs HTB, l'organisation est toujours cruciale. Il est essentiel de donner la priorité à une documentation claire et précise dès le tout début. Cette compétence nous sera bénéfique, quelle que soit la voie que nous empruntons dans la sécurité de l'information ou même dans d'autres carrières.

---

## Structure des Dossiers

Lorsque nous attaquons une seule machine, un laboratoire ou l'environnement d'un client, nous devrions avoir une structure de dossiers claire sur notre machine d'attaque pour sauvegarder des données telles que : les informations de périmètre (scoping), les données d'énumération, les preuves de tentatives d'exploitation, les données sensibles comme les identifiants, et d'autres données obtenues pendant la reconnaissance (recon), l'exploitation et la post-exploitation. Un exemple de structure de dossiers pourrait ressembler à ce qui suit :

```bash
Hiterof13@htb[/htb]$ tree Projects/  Projects/
└── Acme Company
    ├── EPT
    │   ├── evidence
    │   │   ├── credentials
    │   │   ├── data
    │   │   └── screenshots
    │   ├── logs
    │   ├── scans
    │   ├── scope
    │   └── tools
    └── IPT
        ├── evidence
        │   ├── credentials
        │   │   ├── data
        │   │   └── screenshots
        ├── logs
        ├── scans
        ├── scope
        └── tools
```

Ici, nous avons un dossier pour le client `Acme Company` avec deux évaluations, un Test d'Intrusion Interne (IPT) et un Test d'Intrusion Externe (EPT). Sous chaque dossier, nous avons des sous-dossiers pour enregistrer les données de scan, tous les outils pertinents, les journaux (logs), les informations de périmètre (c'est-à-dire les listes d'IP/réseaux à fournir à nos outils de scan), et un dossier de preuves qui peut contenir tous les identifiants récupérés pendant l'évaluation, toutes les données pertinentes récupérées ainsi que des captures d'écran.

C'est une préférence personnelle, mais certaines personnes créent un dossier pour chaque hôte cible et y enregistrent les captures d'écran. D'autres organisent leurs notes par hôte ou par réseau et enregistrent les captures d'écran directement dans leur outil de prise de notes. Expérimentez avec les structures de dossiers et voyez ce qui fonctionne le mieux pour vous afin de rester organisé et de travailler le plus efficacement possible.

---

## Outils de Prise de Notes

La productivité et l'organisation sont très importantes. Un testeur d'intrusion (penetration tester) très technique mais désorganisé aura du mal à réussir dans ce secteur. Divers outils peuvent être utilisés pour l'organisation et la prise de notes. Le choix d'un outil de prise de notes est très personnel. Certains d'entre nous n'auront peut-être pas besoin d'une fonctionnalité qu'une autre personne requiert en fonction de son flux de travail. Voici quelques excellentes options à explorer :

||||
|---|---|---|
|[Cherrytree](https://www.giuspen.com/cherrytree)|[Visual Studio Code](https://code.visualstudio.com/)|[Evernote](https://evernote.com/)|
|[Notion](https://www.notion.so/)|[GitBook](https://www.gitbook.com/)|[Sublime Text](https://www.sublimetext.com/)|
|[Notepad++](https://notepad-plus-plus.org/downloads)|||

Certains de ces outils sont plus axés sur la prise de notes, tandis que d'autres comme Notion et GitBook ont des fonctionnalités plus riches qui peuvent être utilisées pour créer des pages de type Wiki, des aide-mémoires, et plus encore. Il est important de s'assurer que toutes les données client sont stockées uniquement localement et non synchronisées sur le cloud si vous utilisez l'un de ces outils lors d'évaluations réelles.

Astuce : Apprendre le langage [Markdown](https://en.wikipedia.org/wiki/Markdown) est facile et très utile pour la prise de notes, car il peut être facilement représenté de manière visuellement attrayante et organisée.

---

## Autres Outils et Astuces

Chaque professionnel de la sécurité de l'information devrait maintenir une base de connaissances. Celle-ci peut être au format de votre choix (bien que les outils ci-dessus soient recommandés). Cette base de connaissances devrait contenir des guides de référence rapide pour les tâches de configuration que nous effectuons sur la plupart des évaluations et des aide-mémoires pour les commandes courantes que nous utilisons à chaque phase d'une évaluation.

À mesure que nous terminons des machines, des laboratoires, des évaluations, des formations, etc., nous devrions agréger chaque payload, commande, astuce, car nous ne savons jamais quand l'un d'eux pourrait s'avérer utile. Les avoir à portée de main augmentera notre efficacité et notre productivité globales. Chaque module de HTB Academy dispose d'un aide-mémoire des commandes pertinentes présentées dans les sections du module, que vous pouvez télécharger et conserver pour référence future.

Nous devrions également maintenir des listes de contrôle (checklists), des modèles de rapport pour divers types d'évaluation, et construire une base de données de résultats/vulnérabilités (findings). Cette base de données peut prendre la forme d'une feuille de calcul ou de quelque chose de plus complexe et inclure un titre de résultat, une description, un impact, des conseils de remédiation et des références. Avoir ces résultats déjà rédigés nous fera gagner un temps considérable et nous évitera de refaire le travail pendant la phase de rédaction du rapport, car la majeure partie des résultats sera déjà écrite et ne nécessitera probablement qu'une personnalisation pour l'environnement cible.

---

## Pour la Suite

Essayez divers outils de prise de notes et développez la structure de dossiers qui vous convient et qui correspond à votre méthodologie. Commencez tôt, pour que cela devienne une habitude ! Le walkthrough de Nibbles plus loin dans ce module est une excellente occasion de pratiquer notre documentation. De plus, ce module contient de nombreuses commandes qu'il est utile d'ajouter à notre aide-mémoire de commandes courantes.

---

← [[02 - Démarrer avec une Distribution de Pentest]] | [[00 - Sommaire Getting Started|Sommaire]] | [[04 - Se Connecter avec un VPN]] →
