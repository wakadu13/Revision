---
tags:
  - windows
ordre: 10
---

# Windows Management Instrumentation (WMI)

---

WMI est un sous-système de PowerShell qui fournit aux administrateurs système des outils puissants pour la surveillance du système. L'objectif de WMI est de consolider la gestion des appareils et des applications sur les réseaux d'entreprise. WMI est un composant essentiel du système d'exploitation Windows et est préinstallé depuis Windows 2000. Il est composé des éléments suivants :

|**Nom du composant**|**Description**|
|:--|:--|
|Service WMI|Le processus Windows Management Instrumentation, qui s'exécute automatiquement au démarrage et sert d'intermédiaire entre les fournisseurs WMI, le référentiel WMI et les applications de gestion.|
|Objets gérés|Tout composant logique ou physique pouvant être géré par WMI.|
|Fournisseurs WMI|Objets qui surveillent les événements/données liés à un objet spécifique.|
|Classes|Celles-ci sont utilisées par les fournisseurs WMI pour transmettre des données au service WMI.|
|Méthodes|Celles-ci sont rattachées à des classes et permettent d'effectuer des actions. Par exemple, les méthodes peuvent être utilisées pour démarrer/arrêter des processus sur des machines distantes.|
|Référentiel WMI|Une base de données qui stocke toutes les données statiques relatives à WMI.|
|Gestionnaire d'objets CIM|Le système qui demande des données aux fournisseurs WMI et les renvoie à l'application qui les a demandées.|
|API WMI|Permet aux applications d'accéder à l'infrastructure WMI.|
|Consommateur WMI|Envoie des requêtes aux objets via le Gestionnaire d'objets CIM.|

Voici quelques-unes des utilisations de WMI :

- Informations sur l'état des systèmes locaux/distants
- Configuration des paramètres de sécurité sur les machines/applications distantes
- Définition et modification des autorisations des utilisateurs et des groupes
- Définition/modification des propriétés du système
- Exécution de code
- Planification de processus
- Mise en place de la journalisation

Ces tâches peuvent toutes être effectuées en utilisant une combinaison de PowerShell et de l'interface de ligne de commande WMI (WMIC). WMI peut être exécuté via l'invite de commande Windows en tapant `WMIC` pour ouvrir un shell interactif ou en exécutant directement une commande telle que `wmic computersystem get name` pour obtenir le nom d'hôte. Nous pouvons afficher une liste des commandes et des alias WMIC en tapant `WMIC /?`.

```cmd
C:\htb> wmic /?  WMIC is deprecated.  [global switches] <command>  The following global switches are available: /NAMESPACE           Path for the namespace the alias operate against. /ROLE                Path for the role containing the alias definitions. /NODE                Servers the alias will operate against. /IMPLEVEL            Client impersonation level. /AUTHLEVEL           Client authentication level. /LOCALE              Language id the client should use. /PRIVILEGES          Enable or disable all privileges. /TRACE               Outputs debugging information to stderr. /RECORD              Logs all input commands and output. /INTERACTIVE         Sets or resets the interactive mode. /FAILFAST            Sets or resets the FailFast mode. /USER                User to be used during the session. /PASSWORD            Password to be used for session login. /OUTPUT              Specifies the mode for output redirection. /APPEND              Specifies the mode for output redirection. /AGGREGATE           Sets or resets aggregate mode. /AUTHORITY           Specifies the <authority type> for the connection. /?[:<BRIEF|FULL>]    Usage information.  For more information on a specific global switch, type: switch-name /?  Press any key to continue, or press the ESCAPE key to stop
```

L'exemple de commande suivant liste les informations sur le système d'exploitation.

```cmd
C:\htb> wmic os list brief  BuildNumber  Organization  RegisteredUser  SerialNumber             SystemDirectory      Version 19041                      Owner           00123-00123-00123-AAOEM  C:\Windows\system32  10.0.19041
```

WMIC utilise des alias et des verbes, adverbes et commutateurs associés. L'exemple de commande ci-dessus utilise `LIST` pour afficher les données et l'adverbe `BRIEF` pour ne fournir que l'ensemble principal des propriétés. Une liste détaillée des verbes, commutateurs et adverbes est disponible [ici](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmic). WMI peut être utilisé avec PowerShell en utilisant le [module](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-wmiobject?view=powershell-5.1) `Get-WmiObject`. Ce module est utilisé pour obtenir des instances de classes WMI ou des informations sur les classes disponibles. Ce module peut être utilisé sur des machines locales ou distantes.

Ici, nous pouvons obtenir des informations sur le système d'exploitation.

```powershell
PS C:\htb> Get-WmiObject -Class Win32_OperatingSystem
| select SystemDirectory,BuildNumber,SerialNumber,Version
| ft  SystemDirectory     BuildNumber SerialNumber            Version ---------------     ----------- ------------            ------- C:\Windows\system32 19041       00123-00123-00123-AAOEM 10.0.19041
```

Nous pouvons également utiliser le [module](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/invoke-wmimethod?view=powershell-5.1) `Invoke-WmiMethod`, qui est utilisé pour appeler les méthodes des objets WMI. Un exemple simple est le renommage d'un fichier. Nous pouvons voir que la commande s'est terminée correctement car la `ReturnValue` est définie sur 0.

```powershell
PS C:\htb> Invoke-WmiMethod -Path "CIM_DataFile.Name='C:\users\public\spns.csv'" -Name Rename -ArgumentList "C:\Users\Public\kerberoasted_users.csv"   __GENUS          : 2 __CLASS          : __PARAMETERS __SUPERCLASS     : __DYNASTY        : __PARAMETERS __RELPATH        : __PROPERTY_COUNT : 1 __DERIVATION     : {} __SERVER         : __NAMESPACE      : __PATH           : ReturnValue      : 0 PSComputerName   :
```

Cette section fournit un bref aperçu de `WMI`, `WMIC` et de la combinaison de `WMIC` et `PowerShell`. `WMI` a une grande variété d'utilisations pour les opérateurs de la blue team et de la red team. Les sections suivantes de ce cours montreront certaines façons dont `WMI` peut être exploité de manière offensive pour l'énumération et le mouvement latéral.
---

← [[09 - Interagir avec le système d'exploitation Windows]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[11 - Microsoft Management Console (MMC)]] →
