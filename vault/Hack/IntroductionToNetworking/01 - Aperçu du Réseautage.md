---
tags:
  - networking
ordre: 1
---

# Aperçu du Réseautage

---

Un réseau permet à deux ordinateurs de communiquer entre eux. Il existe un large éventail de `topologies` (maillage/arbre/étoile), de `supports` (ethernet/fibre/coaxial/sans fil) et de `protocoles` (TCP/UDP/IPX) qui peuvent être utilisés pour faciliter le réseau. En tant que professionnels de la sécurité, il est important de comprendre le réseautage car lorsqu'un réseau tombe en panne, l'erreur peut être silencieuse, nous faisant manquer quelque chose.

Mettre en place un grand réseau plat n'est pas extrêmement difficile, et il peut s'agir d'un réseau fiable, du moins sur le plan opérationnel. Cependant, un réseau plat, c'est comme construire une maison sur un terrain et la considérer comme sécurisée parce qu'elle a une serrure sur la porte. En créant de nombreux réseaux plus petits et en les faisant communiquer, nous pouvons ajouter des couches de défense. Pivoter sur un réseau n'est pas difficile, mais le faire rapidement et silencieusement est ardu et ralentira les attaquants. Pour en revenir au scénario de la maison, examinons les exemples suivants :

#### Exemple N°1

Construire des réseaux plus petits et les entourer de listes de contrôle d'accès (Access Control Lists) c'est comme installer une clôture autour de la propriété qui crée des points d'entrée et de sortie spécifiques. Oui, un attaquant pourrait sauter par-dessus la clôture, mais cela semble suspect et n'est pas courant, ce qui permet de le détecter rapidement comme une activité malveillante. Pourquoi le réseau des imprimantes communique-t-il avec les serveurs via HTTP ?

#### Exemple N°2

Prendre le temps de cartographier et de documenter l'objectif de chaque réseau, c'est comme placer des lumières autour de la propriété, en s'assurant que toute activité peut être vue. Pourquoi le réseau des imprimantes communique-t-il avec Internet tout court ?

#### Exemple N°3

Avoir des buissons autour des fenêtres est un moyen de dissuasion pour les personnes qui tentent d'ouvrir la fenêtre. Tout comme les systèmes de détection d'intrusion (Intrusion Detection Systems) comme Suricata ou Snort sont un moyen de dissuasion contre l'exécution d'analyses de réseau. Pourquoi une analyse de ports (port scan) a-t-elle été lancée depuis le réseau des imprimantes ?

Ces exemples peuvent paraître absurdes, et il est de bon sens d'empêcher une imprimante de faire tout ce qui précède. Cependant, si l'imprimante se trouve sur un « réseau plat /24 » et obtient une adresse DHCP, il peut être difficile de lui imposer ce type de restrictions.

---

## C'est l'heure de l'anecdote - L'oubli d'un Pentester

La plupart des réseaux utilisent un sous-réseau `/24`, à tel point que de nombreux testeurs d'intrusion (Penetration Testers) définiront ce masque de sous-réseau (255.255.255.0) sans vérifier. Le réseau /24 permet aux ordinateurs de communiquer entre eux tant que les trois premiers octets d'une adresse IP sont identiques (ex : 192.168.1.xxx). Définir le masque de sous-réseau sur `/25` divise cette plage en deux, et l'ordinateur ne pourra communiquer qu'avec les ordinateurs de « sa moitié ». Nous avons vu des rapports de tests d'intrusion où l'évaluateur affirmait qu'un contrôleur de domaine (Domain Controller) était hors ligne alors qu'en réalité, il se trouvait simplement sur un réseau différent. La structure du réseau ressemblait à ceci :

- Passerelle serveur : 10.20.0.1/25
- Contrôleur de domaine : 10.20.0.10/25
- Passerelle client : 10.20.0.129/25
- Poste de travail client : 10.20.0.200/25
- IP du Pentester : 10.20.0.252/24 (Passerelle définie sur 10.20.0.1)

Le Pentester a communiqué avec les postes de travail clients et a pensé avoir fait un excellent travail car il a réussi à voler un mot de passe de poste de travail via Impacket. Cependant, en raison d'une mauvaise compréhension du réseau, il n'a jamais réussi à sortir du réseau client pour atteindre des cibles de plus « grande valeur » telles que les serveurs de bases de données. Espérons que, si cela vous semble confus, vous pourrez revenir sur cette affirmation à la fin du module et la comprendre !

---

## Informations de base

Examinons le schéma de haut niveau suivant sur le fonctionnement d'une configuration de télétravail (Work From Home).

![Diagramme montrant un réseau domestique avec un routeur connectant un smartphone, un ordinateur portable et un PC, et un réseau d'entreprise avec un routeur connectant un commutateur, un serveur web, un téléphone IP, une imprimante et deux hôtes clients. Les deux réseaux se connectent à un fournisseur d'accès à Internet (FAI), avec un serveur de noms de domaine (DNS) et un accès à Internet.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/net_overview.png)

---

L'ensemble d'Internet est basé sur de nombreux réseaux subdivisés, comme le montre l'exemple et marqués comme « `Réseau domestique` » et « `Réseau d'entreprise` ». On peut imaginer le `réseautage` comme la livraison de courrier ou de paquets envoyés par un ordinateur et reçus par un autre.

Imaginons comme scénario que nous voulons visiter le site web d'une entreprise depuis notre « `Réseau domestique` ». Dans ce cas, nous échangeons des données avec le site web de l'entreprise situé dans leur « `Réseau d'entreprise` ». Comme pour l'envoi de courrier ou de paquets, nous connaissons l'adresse où les paquets doivent aller. L'adresse du site web ou `Uniform Resource Locator` (`URL`) que nous saisissons dans notre navigateur est aussi appelée `Fully Qualified Domain Name` (`FQDN` ou nom de domaine pleinement qualifié).

La différence entre les `URL` et les `FQDN` est la suivante :

- un `FQDN` (`www.hackthebox.eu`) ne spécifie que l'adresse du « bâtiment » et
- une `URL` (`https://www.hackthebox.eu/example?floor=2&office=dev&employee=17`) spécifie également l'« `étage` », le « `bureau` », la « `boîte aux lettres` » et l'« `employé` » correspondant à qui le paquet est destiné.

Nous aborderons les représentations et définitions exactes de manière plus claire et précise dans d'autres sections.

Le fait est que nous connaissons l'adresse, mais pas l'emplacement géographique exact de l'adresse. Dans cette situation, le bureau de poste peut déterminer l'emplacement exact, qui transmet ensuite les paquets à l'endroit souhaité. Par conséquent, notre bureau de poste transmet nos paquets au bureau de poste principal, qui représente notre `Fournisseur d'Accès à Internet` (`FAI`).

Notre bureau de poste est notre `routeur` que nous utilisons pour nous connecter à « `Internet` » en réseautage.

Dès que nous envoyons notre paquet via notre bureau de poste (`routeur`), le paquet est transmis au `bureau de poste principal` (`FAI`). Ce bureau de poste principal consulte le `registre d'adresses`/`annuaire téléphonique` (`Domain Name Service` ou Service de Noms de Domaine) pour savoir où se trouve cette adresse et renvoie les coordonnées géographiques correspondantes (`adresse IP`). Maintenant que nous connaissons l'emplacement exact de l'adresse, notre paquet y est envoyé directement par un vol direct via notre bureau de poste principal.

Après que le serveur web a reçu notre paquet avec la demande de l'apparence de son site web, le serveur web nous renvoie le paquet avec les données pour la présentation du site web via le bureau de poste (`routeur`) du « `Réseau d'entreprise` » à l'adresse de retour spécifiée (`notre adresse IP`).

---

## Points supplémentaires

Dans ce diagramme, j'espère que le réseau d'entreprise présenté se compose de cinq réseaux distincts !

1. Le serveur Web devrait se trouver dans une DMZ (Zone Démilitarisée) car les clients sur Internet peuvent initier des communications avec le site web, ce qui le rend plus susceptible d'être compromis. Le placer dans un réseau distinct permet aux administrateurs de mettre en place des protections réseau entre le serveur web et les autres appareils.
2. Les postes de travail devraient être sur leur propre réseau, et dans un monde parfait, chaque poste de travail devrait avoir une règle de pare-feu basé sur l'hôte (Host-Based Firewall) l'empêchant de communiquer avec d'autres postes de travail. Si un poste de travail se trouve sur le même réseau qu'un serveur, les attaques réseau comme l'`usurpation` (`spoofing`) ou l'`attaque de l'homme du milieu` (`man in the middle`) deviennent un problème beaucoup plus important.
3. Le commutateur et le routeur devraient être sur un « réseau d'administration ». Cela empêche les postes de travail d'espionner toute communication entre ces appareils. J'ai souvent effectué un test d'intrusion et vu des annonces `OSPF` (Open Shortest Path First). Comme le routeur n'avait pas de `réseau de confiance`, n'importe qui sur le réseau interne aurait pu envoyer une annonce malveillante et effectuer une `attaque de l'homme du milieu` contre n'importe quel réseau.
4. Les téléphones IP devraient être sur leur propre réseau. Du point de vue de la sécurité, c'est pour empêcher les ordinateurs d'écouter clandestinement les communications. En plus de la sécurité, les téléphones sont uniques dans le sens où la latence/le décalage est significatif. Les placer sur leur propre réseau peut permettre aux administrateurs réseau de prioriser leur trafic pour prévenir plus facilement une latence élevée.
5. Les imprimantes devraient être sur leur propre réseau. Cela peut paraître étrange, mais il est quasiment impossible de sécuriser une imprimante. En raison du fonctionnement de Windows, si une imprimante indique à un ordinateur qu'une authentification est requise lors d'une tâche d'impression, cet ordinateur tentera une authentification `NTLMv2`, ce qui peut conduire au vol de mots de passe. De plus, ces appareils sont excellents pour la persistance et, en général, reçoivent des tonnes d'informations sensibles.

---

## Anecdote amusante

Pendant le COVID, j'ai été chargé de réaliser un `test d'intrusion physique` (`Physical Penetration Test`) à travers plusieurs états, et mon état était sous un ordre de `confinement` (`stay at home`). L'entreprise que je testais avait un personnel minimal au bureau. J'ai décidé d'acheter une imprimante coûteuse et je l'ai exploitée pour y placer un shell inversé (reverse shell), de sorte que lorsqu'elle se connecterait au réseau, elle m'enverrait un shell (accès à distance). J'ai ensuite expédié l'imprimante à l'entreprise et envoyé un e-mail de hameçonnage (phishing) remerciant le personnel d'être venu et expliquant que l'imprimante devrait leur permettre d'imprimer ou de numériser des choses plus rapidement s'ils voulaient ramener du matériel à la maison pour faire du télétravail pendant quelques jours. L'imprimante a été branchée presque instantanément, et l'ordinateur de leur administrateur de domaine a eu la gentillesse d'envoyer ses identifiants à l'imprimante !

Si le client avait conçu un réseau sécurisé, cette attaque n'aurait probablement pas été possible pour de nombreuses raisons :

- L'imprimante n'aurait pas dû pouvoir communiquer avec Internet
- Le poste de travail n'aurait pas dû pouvoir communiquer avec l'imprimante sur le port 445
- L'imprimante ne devrait pas pouvoir initier des connexions vers les postes de travail. Dans certains cas, les combinaisons imprimante/scanner devraient pouvoir communiquer avec un serveur de messagerie pour envoyer par e-mail des documents numérisés.
---

[[00 - Sommaire Introduction to Networking|Sommaire]] | [[02 - Types de réseaux]] →
