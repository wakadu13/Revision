---
tags:
  - linux
ordre: 23
---

# Conteneurisation

La conteneurisation (containerization) est le processus d'empaquetage et d'exécution d'applications dans des environnements isolés, généralement appelés conteneurs. Ces conteneurs fournissent des environnements légers et cohérents pour l'exécution des applications, garantissant qu'elles se comportent de la même manière, quel que soit l'endroit où elles sont déployées. Des technologies comme Docker, Docker Compose et Linux Containers (LXC) rendent la conteneurisation possible, principalement sur les systèmes basés sur Linux. Les conteneurs diffèrent des machines virtuelles en ce qu'ils partagent le noyau du système hôte, ce qui les rend beaucoup plus légers et efficaces. Avec ces technologies, les utilisateurs peuvent rapidement créer, déployer et gérer des applications avec une sécurité, une portabilité et une scalabilité améliorées.

Les conteneurs sont hautement configurables, permettant aux utilisateurs de les adapter à leurs besoins spécifiques, et leur nature légère facilite l'exécution simultanée de plusieurs conteneurs sur le même système hôte. Cette caractéristique est particulièrement avantageuse pour la mise à l'échelle des applications et la gestion d'architectures de microservices complexes.

Imaginez que vous organisez un grand concert et que chaque groupe a besoin de sa propre configuration de scène personnalisée. Au lieu de construire une scène entièrement nouvelle pour chaque groupe (ce qui reviendrait à utiliser une machine virtuelle), vous créez des « modules de scène » portables et autonomes qui incluent tout ce dont le groupe a besoin : lumières, instruments, haut-parleurs, etc. Ces modules sont légers, réutilisables et peuvent être facilement déplacés d'un lieu à l'autre. La clé est que les modules fonctionnent tous de manière transparente sur la même scène principale (le système hôte), mais chacun est suffisamment isolé pour que la configuration d'un groupe n'interfère pas avec celle des autres.

De la même manière, les conteneurs empaquettent une application avec tous ses outils et paramètres requis, lui permettant de s'exécuter de manière cohérente sur différents systèmes sans conflit, tout en partageant la même « scène principale » (les ressources du système sous-jacent).

La sécurité est un aspect critique de la conteneurisation. Les conteneurs isolent les applications du système hôte et les unes des autres, fournissant une barrière qui réduit le risque que des activités malveillantes n'affectent l'hôte ou d'autres conteneurs. Cette isolation, ainsi que des techniques de configuration et de durcissement (hardening) appropriées, ajoute une couche de sécurité supplémentaire. Cependant, il est important de noter que les conteneurs n'offrent pas le même niveau d'isolation que les machines virtuelles traditionnelles. S'ils ne sont pas correctement gérés, des vulnérabilités telles que l'élévation de privilèges (privilege escalation) ou les évasions de conteneur (container escapes) peuvent être exploitées pour obtenir un accès non autorisé au système hôte ou à d'autres conteneurs.

En plus d'une sécurité et d'une efficacité des ressources améliorées, les conteneurs rendent les applications plus faciles à déployer, à gérer et à mettre à l'échelle. Comme les conteneurs encapsulent tout ce dont l'application a besoin (par ex., bibliothèques, dépendances), ils permettent une cohérence entre les environnements de développement, de test et de production. Cette portabilité garantit que les applications s'exécutent de manière fiable dans différents environnements.

Cependant, il est important de reconnaître que, malgré leurs avantages, les conteneurs ne sont pas à l'abri des risques de sécurité. Il existe des méthodes que nous pouvons utiliser pour élever les privilèges ou échapper à l'isolation que les conteneurs fournissent.

---

## Dockers

Docker est une plateforme open source pour automatiser le déploiement d'applications en tant qu'unités autonomes appelées conteneurs. Il utilise un système de fichiers en couches (layered filesystem) et des fonctionnalités d'isolation des ressources pour offrir flexibilité et portabilité. De plus, il fournit un ensemble robuste d'outils pour créer, déployer et gérer des applications, ce qui aide à rationaliser le processus de conteneurisation.

Imaginez les conteneurs Docker comme une boîte à lunch scellée. Vous pouvez manger la nourriture (exécuter des applications) à l'intérieur, mais une fois que vous fermez la boîte (arrêtez le conteneur), tout se réinitialise. Pour fabriquer une nouvelle boîte à lunch (nouveau conteneur) avec un contenu mis à jour (configurations modifiées), vous créez une nouvelle recette (Dockerfile) basée sur l'original. Lorsque vous servez plusieurs boîtes à lunch dans un restaurant (production), vous utiliseriez un système de cuisine (Kubernetes/Docker Compose) pour gérer toutes les commandes en douceur.

### Installer Docker-Engine

L'installation de Docker est relativement simple. Nous pouvons utiliser le script suivant pour l'installer sur un hôte Ubuntu :

```bash
#!/bin/bash

# Preparation
sudo apt update -y
sudo apt install ca-certificates curl gnupg lsb-release -y
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update -y
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Add user htb-student to the Docker group
sudo usermod -aG docker htb-student
echo '[!] You need to log out and log back in for the group changes to take effect.'

# Test Docker installation
docker run hello-world
```

Le moteur Docker et des images Docker spécifiques sont nécessaires pour exécuter un conteneur. Celles-ci peuvent être obtenues sur le [Docker Hub](https://hub.docker.com/), un dépôt d'images préfabriquées, ou créées par l'utilisateur. Le Docker Hub est un registre (registry) basé sur le cloud pour les dépôts de logiciels ou une bibliothèque pour les images Docker. Il est divisé en une zone `public` et une zone `private`. La zone publique permet aux utilisateurs de téléverser et de partager des images avec la communauté. Elle contient également des images officielles de l'équipe de développement de Docker et de projets open source établis. Les images téléversées dans une zone privée du registre ne sont pas accessibles publiquement. Elles peuvent être partagées au sein d'une entreprise ou avec des équipes et des connaissances.

La création d'une image Docker se fait en créant un [Dockerfile](https://docs.docker.com/engine/reference/builder/), qui contient toutes les instructions dont le moteur Docker a besoin pour créer le conteneur. Nous pouvons utiliser des conteneurs Docker comme notre serveur d'« hébergement de fichiers » lors du transfert de fichiers spécifiques vers nos systèmes cibles. Par conséquent, nous devons créer un `Dockerfile` basé sur Ubuntu 22.04 avec un serveur `Apache` et `SSH` en cours d'exécution. Avec cela, nous pouvons utiliser `scp` pour transférer des fichiers vers l'image docker, et Apache nous permet d'héberger des fichiers et d'utiliser des outils comme `curl`, `wget`, et autres sur le système cible pour télécharger les fichiers requis. Un tel `Dockerfile` pourrait ressembler à ce qui suit :

### Dockerfile

```dockerfile
# Use the latest Ubuntu 22.04 LTS as the base image
FROM ubuntu:22.04

# Update the package repository and install the required packages
RUN apt-get update && \
    apt-get install -y \
        apache2 \
        openssh-server \
        && \
    rm -rf /var/lib/apt/lists/*

# Create a new user called "docker-user"
RUN useradd -m docker-user && \
    echo "docker-user:password" | chpasswd

# Give the docker-user user full access to the Apache and SSH services
RUN chown -R docker-user:docker-user /var/www/html && \
    chown -R docker-user:docker-user /var/run/apache2 && \
    chown -R docker-user:docker-user /var/log/apache2 && \
    chown -R docker-user:docker-user /var/lock/apache2 && \
    usermod -aG sudo docker-user && \
    echo "docker-user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Expose the required ports
EXPOSE 22 80

# Start the SSH and Apache services
CMD service ssh start && /usr/sbin/apache2ctl -D FOREGROUND
```

Après avoir défini notre Dockerfile, nous devons le convertir en une image. Avec la commande `build`, nous prenons le répertoire avec le Dockerfile, exécutons les étapes du `Dockerfile`, et stockons l'image dans notre moteur Docker local. Si l'une des étapes échoue à cause d'une erreur, la création du conteneur sera interrompue. Avec l'option `-t`, nous donnons à notre conteneur un tag, afin qu'il soit plus facile à identifier et à utiliser plus tard.

### Docker Build

```bash
Hiterof13@htb[/htb]$ docker build -t FS_docker .
```

Une fois l'image Docker créée, elle peut être exécutée via le moteur Docker, ce qui en fait un moyen très efficace et facile d'exécuter un conteneur. C'est similaire au concept de machine virtuelle, basé sur des images. Cependant, ces images sont des modèles en lecture seule et fournissent le système de fichiers nécessaire à l'exécution ainsi que tous les paramètres. Un conteneur peut être considéré comme un processus en cours d'exécution d'une image. Lorsqu'un conteneur doit être démarré sur un système, un paquet avec l'image respective est d'abord chargé s'il n'est pas disponible localement. Nous pouvons démarrer le conteneur avec la commande suivante [docker run](https://docs.docker.com/engine/reference/commandline/run/) :

### Docker Run - Syntaxe

```bash
Hiterof13@htb[/htb]$ docker run -p <host port>:<docker port> -d <docker container name>
```

### Docker Run

```bash
Hiterof13@htb[/htb]$ docker run -p 8022:22 -p 8080:80 -d FS_docker
```

Dans ce cas, nous démarrons un nouveau conteneur à partir de l'image `FS_docker` et mappons les ports hôtes 8022 et 8080 aux ports conteneur 22 et 80, respectivement. Le conteneur s'exécute en arrière-plan, nous permettant d'accéder aux services SSH et HTTP à l'intérieur du conteneur en utilisant les ports hôtes spécifiés.

### Gestion de Docker

Pour la gestion des conteneurs Docker, Docker fournit une suite complète d'outils qui nous permettent de créer, déployer et gérer facilement les conteneurs. Avec ces outils puissants, nous pouvons lister, démarrer et arrêter des conteneurs et les gérer efficacement, assurant une exécution transparente des applications. Certaines des commandes de gestion Docker les plus couramment utilisées sont :

|**Commande**|**Description**|
|---|---|
|`docker ps`|Lister tous les conteneurs en cours d'exécution|
|`docker stop`|Arrêter un conteneur en cours d'exécution.|
|`docker start`|Démarrer un conteneur arrêté.|
|`docker restart`|Redémarrer un conteneur en cours d'exécution.|
|`docker rm`|Supprimer un conteneur.|
|`docker rmi`|Supprimer une image Docker.|
|`docker logs`|Voir les journaux d'un conteneur.|

Il est important de noter que les commandes Docker peuvent être combinées avec diverses options pour ajouter des fonctionnalités supplémentaires. Par exemple, vous pouvez spécifier quels ports exposer, monter des volumes pour conserver des données, ou définir des variables d'environnement pour configurer vos conteneurs. Cette flexibilité vous permet de personnaliser vos conteneurs Docker pour répondre à des besoins et exigences spécifiques.

Lorsque vous travaillez avec des images Docker, il est crucial de comprendre que toute modification apportée à un conteneur en cours d'exécution basé sur une image n'est pas automatiquement sauvegardée dans l'image. Pour préserver ces modifications, vous devez créer une nouvelle image qui les inclut. Cela se fait en écrivant un nouveau Dockerfile, qui commence par l'instruction `FROM` (spécifiant l'image de base) et inclut ensuite les commandes nécessaires pour appliquer les modifications. Une fois le Dockerfile prêt, vous pouvez utiliser la commande `docker build` pour construire la nouvelle image et lui attribuer un tag unique pour l'identifier. Ce processus garantit que l'image originale reste inchangée, tandis que la nouvelle image reflète les mises à jour.

Il est également important de se rappeler que les conteneurs Docker sont sans état (stateless) par conception, ce qui signifie que toute modification effectuée à l'intérieur d'un conteneur en cours d'exécution (par exemple, la modification de fichiers) est perdue une fois le conteneur arrêté ou supprimé. Pour cette raison, il est préférable d'utiliser des volumes pour persister les données à l'extérieur du conteneur ou pour stocker l'état de l'application.

Dans les environnements de production, la gestion des conteneurs à grande échelle devient plus complexe. Des outils comme Docker Compose ou Kubernetes aident à orchestrer les conteneurs, vous permettant de gérer, de mettre à l'échelle et de lier plusieurs conteneurs efficacement.

---

## Linux Containers

Linux Containers (`LXC`) est une technologie de virtualisation légère qui permet à plusieurs systèmes Linux isolés (appelés conteneurs) de s'exécuter sur un seul hôte. LXC utilise des fonctionnalités clés d'isolation des ressources, telles que les groupes de contrôle (`cgroups`) et les `espaces de noms` (`namespaces`), pour garantir que chaque conteneur fonctionne de manière indépendante. Contrairement aux machines virtuelles traditionnelles, qui nécessitent un système d'exploitation complet pour chaque instance, les conteneurs partagent le noyau de l'hôte, ce qui rend LXC plus efficace en termes d'utilisation des ressources.

LXC fournit un ensemble complet d'outils et d'API pour la gestion et la configuration des conteneurs, ce qui en fait un choix populaire pour la conteneurisation sur les systèmes Linux. Cependant, bien que LXC et Docker soient tous deux des technologies de conteneurisation, ils servent des objectifs différents et ont des caractéristiques uniques.

Docker s'appuie sur l'idée de la conteneurisation en y ajoutant la facilité d'utilisation et la portabilité, ce qui l'a rendu très populaire dans le monde du DevOps. Docker met l'accent sur l'empaquetage des applications avec toutes leurs dépendances dans une « image » portable, leur permettant d'être facilement déployées dans différents environnements. Cependant, il existe quelques différences entre les deux qui peuvent être distinguées en fonction des catégories suivantes :

|**Catégorie**|**Description**|
|---|---|
|`Approche`|LXC est souvent considéré comme un outil de conteneurisation plus traditionnel au niveau du système, se concentrant sur la création d'environnements Linux isolés qui se comportent comme des machines virtuelles légères. Docker, d'autre part, est axé sur l'application, ce qui signifie qu'il est optimisé pour l'empaquetage et le déploiement d'applications uniques ou de microservices.|
|`Création d'image`|Docker utilise un format d'image standardisé (images Docker) qui inclut tout le nécessaire pour exécuter une application (code, bibliothèques, configurations). LXC, bien que capable de fonctionnalités similaires, nécessite généralement plus de configuration manuelle pour la création et la gestion des environnements.|
|`Portabilité`|Docker excelle en matière de portabilité. Ses images de conteneurs peuvent être facilement partagées entre différents systèmes via Docker Hub ou d'autres registres. Les environnements LXC sont moins portables dans ce sens, car ils sont plus étroitement intégrés à la configuration du système hôte.|
|`Facilité d'utilisation`|Docker est conçu avec la simplicité à l'esprit, offrant une CLI conviviale et un soutien communautaire étendu. LXC, bien que puissant, peut nécessiter une connaissance plus approfondie de l'administration système Linux, ce qui le rend moins simple pour les débutants.|
|`Sécurité`|Les conteneurs Docker sont généralement plus sécurisés dès le départ, grâce à des couches d'isolation supplémentaires comme AppArmor et SELinux, ainsi qu'à sa fonctionnalité de système de fichiers en lecture seule. Les conteneurs LXC, bien que sécurisés, peuvent nécessiter des configurations supplémentaires pour atteindre le niveau d'isolation que Docker offre par défaut. Fait intéressant, lorsqu'ils sont mal configurés, Docker et LXC peuvent tous deux présenter un vecteur pour l'élévation de privilèges locale (ces techniques sont traitées en profondeur dans notre [module Linux Local Privilege Escalation](https://academy.hackthebox.com/module/details/51).|

Dans LXC, les images sont construites manuellement en créant un système de fichiers racine (root filesystem) et en installant les paquets et configurations nécessaires. Ces conteneurs sont liés au système hôte, peuvent ne pas être facilement portables et peuvent nécessiter une expertise technique plus importante pour être configurés et gérés.

D'un autre côté, Docker est une plateforme centrée sur l'application qui s'appuie sur LXC et fournit une interface plus conviviale pour la conteneurisation. Ses images sont construites à l'aide d'un Dockerfile, qui spécifie l'image de base et les étapes requises pour construire l'image. Ces images sont conçues pour être portables afin de pouvoir être facilement déplacées d'un environnement à un autre.

Pour installer LXC sur une distribution Linux, nous pouvons utiliser le gestionnaire de paquets de la distribution. Par exemple, sur Ubuntu, nous pouvons utiliser le gestionnaire de paquets `apt` pour installer LXC avec la commande suivante :

### Installer LXC

```bash
Hiterof13@htb[/htb]$ sudo apt install lxc -y
```

Une fois LXC installé, nous pouvons commencer à créer et à gérer des conteneurs sur l'hôte Linux. Il convient de noter que LXC nécessite que le noyau Linux prenne en charge les fonctionnalités nécessaires à la conteneurisation. La plupart des noyaux Linux modernes ont un support intégré pour la conteneurisation, mais certains noyaux plus anciens peuvent nécessiter une configuration ou un patch supplémentaire pour activer le support de LXC.

### Créer un conteneur LXC

Pour créer un nouveau conteneur LXC, nous pouvons utiliser la commande `lxc-create` suivie du nom du conteneur et du modèle à utiliser. Par exemple, pour créer un nouveau conteneur Ubuntu nommé `linuxcontainer`, nous pouvons utiliser la commande suivante :

```bash
Hiterof13@htb[/htb]$ sudo lxc-create -n linuxcontainer -t ubuntu
```

### Gérer les conteneurs LXC

Lorsque l'on travaille avec des conteneurs LXC, plusieurs tâches sont impliquées dans leur gestion. Ces tâches incluent la création de nouveaux conteneurs, la configuration de leurs paramètres, leur démarrage et leur arrêt selon les besoins, et la surveillance de leurs performances. Heureusement, de nombreux outils en ligne de commande et fichiers de configuration sont disponibles pour aider à ces tâches. Ces outils nous permettent de gérer rapidement et facilement nos conteneurs, en veillant à ce qu'ils soient optimisés pour nos besoins et exigences spécifiques. En exploitant efficacement ces outils, nous pouvons nous assurer que nos conteneurs LXC fonctionnent de manière efficace et efficiente, nous permettant de maximiser les performances et les capacités de notre système.

Les paramètres de réseau, de stockage et de sécurité ne sont pas gérés avec `lxc-config`. Cette commande ne fait qu'interroger les paramètres système globaux de LXC (par exemple `lxc.lxcpath`). Les paramètres par conteneur se trouvent dans le fichier de configuration du conteneur, généralement `/var/lib/lxc/<container>/config` pour les conteneurs privilégiés, et sont documentés dans `lxc.container.conf(5)`. Ne confondez pas les outils LXC classiques (`lxc-start`, `lxc-attach`) avec le client `lxc config` de LXD, qui utilise des espaces comme séparateurs.

|Commande|Description|
|---|---|
|`lxc-ls`|Lister tous les conteneurs existants|
|`lxc-info -n <container>`|Afficher l'état du conteneur, le PID, les adresses IP et les statistiques de ressources|
|`lxc-stop -n <container>`|Arrêter un conteneur en cours d'exécution.|
|`lxc-start -n <container>`|Démarrer un conteneur arrêté.|
|`lxc-stop -r -n <container>`|Redémarrer un conteneur en cours d'exécution.|
|`lxc-cgroup -n <container> <key> [value]`|Obtenir ou définir une valeur cgroup en direct pour un conteneur en cours d'exécution|
|`lxc-attach -n <container>`|Exécuter un shell ou une commande à l'intérieur d'un conteneur en cours d'exécution.|
|`lxc-attach -n <container> -f /path/to/config`|S'attacher en utilisant un fichier de configuration personnalisé (`--rcfile`), et non un chemin partagé de l'hôte.|
|`lxc-console -n <container>`|S'attacher à la console du conteneur.|

`lxc-config` ne peut lister ou afficher que les clés globales :

```bash
Hiterof13@htb[/htb]$ lxc-config -l
Hiterof13@htb[/htb]$ lxc-config lxc.lxcpath
```

Pour inspecter ou modifier les paramètres réseau d'un conteneur, modifiez des clés telles que `lxc.net.0.type`, `lxc.net.0.link`, et `lxc.net.0.flags` dans le fichier `config` de ce conteneur, puis redémarrez le conteneur. Vous pouvez également afficher une seule clé ou les adresses IP assignées :

```bash
Hiterof13@htb[/htb]$ sudo lxc-info -n linuxcontainer -i
Hiterof13@htb[/htb]$ sudo lxc-info -n linuxcontainer -c lxc.net.0.veth.pair
```

Pour partager un répertoire ou un fichier de l'hôte avec un conteneur, ajoutez un montage par lien (bind mount) dans la configuration du conteneur plutôt que de passer un chemin à `lxc-attach` :

```text
lxc.mount.entry = /path/on/host path/in/container none bind,create=dir 0 0
```

Après avoir ajouté l'entrée, redémarrez le conteneur pour que le montage soit appliqué.

En tant que testeurs d'intrusion, nous sommes souvent confrontés à des situations où nous devons tester des logiciels ou des systèmes qui ont des dépendances complexes ou des configurations difficiles à reproduire sur nos machines locales. C'est là que les conteneurs Linux deviennent extrêmement utiles. Un conteneur Linux est un paquet léger et autonome qui inclut tout le nécessaire pour exécuter un logiciel spécifique, comme le code, les bibliothèques et les fichiers de configuration. Les conteneurs offrent un environnement isolé, permettant au logiciel de s'exécuter de manière cohérente sur n'importe quelle machine Linux, quelle que soit la configuration du système hôte.

Les conteneurs sont particulièrement utiles car ils nous permettent de créer et d'exécuter rapidement des environnements isolés adaptés à nos besoins de test spécifiques. Par exemple, si nous devons tester une application web qui dépend d'une version particulière d'une base de données ou d'un serveur web, nous pouvons créer un conteneur avec les versions et configurations exactes dont nous avons besoin. Cela élimine les tracas de la configuration manuelle de ces composants sur notre machine, ce qui peut être long et sujet aux erreurs.

Nous pouvons également les utiliser pour tester des exploits ou des malwares dans un environnement contrôlé où nous créons un conteneur qui simule un système ou un réseau vulnérable, puis utilisons ce conteneur pour tester en toute sécurité des exploits sans risquer d'endommager nos machines ou nos réseaux. Cependant, il est important de configurer la sécurité des conteneurs LXC pour empêcher tout accès non autorisé ou toute activité malveillante à l'intérieur du conteneur. Cela peut être réalisé en mettant en œuvre plusieurs mesures de sécurité, telles que :

- Restreindre l'accès au conteneur
- Limiter les ressources
- Isoler le conteneur de l'hôte
- Appliquer un contrôle d'accès obligatoire (mandatory access control)
- Maintenir le conteneur à jour

Les conteneurs LXC sont accessibles par diverses méthodes, telles que SSH ou la console. Il est recommandé de restreindre l'accès au conteneur en désactivant les services inutiles, en utilisant des protocoles sécurisés et en appliquant des mécanismes d'authentification forts. Par exemple, nous pouvons désactiver l'accès SSH au conteneur en supprimant le paquet `openssh-server` ou en configurant SSH pour n'autoriser l'accès qu'à partir d'adresses IP de confiance. Ces conteneurs partagent également le même noyau que le système hôte, ce qui signifie qu'ils peuvent accéder à toutes les ressources disponibles sur le système. Nous pouvons utiliser des limites de ressources ou des quotas pour empêcher les conteneurs de consommer des ressources excessives. Par exemple, nous pouvons utiliser les `cgroups` pour limiter la quantité de CPU, de mémoire ou d'espace disque qu'un conteneur peut utiliser.

### Sécuriser LXC

Limitons les ressources du conteneur. Pour configurer les `cgroups` pour LXC et limiter le CPU et la mémoire, modifiez le fichier de configuration propre au conteneur. Les conteneurs privilégiés stockent ce fichier à l'emplacement `/var/lib/lxc/<container name>/config`. Le répertoire `/usr/share/lxc/config/` ne contient que des modèles partagés tels que `common.conf` ; ce n'est pas l'endroit pour ajouter des limites par conteneur. Par exemple, pour modifier la configuration d'un conteneur nommé `linuxcontainer`, nous pouvons utiliser la commande suivante :

```bash
Hiterof13@htb[/htb]$ sudo vim /var/lib/lxc/linuxcontainer/config
```

Dans ce fichier de configuration, nous pouvons ajouter les lignes suivantes pour limiter le CPU et la mémoire que le conteneur peut utiliser.

```text
lxc.cgroup.cpu.shares = 512
lxc.cgroup.memory.limit_in_bytes = 512M
```

Lorsque vous travaillez avec des conteneurs, il est important de comprendre le paramètre `lxc.cgroup.cpu.shares`. Ce paramètre détermine le temps CPU qu'un conteneur peut utiliser par rapport aux autres conteneurs sur le système. Par défaut, cette valeur est fixée à 1024, ce qui signifie que le conteneur peut utiliser jusqu'à sa juste part de temps CPU. Cependant, si nous fixons cette valeur à 512, par exemple, le conteneur ne peut utiliser que la moitié du temps CPU disponible sur le système. Cela peut être un moyen utile de gérer les ressources et de s'assurer que tous les conteneurs ont l'accès nécessaire au temps CPU.

L'un des paramètres clés pour contrôler l'allocation des ressources d'un conteneur est le paramètre `lxc.cgroup.memory.limit_in_bytes`. Ce paramètre vous permet de définir la quantité maximale de mémoire qu'un conteneur peut utiliser. Il est important de noter que cette valeur peut être spécifiée dans diverses unités, y compris les octets, les kilo-octets (K), les méga-octets (M), les giga-octets (G) ou les téra-octets (T), permettant un haut degré de granularité dans la définition des limites de ressources du conteneur. Après avoir ajouté ces deux lignes, nous pouvons enregistrer et fermer le fichier en tapant :

- `[Esc]`
- `:`
- `wq`

Pour appliquer ces changements, redémarrez le conteneur afin qu'il recharge sa configuration. Le redémarrage du service `lxc` n'est pas nécessaire pour le fichier `config` d'un seul conteneur.

```bash
Hiterof13@htb[/htb]$ sudo lxc-stop -n linuxcontainer
Hiterof13@htb[/htb]$ sudo lxc-start -n linuxcontainer
```

Si le conteneur est déjà en cours d'exécution et que nous n'avons besoin que d'une limite temporaire, `lxc-cgroup` peut définir les mêmes valeurs en direct :

```bash
Hiterof13@htb[/htb]$ sudo lxc-cgroup -n linuxcontainer cpu.shares 512
Hiterof13@htb[/htb]$ sudo lxc-cgroup -n linuxcontainer memory.limit_in_bytes 512M
```

LXC utilise les `espaces de noms` (`namespaces`) pour fournir un environnement isolé pour les processus, les réseaux et les systèmes de fichiers par rapport au système hôte. Les espaces de noms sont une fonctionnalité du noyau Linux qui permet de créer des environnements isolés en fournissant une abstraction des ressources système.

Les espaces de noms sont un aspect crucial de la conteneurisation car ils fournissent un haut degré d'isolation pour les processus du conteneur, les interfaces réseau, les tables de routage et les règles de pare-feu. Chaque conteneur se voit attribuer un espace de numéros d'ID de processus (`pid`) unique, isolé des ID de processus du système hôte. Cela garantit que les processus du conteneur ne peuvent pas interférer avec les processus du système hôte, améliorant ainsi la stabilité et la fiabilité du système. De plus, chaque conteneur possède ses propres interfaces réseau (`net`), tables de routage et règles de pare-feu, qui sont complètement séparées des interfaces réseau du système hôte. Toute activité liée au réseau à l'intérieur du conteneur est isolée du réseau du système hôte, offrant une couche supplémentaire de sécurité réseau.

De plus, les conteneurs sont livrés avec leur propre système de fichiers racine (`mnt`), qui est entièrement différent du système de fichiers racine du système hôte. Cette séparation entre les deux garantit que toute modification apportée au système de fichiers du conteneur n'affecte pas le système de fichiers du système hôte. Cependant, il est important de se rappeler que si les espaces de noms offrent un haut niveau d'isolation, ils ne fournissent pas une sécurité complète. Par conséquent, il est toujours conseillé de mettre en œuvre des mesures de sécurité supplémentaires pour protéger davantage le conteneur et le système hôte contre d'éventuelles failles de sécurité.

Voici 9 exercices optionnels pour pratiquer LXC :

|||
|---|---|
|1|Installez LXC sur votre machine et créez votre premier conteneur.|
|2|Configurez les paramètres réseau de votre conteneur LXC en modifiant les clés `lxc.net.0.*` dans `/var/lib/lxc/<container>/config`.|
|3|Créez une image LXC personnalisée et utilisez-la pour lancer un nouveau conteneur.|
|4|Configurez les limites de ressources pour vos conteneurs LXC (CPU, mémoire, espace disque).|
|5|Explorez les commandes `lxc-*` pour la gestion des conteneurs.|
|6|Utilisez LXC pour créer un conteneur exécutant une version spécifique d'un serveur web (par ex., Apache, Nginx).|
|7|Configurez l'accès SSH à vos conteneurs LXC et connectez-vous à eux à distance.|
|8|Créez un conteneur avec persistance, afin que les modifications apportées au conteneur soient sauvegardées et puissent être réutilisées.|
|9|Utilisez LXC pour tester des logiciels dans un environnement contrôlé, comme une application web vulnérable ou un malware.|

---

← [[22 - Gestion des systèmes de fichiers]] | [[00 - Sommaire Linux|Sommaire]] | [[24 - Configuration du Réseau]] →
