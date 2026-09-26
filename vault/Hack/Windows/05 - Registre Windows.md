---
tags:
  - windows
ordre: 5
---

# Registre Windows

---

Le [Registre Windows](https://learn.microsoft.com/fr-fr/troubleshoot/windows-server/performance/windows-registry-advanced-users) (Windows Registry) est une base de données hiérarchique utilisée par Windows et de nombreuses applications installées pour stocker des informations de configuration. Il contient des paramètres relatifs aux profils utilisateur, aux logiciels, au matériel, aux services, aux politiques de sécurité et au système d'exploitation lui-même.

Un hôte Windows peut utiliser le Registre pour déterminer quelles applications s'exécutent lorsqu'un utilisateur se connecte, comment un service démarre, ou si une fonctionnalité de sécurité est activée. Les administrateurs système utilisent souvent le Registre lors de la configuration des systèmes, du déploiement de logiciels et du dépannage de problèmes.

Les erreurs lors de la manipulation du Registre peuvent entraîner l'arrêt du fonctionnement d'applications ou de composants Windows sous-jacents en raison des paramètres importants qu'il contient. Il est important de comprendre le but d'un paramètre avant de le modifier et, dans l'idéal, de le tester d'abord dans un environnement de laboratoire chaque fois que possible.

---

## Structure du Registre

Le Registre est organisé en `ruches` (hives), `clés` (keys), `sous-clés` (subkeys) et `valeurs` (values). Ces composants forment une hiérarchie similaire aux dossiers, sous-dossiers et fichiers dans le système de fichiers de Windows.

|Composant|Description|
|---|---|
|**Ruche**|Une section de premier niveau du Registre qui contient divers types de paramètres, tels que la configuration à l'échelle du système ou les paramètres de l'utilisateur actuel.|
|**Clé**|Un conteneur au sein d'une ruche, similaire à un dossier. Une clé peut contenir des clés et des valeurs supplémentaires.|
|**Sous-clé**|Une clé située sous une autre clé. Les sous-clés sont utilisées pour organiser les paramètres associés dans une hiérarchie.|
|**Valeur**|Un paramètre individuel stocké dans une clé. Chaque valeur a un nom, un type de données et ses données associées.|

Par exemple, étant donné le chemin de registre suivant :

```text
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion
```

![Visualisation d'un chemin du Registre dans Regedit.exe.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/reg_path.png)

Dans cet exemple :

- `HKEY_LOCAL_MACHINE` est la ruche.
- `SOFTWARE` est une clé dans la ruche.
- `Microsoft`, `Windows` et `CurrentVersion` sont des sous-clés en dessous.
- La sélection de `CurrentVersion` dans l'Éditeur du Registre affiche les valeurs stockées dans cette clé.

Les valeurs du Registre apparaissent dans le volet droit de l'Éditeur du Registre. Chaque valeur comprend trois composants principaux :

|Composant|Description|
|---|---|
|**Nom**|Identifie le paramètre.|
|**Type**|Détermine le type de données que la valeur peut stocker.|
|**Données**|Contient les informations de configuration.|

Vous trouverez ci-dessous quelques-unes des principales ruches du Registre présentes dans chaque système d'exploitation Windows, visibles avec toutes les ruches réduites.

![Visualisation de toutes les ruches principales du Registre.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/reg_hives.png)

|Ruche|Abréviation|Objectif|
|---|---|---|
|`HKEY_CURRENT_USER`|`HKCU`|Stocke les paramètres de l'utilisateur actuellement connecté.|
|`HKEY_LOCAL_MACHINE`|`HKLM`|Stocke les paramètres matériels, logiciels et du système d'exploitation à l'échelle du système.|
|`HKEY_CLASSES_ROOT`|`HKCR`|Stocke les associations de fichiers et les informations d'enregistrement des applications.|
|`HKEY_USERS`|`HKU`|Contient les profils utilisateur actuellement chargés sur le système.|
|`HKEY_CURRENT_CONFIG`|`HKCC`|Contient des informations sur la configuration matérielle actuelle.|

Les deux ruches avec lesquelles nous interagissons le plus souvent sont `HKCU` et `HKLM`. Les modifications apportées sous `HKCU` n'affectent généralement que l'utilisateur actuel, tandis que les modifications apportées sous `HKLM` affectent généralement l'ensemble de l'ordinateur et nécessitent des privilèges administratifs pour être modifiées.

Les valeurs du Registre peuvent stocker plusieurs types de données. Voici quelques exemples courants :

|Type|Description|
|---|---|
|`REG_SZ`|Une chaîne de texte standard.|
|`REG_DWORD`|Un nombre de 32 bits, couramment utilisé pour les paramètres activés ou désactivés.|
|`REG_QWORD`|Un nombre de 64 bits.|
|`REG_MULTI_SZ`|Plusieurs chaînes de texte.|
|`REG_BINARY`|Données binaires brutes.|

---

## Éditeur du Registre

Windows inclut un outil graphique appelé `Éditeur du Registre` (Registry Editor), ou `regedit.exe`, qui peut être utilisé pour parcourir et modifier le Registre.

Nous pouvons ouvrir l'Éditeur du Registre en tapant `regedit` dans le menu Démarrer ou en appuyant sur `Win + R`, en entrant `regedit`, et en sélectionnant `OK`.

![Ouverture de l'Éditeur du Registre.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/reg_editor.png)

L'Éditeur du Registre est divisé en deux volets principaux : le volet de gauche affiche la hiérarchie du Registre, et le volet de droite affiche les valeurs contenues dans la clé sélectionnée. La barre d'adresse montre le chemin complet de la clé sélectionnée.

Nous pouvons développer les clés en utilisant les flèches dans le volet de gauche ou en collant un chemin de registre commençant par un nom de ruche dans la barre d'adresse.

### Création d'une clé de test

Avant de modifier un paramètre Windows existant, créons une clé de test sous le profil de l'utilisateur actuel.

Naviguez vers :

```text
HKEY_CURRENT_USER\Software
```

Faites un clic droit sur la clé `Software` et sélectionnez **Nouveau → Clé**. Nommez la nouvelle clé :

```text
HTB-Academy
```

Sélectionnez la nouvelle clé, faites un clic droit sur la zone vide dans le volet de droite, et sélectionnez **Nouveau → Valeur chaîne**. Nommez la valeur `CourseName`.

Double-cliquez sur `CourseName`, entrez les données suivantes, et sélectionnez `OK` :

```text
Windows Fundamentals
```

Créez une deuxième valeur en sélectionnant **Nouveau → Valeur DWORD (32 bits)**. Nommez-la `LabComplete`, puis double-cliquez dessus et définissez sa valeur à `1`.

![Création d'une clé d'exemple dans l'Éditeur du Registre.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/example_key.png)

Voici un enregistrement étape par étape de cet exercice :

![Création interactive d'une clé d'exemple dans l'Éditeur du Registre.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/practice_key.gif)

Nous pouvons modifier une valeur en double-cliquant dessus ou en faisant un clic droit pour faire apparaître un menu d'options. Les clés et les valeurs peuvent également être supprimées à l'aide de l'option `Supprimer`.

![Modification d'une clé dans l'Éditeur du Registre.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/modify_key.png)

L'Éditeur du Registre demande une confirmation avant de supprimer des données, mais il ne vérifie pas si Windows ou une autre application dépend de la clé sélectionnée, donc toute suppression doit être effectuée avec précaution.

## Interaction avec le Registre à l'aide de reg.exe

Windows inclut également l'utilitaire en ligne de commande `reg.exe`, qui peut être utilisé pour interroger et modifier le Registre depuis un terminal sur une machine Windows, dans des scripts ou des sessions d'administration à distance.

Nous pouvons voir ses opérations disponibles avec :

```cmd
C:\htb> reg /?  REG Operation [Parameter List]    Operation  [ QUERY
| ADD
| DELETE
| COPY    |                SAVE
| LOAD
| UNLOAD
| RESTORE |                COMPARE
| EXPORT
| IMPORT
| FLAGS ]  Return Code: (Except for REG COMPARE)    0 - Successful   1 - Failed  For help on a specific operation type:    REG Operation /?  Examples:    REG QUERY /?   REG ADD /?   REG DELETE /?   REG COPY /?   REG SAVE /?   REG RESTORE /?   REG LOAD /?   REG UNLOAD /?   REG COMPARE /?   REG EXPORT /?   REG IMPORT /?   REG FLAGS /?
```

Les opérations courantes incluent `query`, `add`, `delete`, `export` et `import`. Nous pouvons demander de l'aide pour une opération spécifique avec une commande telle que :

```cmd
C:\htb> reg query /?  REG QUERY KeyName [/v [ValueName] | /ve] [/s]           [/f Data [/k] [/d] [/c] [/e]] [/t Type] [/z] [/se Separator]           [/reg:32 | /reg:64]    KeyName  [\\Machine\]FullKey            Machine - Name of remote machine, omitting defaults to the                      current machine. Only HKLM and HKU are available on                      remote machines            FullKey - in the form of ROOTKEY\SubKey name                 ROOTKEY - [ HKLM
| HKCU
| HKCR
| HKU
| HKCC ]                 SubKey  - The full name of a registry key under the                           selected ROOTKEY    /v       Queries for a specific registry key values.            If omitted, all values for the key are queried.             Argument to this switch can be optional only when specified            along with /f switch. This specifies to search in valuenames only.    /ve      Queries for the default value or empty value name (Default).    /s       Queries all subkeys and values recursively (like dir /s).    /se      Specifies the separator (length of 1 character only) in            data string for REG_MULTI_SZ. Defaults to "\0" as the separator.    /f       Specifies the data or pattern to search for.            Use double quotes if a string contains spaces. Default is "*".    /k       Specifies to search in key names only.    /d       Specifies the search in data only.    /c       Specifies that the search is case sensitive.            The default search is case insensitive.    /e       Specifies to return only exact matches.            By default all the matches are returned.    /t       Specifies registry value data type.            Valid types are:              REG_SZ, REG_MULTI_SZ, REG_EXPAND_SZ,              REG_DWORD, REG_QWORD, REG_BINARY, REG_NONE            Defaults to all types.    /z       Verbose: Shows the numeric equivalent for the type of the valuename.    /reg:32  Specifies the key should be accessed using the 32-bit registry view.    /reg:64  Specifies the key should be accessed using the 64-bit registry view.  Examples:    REG QUERY HKLM\Software\Microsoft\ResKit /v Version     Displays the value of the registry value Version    REG QUERY \\ABC\HKLM\Software\Microsoft\ResKit\Nt\Setup /s     Displays all subkeys and values under the registry key Setup     on remote machine ABC    REG QUERY HKLM\Software\Microsoft\ResKit\Nt\Setup /se #     Displays all the subkeys and values with "#" as the seperator     for all valuenames whose type is REG_MULTI_SZ.    REG QUERY HKLM /f SYSTEM /t REG_SZ /c /e     Displays Key, Value and Data with case sensitive and exact     occurrences of "SYSTEM" under HKLM root for the data type REG_SZ    REG QUERY HKCU /f 0F /d /t REG_BINARY     Displays Key, Value and Data for the occurrences of "0F" in data     under HKCU root for the data type REG_BINARY    REG QUERY HKLM\SOFTWARE /ve     Displays Value and Data for the empty value (Default)     under HKLM\SOFTWARE
```

### Interrogation des données du Registre

La commande `reg query` affiche les valeurs et les sous-clés contenues dans une clé. Interrogeons la clé d'exemple `HTB-Academy` que nous avons créée précédemment.

```cmd
C:\htb> reg query "HKCU\Software\HTB-Academy"  HKEY_CURRENT_USER\Software\HTB-Academy     CourseName      REG_SZ       Windows Fundamentals     LabComplete     REG_DWORD    0x1
```

Pour récupérer une valeur spécifique, nous pouvons utiliser le paramètre `/v` :

```cmd
C:\htb> reg query "HKCU\Software\HTB-Academy" /v CourseName  HKEY_CURRENT_USER\Software\HTB-Academy     CourseName    REG_SZ    Windows Fundamentals
```

### Ajout et modification de valeurs

La commande `reg add` peut être utilisée pour créer une clé, créer une valeur ou modifier une valeur existante.

Quelques paramètres couramment utilisés sont :

|Paramètre|Objectif|
|---|---|
|`/v`|Spécifie le nom de la valeur.|
|`/t`|Spécifie le type de valeur.|
|`/d`|Spécifie les données à stocker.|
|`/f`|Exécute l'opération sans demander de confirmation.|

La commande suivante crée une nouvelle valeur de chaîne nommée `CreatedBy` :

```cmd
C:\htb> reg add "HKCU\Software\HTB-Academy" /v CreatedBy /t REG_SZ /d "reg.exe" /f  The operation completed successfully.
```

Nous pouvons également modifier la valeur DWORD existante pour la changer de `1` à `0`.

```cmd
C:\htb> reg add "HKCU\Software\HTB-Academy" /v LabComplete /t REG_DWORD /d 0 /f  The operation completed successfully.
```

Nous pouvons ensuite vérifier les deux changements en utilisant `reg query` :

```cmd
C:\htb> reg query "HKCU\Software\HTB-Academy"  HKEY_CURRENT_USER\Software\HTB-Academy     CourseName    REG_SZ    Windows Fundamentals     LabComplete    REG_DWORD    0x0     CreatedBy    REG_SZ    reg.exe
```

### Suppression de données du Registre

La commande `reg delete` peut supprimer une valeur individuelle ou une clé entière.

La commande suivante supprime uniquement la valeur `CreatedBy` :

```cmd
C:\htb> reg delete "HKCU\Software\HTB-Academy" /v CreatedBy /f  The operation completed successfully.
```

La commande suivante supprime la clé de test et toutes les valeurs qu'elle contient :

```cmd
C:\htb> reg delete "HKCU\Software\HTB-Academy" /f  The operation completed successfully.
```

Nous devons examiner attentivement le chemin avant d'utiliser `reg delete`, surtout lorsque l'option `/f` est incluse, car une erreur pourrait causer des dommages importants au système.

---

## Autorisations du Registre

Les clés du Registre ont des autorisations (permissions) qui déterminent quels utilisateurs et groupes peuvent les lire ou les modifier.

Un utilisateur standard peut généralement modifier les paramètres dans certaines parties de sa propre ruche `HKCU`. Les clés à l'échelle du système sous `HKLM` sont plus restreintes et nécessitent généralement une fenêtre de terminal ou une session de l'Éditeur du Registre avec élévation de privilèges.

Si le processus actuel n'a pas les autorisations suffisantes, Windows peut renvoyer une erreur `Accès refusé` (Access is denied) ou `L'opération demandée nécessite une élévation` (The requested operation requires elevation).

---

## Contrôle de Compte d'Utilisateur et le Registre

Le Contrôle de Compte d'Utilisateur (User Account Control), ou UAC, aide à empêcher les applications d'effectuer des modifications administratives sans approbation.

Windows stocke ses principales valeurs de politique UAC sous :

```text
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
```

Une valeur dans cette clé est `EnableLUA`. C'est une valeur `REG_DWORD` :

- `1` indique que l'UAC est activé.
- `0` indique que l'UAC est désactivé.

Nous pouvons interroger sa valeur actuelle sans apporter de modifications :

```cmd
C:\htb> reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA  HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System     EnableLUA    REG_DWORD    0x1
```

La modification de ce paramètre nécessite des privilèges administratifs et nécessite normalement un redémarrage avant que la modification complète ne prenne effet. La désactivation de l'UAC ne doit être effectuée que dans un environnement de laboratoire isolé, sauf en cas de nécessité absolue.
---

← [[04 - Autorisations NTFS vs autorisations de partage]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[06 - Services et Processus Windows]] →
