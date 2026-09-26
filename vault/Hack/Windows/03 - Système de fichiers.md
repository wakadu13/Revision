---
tags:
  - windows
ordre: 3
---

# Système de fichiers

---

Il existe 5 types de systèmes de fichiers Windows : FAT12, FAT16, FAT32, NTFS, et exFAT. Les systèmes FAT12 et FAT16 ne sont plus utilisés sur les systèmes d'exploitation Windows modernes. Dans cette formation, nous aborderons les systèmes de fichiers FAT32 et exFAT, mais nous nous concentrerons principalement sur le système de fichiers NTFS.

FAT32 (File Allocation Table, ou table d'allocation de fichiers) est largement utilisé sur de nombreux types de périphériques de stockage tels que les clés USB et les cartes SD, mais peut également être utilisé pour formater des disques durs. Le "32" dans le nom fait référence au fait que FAT32 utilise 32 bits de données pour identifier les clusters de données sur un périphérique de stockage.

**`Avantages de FAT32 :`**

- Compatibilité des périphériques - il peut être utilisé sur des ordinateurs, des appareils photo numériques, des consoles de jeux, des smartphones, des tablettes, et plus encore.
- Compatibilité multi-systèmes d'exploitation - Il fonctionne sur tous les systèmes d'exploitation Windows à partir de Windows 95 et est également pris en charge par MacOS et Linux.

**`Inconvénients de FAT32 :`**

- Ne peut être utilisé qu'avec des fichiers de moins de 4 Go.
- Aucune fonctionnalité intégrée de protection des données ou de compression de fichiers.
- Nécessite l'utilisation d'outils tiers pour le chiffrement de fichiers.

NTFS (New Technology File System, ou système de fichiers de nouvelle technologie) est le système de fichiers par défaut de Windows depuis Windows NT 3.1. En plus de combler les lacunes de FAT32, NTFS offre également un meilleur support pour les métadonnées et de meilleures performances grâce à une structuration améliorée des données.

**`Avantages de NTFS :`**

- NTFS est fiable et peut restaurer la cohérence du système de fichiers en cas de panne système ou de coupure de courant.
- Fournit la sécurité en nous permettant de définir des autorisations granulaires sur les fichiers et les dossiers.
- Prend en charge des partitions de très grande taille.
- Dispose d'une journalisation (journaling) intégrée, ce qui signifie que les modifications de fichiers (ajout, modification, suppression) sont enregistrées.

**`Inconvénients de NTFS :`**

- La plupart des appareils mobiles ne prennent pas en charge NTFS nativement.
- Les appareils multimédias plus anciens tels que les téléviseurs et les appareils photo numériques n'offrent pas de prise en charge pour les périphériques de stockage NTFS.

---

## Autorisations

Le système de fichiers NTFS dispose de nombreuses autorisations de base et avancées. Voici quelques-uns des principaux types d'autorisation :

|Type d'autorisation|Description|
|---|---|
|Contrôle total|Permet de lire, écrire, modifier et supprimer des fichiers/dossiers.|
|Modifier|Permet de lire, écrire et supprimer des fichiers/dossiers.|
|Affichage du contenu du dossier|Permet de visualiser et de lister les dossiers et sous-dossiers ainsi que d'exécuter des fichiers. Seuls les dossiers héritent de cette autorisation.|
|Lecture et exécution|Permet de visualiser et de lister les fichiers et sous-dossiers ainsi que d'exécuter des fichiers. Les fichiers et les dossiers héritent de cette autorisation.|
|Écriture|Permet d'ajouter des fichiers aux dossiers et sous-dossiers et d'écrire dans un fichier.|
|Lecture|Permet de visualiser et de lister les dossiers et sous-dossiers et de consulter le contenu d'un fichier.|
|Parcours de dossier|Permet ou refuse la capacité de naviguer à travers les dossiers pour atteindre d'autres fichiers ou dossiers. Par exemple, un utilisateur peut ne pas avoir l'autorisation de lister le contenu du répertoire ou de voir les fichiers dans le répertoire des documents ou des applications web dans cet exemple c:\users\bsmith\documents\webapps\backups\backup_02042020.zip mais avec les autorisations de Parcours de dossier appliquées, il peut accéder à l'archive de sauvegarde.|

Les fichiers et les dossiers héritent des autorisations NTFS de leur dossier parent pour faciliter l'administration, de sorte que les administrateurs n'ont pas besoin de définir explicitement les autorisations pour chaque fichier et dossier, car cela prendrait énormément de temps. Si des autorisations doivent être définies explicitement, un administrateur peut désactiver l'héritage des autorisations pour les fichiers et dossiers nécessaires, puis définir les autorisations directement sur chacun d'eux.

---

## Liste de contrôle d'accès pour le contrôle d'intégrité (icacls)

Les autorisations NTFS sur les fichiers et les dossiers dans Windows peuvent être gérées à l'aide de l'interface graphique (GUI) de l'Explorateur de fichiers sous l'onglet Sécurité. En dehors de l'interface graphique, nous pouvons également atteindre un niveau de granularité élevé sur les autorisations de fichiers NTFS dans Windows depuis la ligne de commande à l'aide de l'utilitaire icacls.

Nous pouvons lister les autorisations NTFS d'un répertoire spécifique en exécutant soit `icacls` depuis le répertoire de travail, soit `icacls C:\Windows` sur un répertoire qui n'est pas l'actuel.

```cmd
C:\htb> icacls c:\windows c:\windows NT SERVICE\TrustedInstaller:(F)            NT SERVICE\TrustedInstaller:(CI)(IO)(F)            NT AUTHORITY\SYSTEM:(M)            NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)            BUILTIN\Administrators:(M)            BUILTIN\Administrators:(OI)(CI)(IO)(F)            BUILTIN\Users:(RX)            BUILTIN\Users:(OI)(CI)(IO)(GR,GE)            CREATOR OWNER:(OI)(CI)(IO)(F)            APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(RX)            APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(OI)(CI)(IO)(GR,GE)            APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(RX)            APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(OI)(CI)(IO)(GR,GE)  Successfully processed 1 files; Failed processing 0 files
```

Le niveau d'accès à la ressource est indiqué après chaque utilisateur dans la sortie. Les paramètres d'héritage possibles sont :

- `(CI)` : héritage des conteneurs (container inherit)
- `(OI)` : héritage des objets (object inherit)
- `(IO)` : héritage seul (inherit only)
- `(NP)` : ne pas propager l'héritage (do not propagate inherit)
- `(I)` : autorisation héritée du conteneur parent (permission inherited from parent container)

Dans l'exemple ci-dessus, le compte `NT AUTHORITY\SYSTEM` a les autorisations d'héritage des objets, d'héritage des conteneurs, d'héritage seul et d'accès total. Cela signifie que ce compte a un contrôle total sur tous les objets du système de fichiers dans ce répertoire et ses sous-répertoires.

Les autorisations d'accès de base sont les suivantes :

- `F` : accès total (full access)
- `D` : accès en suppression (delete access)
- `N` : aucun accès (no access)
- `M` : accès en modification (modify access)
- `RX` : accès en lecture et exécution (read and execute access)
- `R` : accès en lecture seule (read-only access)
- `W` : accès en écriture seule (write-only access)

Nous pouvons ajouter et supprimer des autorisations via la ligne de commande en utilisant `icacls`. Ici, nous exécutons `icacls` dans le contexte d'un compte administrateur local montrant le répertoire `C:\users` où l'utilisateur `joe` n'a aucune autorisation d'écriture.

```cmd
C:\htb> icacls c:\Users c:\Users NT AUTHORITY\SYSTEM:(OI)(CI)(F)          BUILTIN\Administrators:(OI)(CI)(F)          BUILTIN\Users:(RX)          BUILTIN\Users:(OI)(CI)(IO)(GR,GE)          Everyone:(RX)          Everyone:(OI)(CI)(IO)(GR,GE)  Successfully processed 1 files; Failed processing 0 files
```

En utilisant la commande `icacls c:\users /grant joe:f`, nous pouvons accorder à l'utilisateur joe le contrôle total sur le répertoire, mais étant donné que `(oi)` et `(ci)` n'ont pas été inclus dans la commande, l'utilisateur joe n'aura des droits que sur le dossier `c:\users` mais pas sur les sous-répertoires et les fichiers qu'ils contiennent.

```cmd
C:\htb> icacls c:\users /grant joe:f processed file: c:\users Successfully processed 1 files; Failed processing 0 files
```

```cmd
C:\htb> >icacls c:\users c:\users WS01\joe:(F)          NT AUTHORITY\SYSTEM:(OI)(CI)(F)          BUILTIN\Administrators:(OI)(CI)(F)          BUILTIN\Users:(RX)          BUILTIN\Users:(OI)(CI)(IO)(GR,GE)          Everyone:(RX)          Everyone:(OI)(CI)(IO)(GR,GE)  Successfully processed 1 files; Failed processing 0 files
```

Ces autorisations peuvent être révoquées à l'aide de la commande `icacls c:\users /remove joe`.

`icacls` est très puissant et peut être utilisé dans un environnement de domaine pour donner à certains utilisateurs ou groupes des autorisations spécifiques sur un fichier ou un dossier, refuser explicitement l'accès, activer ou désactiver les autorisations d'héritage, et changer la propriété des répertoires/fichiers.

Une liste complète des arguments de la ligne de commande `icacls` et des paramètres d'autorisation détaillés peut être trouvée [ici](https://ss64.com/nt/icacls.html).
---

← [[02 - Structure du système d'exploitation]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[04 - Autorisations NTFS vs autorisations de partage]] →
