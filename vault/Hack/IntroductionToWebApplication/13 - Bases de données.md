---
tags:
  - web-applications
ordre: 13
---

# Bases de données

---

Les applications Web utilisent des [bases de données](https://en.wikipedia.org/wiki/Database) back-end pour stocker divers contenus et informations liés à l'application web. Il peut s'agir de ressources principales de l'application web comme des images et des fichiers, de contenu de l'application web comme des publications et des mises à jour, ou de données utilisateur comme les noms d'utilisateur et les mots de passe. Cela permet aux applications web de stocker et de récupérer des données facilement et rapidement, et d'activer un contenu dynamique qui est différent pour chaque utilisateur.

Il existe de nombreux types de bases de données, chacun correspondant à un certain type d'utilisation. La plupart des développeurs recherchent certaines caractéristiques dans une base de données, telles que la `vitesse` de stockage et de récupération des données, la `taille` lors du stockage de grandes quantités de données, l'`évolutivité` à mesure que l'application web se développe, et le `coût`.

---

## Relationnelles (SQL)

Les bases de données [relationnelles](https://en.wikipedia.org/wiki/Relational_database) (SQL) stockent leurs données dans des tableaux, des lignes et des colonnes. Chaque tableau peut avoir des clés uniques, qui peuvent lier les tableaux entre eux et créer des relations entre les tableaux.

Par exemple, nous pouvons avoir un tableau `users` dans une base de données relationnelle contenant des colonnes comme `id`, `username`, `first_name`, `last_name`, etc. L'`id` peut être utilisé comme clé du tableau. Un autre tableau, `posts`, peut contenir des publications faites par tous les utilisateurs, avec des colonnes comme `id`, `user_id`, `date`, `content`, etc.

![Schéma de base de données montrant la table 'users' avec les ID, noms d'utilisateur, prénoms et noms de famille, et la table 'posts' avec les ID de publication, ID d'utilisateur, dates et contenus.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/web_apps_relational_db.jpg)

Nous pouvons lier l'`id` du tableau `users` au `user_id` dans le tableau `posts` pour récupérer facilement les détails de l'utilisateur pour chaque publication, sans avoir à stocker tous les détails de l'utilisateur avec chaque publication.

Un tableau peut avoir plus d'une clé, car une autre colonne peut être utilisée comme clé pour se lier à un autre tableau. Par exemple, la colonne `id` peut être utilisée comme clé pour lier le tableau `posts` à un autre tableau contenant des commentaires, chacun appartenant à une certaine publication, et ainsi de suite.

La relation entre les tableaux au sein d'une base de données est appelée un schéma (Schema).

De cette manière, en utilisant des bases de données relationnelles, il devient très rapide et facile de récupérer toutes les données concernant un certain élément de toutes les bases de données. Par exemple, nous pouvons récupérer tous les détails liés à un certain utilisateur de tous les tableaux avec une seule requête. Cela rend les bases de données relationnelles très rapides et fiables pour les grands ensembles de données qui ont une structure et une conception claires. Les bases de données rendent également la gestion des données très efficace.

Certaines des bases de données relationnelles les plus courantes incluent :

|Type|Description|
|---|---|
|[MySQL](https://en.wikipedia.org/wiki/MySQL)|La base de données la plus couramment utilisée sur Internet. C'est une base de données open-source et son utilisation est entièrement gratuite|
|[MSSQL](https://en.wikipedia.org/wiki/Microsoft_SQL_Server)|L'implémentation d'une base de données relationnelle par Microsoft. Largement utilisée avec les serveurs Windows et les serveurs web IIS|
|[Oracle](https://en.wikipedia.org/wiki/Oracle_Database)|Une base de données très fiable pour les grandes entreprises, qui est fréquemment mise à jour avec des solutions de base de données innovantes pour la rendre plus rapide et plus fiable. Elle peut être coûteuse, même pour les grandes entreprises|
|[PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL)|Une autre base de données relationnelle gratuite et open-source. Elle est conçue pour être facilement extensible, permettant d'ajouter de nouvelles fonctionnalités avancées sans nécessiter de modification majeure de la conception initiale de la base de données|

D'autres bases de données SQL courantes incluent : `SQLite`, `MariaDB`, `Amazon Aurora`, et `Azure SQL`.

---

## Non relationnelles (NoSQL)

Une [base de données non relationnelle](https://en.wikipedia.org/wiki/NoSQL) n'utilise pas de tableaux, de lignes, de colonnes, de clés primaires, de relations ou de schémas. Au lieu de cela, une base de données `NoSQL` stocke les données en utilisant divers modèles de stockage, en fonction du type de données stockées.

En raison de l'absence de structure définie pour la base de données, les bases de données `NoSQL` sont très évolutives et flexibles. Lorsqu'on traite des ensembles de données qui ne sont pas très bien définis et structurés, une base de données `NoSQL` serait le meilleur choix pour stocker nos données.

Il existe 4 modèles de stockage courants pour les bases de données `NoSQL` :

- Clé-Valeur
- Orienté document
- Colonnes larges
- Graphe

Chacun des modèles ci-dessus a une manière différente de stocker les données. Par exemple, le modèle `Clé-Valeur` stocke généralement les données en `JSON` ou `XML`, et a une clé pour chaque paire, stockant toutes ses données comme sa valeur :

![Tableau de publications avec des ID, des dates et des contenus, montrant des paires clé-valeur](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/web_apps_non-relational_db.jpg)

L'exemple ci-dessus peut être représenté en utilisant `JSON` comme suit :

```json
{   "100001": {     "date": "01-01-2021",     "content": "Welcome to this web application."   },   "100002": {     "date": "02-01-2021",     "content": "This is the first post on this web app."   },   "100003": {     "date": "02-01-2021",     "content": "Reminder: Tomorrow is the ..."   } }
```

Cela ressemble à une paire dictionnaire/map/clé-valeur dans des langages comme `Python` ou `PHP` (c'est-à-dire `{'key':'value'}`), où la `clé` est généralement une chaîne de caractères, et la `valeur` peut être une chaîne de caractères, un dictionnaire, ou n'importe quel objet de classe.

Le modèle `Orienté document` stocke les données dans des objets `JSON` complexes et chaque objet a certaines métadonnées tout en stockant le reste des données de manière similaire au modèle `Clé-Valeur`.

Certaines des bases de données `NoSQL` les plus courantes incluent :

|Type|Description|
|---|---|
|[MongoDB](https://en.wikipedia.org/wiki/MongoDB)|La base de données `NoSQL` la plus courante. Elle est gratuite et open-source, utilise le modèle `Orienté document` et stocke les données dans des objets `JSON`|
|[ElasticSearch](https://en.wikipedia.org/wiki/Elasticsearch)|Une autre base de données `NoSQL` gratuite et open-source. Elle est optimisée pour le stockage et l'analyse d'énormes ensembles de données. Comme son nom l'indique, la recherche de données dans cette base de données est très rapide et efficace|
|[Apache Cassandra](https://en.wikipedia.org/wiki/Apache_Cassandra)|Également gratuite et open-source. Elle est très évolutive et est optimisée pour gérer avec élégance les valeurs défectueuses|

D'autres bases de données `NoSQL` courantes incluent : `Redis`, `Neo4j`, `CouchDB`, et `Amazon DynamoDB`.

---

## Utilisation dans les applications Web

La plupart des langages et frameworks de développement web modernes facilitent l'intégration, le stockage et la récupération de données à partir de divers types de bases de données. Mais d'abord, la base de données doit être installée et configurée sur le serveur back-end, et une fois qu'elle est opérationnelle, les applications web peuvent commencer à l'utiliser pour stocker et récupérer des données.

Par exemple, au sein d'une application web `PHP`, une fois que `MySQL` est opérationnel, nous pouvons nous connecter au serveur de base de données avec :

```php
$conn = new mysqli("localhost", "user", "pass");
```

Ensuite, nous pouvons créer une nouvelle base de données avec :

```php
$sql = "CREATE DATABASE database1"; $conn->query($sql)
```

Après cela, nous pouvons nous connecter à notre nouvelle base de données et commencer à utiliser la base de données `MySQL` via la syntaxe `MySQL`, directement dans `PHP`, comme suit :

```php
$conn = new mysqli("localhost", "user", "pass", "database1"); $query = "select * from table_1"; $result = $conn->query($query);
```

Les applications Web utilisent généralement l'entrée utilisateur lors de la récupération de données. Par exemple, lorsqu'un utilisateur utilise la fonction de recherche pour rechercher d'autres utilisateurs, son entrée de recherche est transmise à l'application web, qui utilise l'entrée pour rechercher dans la ou les bases de données.

```php
$searchInput =  $_POST['findUser']; $query = "select * from users where name like '%$searchInput%'"; $result = $conn->query($query);
```

Enfin, l'application web renvoie le résultat à l'utilisateur :

```php
while($row = $result->fetch_assoc() ){     echo $row["name"]."<br>"; }
```

Cet exemple de base nous montre à quel point il est facile d'utiliser les bases de données. Cependant, s'il n'est pas codé de manière sécurisée, le code de base de données peut entraîner une variété de problèmes, comme des vulnérabilités d'injection SQL (SQL Injection).
---

← [[12 - Serveurs Web]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[14 - Frameworks de Développement & APIs]] →
