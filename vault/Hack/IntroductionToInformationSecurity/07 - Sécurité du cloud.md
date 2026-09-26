---
tags:
  - infosec
ordre: 7
---

# Sécurité du cloud

---

Imaginez que vous ayez des biens précieux que vous décidez de stocker dans une installation de stockage partagée et de haute technologie au lieu de les garder chez vous. Cette installation est comme « le cloud », un endroit où vous pouvez conserver vos objets et y accéder quand vous en avez besoin. Mais comme d'autres personnes utilisent également cette installation, vous devez prendre des mesures pour vous assurer que vos objets de valeur sont en sécurité et accessibles uniquement à vous. La sécurité du cloud est comme la combinaison de serrures, de caméras de sécurité et d'agents de sécurité dans l'installation de stockage qui protègent vos biens. Ce sont toutes les mesures prises pour protéger vos données et vos applications lorsqu'elles sont stockées dans le cloud, tout comme l'installation garde vos objets en sécurité.

![Schéma de réseau montrant les applications, les serveurs, le cloud, Internet et les connexions client. Inclut les employés, les appareils mobiles, l'entreprise et les équipes : Bleue, Rouge et Violette.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

À mesure que de plus en plus de personnes utilisent ces installations de stockage partagées (services cloud), il devient plus difficile de s'assurer que les biens (données) de chacun sont en sécurité. Les risques sont différents de ceux encourus en gardant les choses à la maison, car vous partagez l'espace et dépendez de la direction de l'installation pour certaines parties de la sécurité. Dans l'installation de stockage, vous et les propriétaires de l'installation avez tous deux un rôle à jouer pour assurer la sécurité de vos objets. L'installation fournit une sécurité globale, comme des gardes et des caméras de surveillance, mais vous, en tant qu'individu, êtes responsable du verrouillage de votre propre unité de stockage. C'est ce qu'on appelle le `shared responsibility model` (modèle de responsabilité partagée) dans le domaine de la sécurité du cloud. Le fournisseur de cloud sécurise le bâtiment (l'infrastructure), tandis que vous sécurisez votre propre unité (vos données et vos applications).

Dans cette installation de stockage partagée, plusieurs choses pourraient potentiellement compromettre la sécurité de vos biens. Par exemple, quelqu'un pourrait crocheter la serrure de votre unité et voler vos objets, ce qui est similaire à un `data breach` (violation de données) en sécurité du cloud, où des personnes non autorisées accèdent à vos informations sensibles. Le système d'accès de l'installation pourrait avoir des failles qui permettent à des personnes non autorisées d'entrer, similaires aux `insecure APIs` (API non sécurisées) dans les services cloud qui peuvent être exploitées par des pirates. Vous pourriez accidentellement oublier de bien verrouiller votre unité de stockage, la laissant ouverte à tous. Cela reflète le `misconfigured cloud storage` (stockage cloud mal configuré), où des paramètres incorrects exposent involontairement des données au public. De plus, quelqu'un pourrait voler votre carte d'accès ou votre code et se faire passer pour vous, ce qui mènerait à un `account hijacking` (détournement de compte) où des attaquants prennent le contrôle de votre compte et accèdent à vos données sans permission.

---

## Domaines clés de la sécurité du cloud

Pour se protéger contre ces menaces, la sécurité du cloud se concentre sur plusieurs domaines clés.

La `Data protection` (protection des données) implique des mesures telles que l'utilisation d'une serrure solide et peut-être même d'un coffre-fort à l'intérieur de votre unité, garantissant que vous seul pouvez accéder à vos objets de valeur. Cela se traduit par le chiffrement de vos données à la fois lorsqu'elles sont stockées (au repos) et lorsqu'elles sont déplacées (en transit), afin qu'elles soient sécurisées à tout moment.

L'`Identity and Access Management` (`IAM`) (gestion des identités et des accès) est un autre aspect crucial, garantissant que seules les personnes autorisées peuvent entrer dans votre unité de stockage. C'est comme avoir une clé personnalisée ou un code d'accès que vous seul connaissez, empêchant les autres d'accéder à votre espace.

La `Network security` (sécurité réseau) dans le cloud est comparable à des couloirs sécurisés et des entrées surveillées dans l'installation, empêchant les personnes non autorisées de se promener. Cela inclut les pare-feux (firewalls) et les réseaux privés virtuels (VPN) qui protègent les données lorsqu'elles se déplacent sur le réseau.

Enfin, la `compliance` (conformité) et la `governance` (gouvernance) impliquent le respect de règles que tout le monde doit suivre, comme ne pas stocker d'objets illégaux dans l'installation. En termes commerciaux, cela signifie suivre les lois et réglementations sur la manière dont les données sont traitées et sécurisées, en s'assurant que toutes les pratiques respectent les normes du secteur et les exigences légales.

---

## Responsabilité

La responsabilité de la sécurité dans cet environnement partagé est répartie entre différentes parties.

1. Les `Cloud service providers` (fournisseurs de services cloud) sont comme la direction de l'installation, ils s'assurent que le bâtiment est sécurisé, que les caméras de surveillance sont opérationnelles et que le personnel de sécurité est en service. Ils gèrent l'infrastructure de sécurité globale du cloud, offrant un environnement sûr pour tout le monde.
2. `You / Administrator` (Vous / Administrateur), le client, êtes responsable de la sécurisation de votre unité de stockage individuelle en la verrouillant correctement et en gardant votre clé ou votre code d'accès en sécurité. Dans un contexte professionnel, cela signifie mettre en œuvre des mots de passe forts, gérer l'accès des utilisateurs et protéger vos données au sein du cloud.
3. Les `Security teams` (équipes de sécurité) au sein des organisations planifient et supervisent ces mesures, un peu comme un chef de la sécurité de l'installation de stockage coordonnerait les protocoles de sûreté. Elles élaborent des stratégies, effectuent des évaluations des risques (risk assessments) et veillent à ce que les éléments techniques et humains de la sécurité soient traités efficacement.

S'assurer que ces mesures de sécurité sont efficaces nécessite des tests réguliers et de la vigilance. Tout comme vous pourriez engager quelqu'un pour tester la sécurité de l'installation en tentant de la percer (avec permission, bien sûr), les entreprises emploient des testeurs d'intrusion (penetration testers) pour évaluer la sécurité de leur cloud. Ces professionnels simulent des attaques pour identifier les faiblesses avant que des acteurs malveillants ne puissent les exploiter, contribuant ainsi à renforcer les défenses. Une gestion continue et une mise à jour constante sont cruciales, car de nouvelles menaces peuvent apparaître, comme quelqu'un qui inventerait un nouvel outil de crochetage.

Par conséquent, vous pourriez avoir besoin de remplacer les anciennes serrures et de mettre à jour périodiquement les mesures de sécurité. De même, la sécurité du cloud nécessite une attention et des mises à jour constantes pour se protéger contre les cybermenaces en constante évolution. Cela implique de corriger les vulnérabilités (patching vulnerabilities), de mettre à jour les protocoles de sécurité, de surveiller les activités suspectes et de former les utilisateurs aux meilleures pratiques. Le fournisseur de cloud et le client doivent tous deux être proactifs dans le maintien d'un environnement sécurisé, en travaillant ensemble pour garantir que toutes les protections sont à jour et efficaces.
---

← [[06 - Reprise après sinistre et continuité d'activité]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[08 - Sécurité physique]] →
