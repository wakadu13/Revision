---
tags:
  - infosec
ordre: 10
---

# Sécurité de l'Internet des objets

---

L'`Internet des objets`, ou `IoT` (Internet of Things), désigne le réseau d'objets du quotidien connectés à Internet, leur permettant d'envoyer et de recevoir des données. Cela inclut tout, des appareils domestiques intelligents aux bracelets de fitness connectés, en passant par les capteurs industriels et même les voitures connectées. À mesure que ces appareils s'intègrent davantage dans notre vie quotidienne, il devient essentiel de les sécuriser pour protéger nos informations personnelles et garantir leur bon fonctionnement.

Imaginez que votre maison soit remplie d'appareils intelligents : un thermostat qui règle la température en fonction de vos préférences, des lumières qui s'allument lorsque vous entrez dans une pièce, un réfrigérateur qui vous prévient lorsque vous n'avez plus de lait, et même une serrure de porte que vous pouvez contrôler depuis votre smartphone. Ces appareils rendent la vie plus pratique, mais ils introduisent également de nouvelles façons pour des invités indésirables d'entrer dans votre maison, non pas par les portes ou les fenêtres, mais par des voies numériques invisibles. La sécurité de l'IoT, c'est comme ajouter des serrures, des alarmes et des protections à ces portes numériques pour protéger votre maison des intrus.

La sécurité de l'IoT est la pratique qui consiste à protéger ces appareils interconnectés et les réseaux sur lesquels ils fonctionnent contre les accès non autorisés, le vol de données (data theft) et d'autres cybermenaces. Elle implique une combinaison de stratégies et de technologies conçues pour protéger les appareils eux-mêmes, les données qu'ils traitent et les canaux de communication qu'ils utilisent.

Contrairement aux ordinateurs traditionnels, de nombreux appareils IoT ont une puissance de traitement et une mémoire limitées. Il est donc difficile de mettre en œuvre des fonctionnalités de sécurité avancées sans affecter leurs performances. De plus, ces appareils sont souvent déployés en grand nombre dans divers environnements, ce qui augmente les chances que l'un d'entre eux soit compromis. Par exemple, imaginez qu'un thermostat intelligent de votre maison soit piraté. Cela peut sembler anodin, mais par le biais de ce thermostat, un cybercriminel pourrait, dans le pire des cas, accéder à l'ensemble de votre réseau domestique, y compris aux fichiers personnels de votre ordinateur ou aux informations sensibles transmises sur le réseau. Dans les environnements industriels, le piratage d'appareils IoT contrôlant des machines pourrait entraîner des perturbations importantes, voire des dommages physiques.

---

## Responsabilité

La gestion globale de la sécurité de l'IoT relève généralement de l'équipe de sécurité de l'information d'une organisation, dirigée par des responsables tels que le Responsable de la sécurité des systèmes d'information (RSSI) (Chief Information Security Officer ou CISO) ou un responsable dédié à la sécurité de l'IoT. Mais la sécurisation de l'écosystème IoT est une responsabilité partagée et implique plusieurs autres acteurs clés :

|**Acteur**|**Responsabilité**|
|---|---|
|`Device Manufacturers`|Ils sont comme les architectes et les constructeurs du château. C'est à eux qu'il incombe de concevoir des appareils en tenant compte de la sécurité dès le départ. Cela inclut le respect des principes de conception sécurisée, comme la réduction au minimum des fonctionnalités inutiles qui pourraient introduire des vulnérabilités, et la fourniture de mises à jour de sécurité en temps opportun pour faire face aux nouvelles menaces.|
|`Network Administrators`|Ces personnes sont comme les gardes qui patrouillent sur les murs du château et surveillent les allées et venues. Ils sécurisent les réseaux auxquels les appareils IoT se connectent, en mettant en œuvre des mesures telles que la segmentation du réseau (network segmentation) — qui consiste à créer différentes sections au sein du château pour contenir toute brèche — et des systèmes de détection d'intrusion (intrusion detection systems) qui les alertent en cas d'activités suspectes.|
|`Application Developers`|Ce sont les scribes et les érudits, qui veillent à ce que les logiciels interagissant avec les appareils IoT soient sécurisés. Ils mettent en œuvre des méthodes d'authentification appropriées, afin que seuls les utilisateurs de confiance puissent accéder aux applications, et ils protègent les données par le biais du chiffrement (encryption) et d'autres mesures de sécurité.|

Prenons le cas d'une grande chaîne de vente au détail qui a installé des systèmes CVC (chauffage, ventilation et climatisation) intelligents dans ses magasins pour améliorer l'efficacité énergétique. Ces systèmes étaient connectés à Internet pour la surveillance et le contrôle à distance. Cependant, les appareils ne disposaient pas de mesures de sécurité adéquates. Des pirates ont exploité cette vulnérabilité pour accéder au réseau de l'entreprise, dérobant au final les données de cartes de crédit de millions de clients.

À mesure que le paysage de l'IoT continue de s'étendre, les défis liés à sa sécurisation se multiplient également. De nouveaux types d'appareils sont constamment introduits, chacun avec ses propres vulnérabilités. Les cybercriminels deviennent de plus en plus sophistiqués, trouvant des moyens innovants pour exploiter les faiblesses des systèmes IoT.
---

← [[09 - Sécurité Mobile]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[11 - Déni de service distribué]] →
