# MCOT - Routage de paquets sur le réseau Internet

## Titre

Routage de paquets sur le réseau Internet

## Motivation

Le réseau Internet est une des pierres angulaires de notre monde moderne. Ce système de communication permet l'échange de données à une vitesse et à une intensité inégalées dans l'histoire. Il a permit l'émergence et le développement de nombreuses industries aujourd'hui essentielles dans nos vies et pour les entreprises.

## Encrage dans le thème

Des campagnes de vaccination et d'alerte contre les épidémies à l'intelligence artificielle Watson capable de compiler les données médicales de patients aux quatre coins du monde pour en tirer des corrélations insoupçonnées, le réseau Internet sous-jacent participe par sa fiabilité et sa rapidité à améliorer l'efficacité du système de santé.

## Bibliographie commentée

Le réseau Internet peut être modélisé comme un graphe où les sommets seraient l'ensemble des ordinateurs connectés au réseau et les arêtes les interconnexions entre les ordinateurs dudit réseau. Ces ordinateurs peuvent prendre des aspects et des caractéristiques très différents: serveurs, routeurs, ordinateurs de bureau, smartphones, montres connectées, station spatiale internationale, etc... mais on peut les catégoriser en général selon trois grandes catégories : serveurs, clients et routeurs. Les serveurs et clients se trouvent en général en bordure du réseau tandis que les routeurs sont en son coeur et assurent le transit des informations.[^Reseaux] [^Model]

Internet est un réseau de réseaux[^Reseaux]. C'est-à-dire que les ordinateurs sont connectés entre eux dans des réseaux plus petits eux-mêmes emboités dans des réseaux plus grands et ainsi de suite jusqu'à former le réseau Internet. Par exemple un ordinateur de maison appartient à son réseau domestique (le "wifi de la maison") mais également au système autonome (AS, Autonomous System) du fournisseur d'accès à Internet, qui est la portion du réseau confié au fournisseur et enfin l'Internet global qui est formé des connexions entre AS et dont les interconnexions sont entretenues par de grandes entreprises comme AT&T (backbone).

Un des aspects primordiaux du réseau Internet est sa topologie, id est l'agencement des noeuds du réseau les uns par rapport aux autres.
La topologie du réseau joue un rôle déterminant dans son efficacité, plus particulièrement sa robustesse et sa résilience contre les incidents. Les données transitent sur le réseau sous forme de "paquets" c'est-à-dire de suites finies de 1 et de 0[^Reseaux]. On veut donc pouvoir assurer le transfert de la majorité de ces paquets même lorsqu'un ou plusieurs noeuds deviennent inopérants. Ainsi un réseau centralisé autour d'un noeud est susceptible de tomber dès lors que le noeud central est déconnecté tandis qu'un réseau distribué, où chaque noeud communique avec un nombre similaire de noeuds, résistera bien mieux à une perte d'une partie du réseau.[^Backbone]
Déterminer la forme du réseau est en soi assez difficile à modéliser.[^Difficulty] Un des premiers modèles théoriques pertinent a été élaboré par Waxman et permet de modéliser en première approximation la structure hiérarchique d'Internet.

La définition de l'efficacité d'un réseau est toutefois complexe.
En 2021, Internet représenterait 3.3 zettabits[^5] de données transférées. Cela représente trois fois plus qu'en 2016. Les paquets doivent souvent être transférés avec des exigences contraignantes en matière de fiabilité, de rapidité, de stabilité et de bande passante, regroupés sous le terme de qualité de service (QoS, quality of service).
Chaque application n'a pas les mêmes exigences en terme de qualité de service mais le réseau doit pouvoir toutes les contenter.
De plus, une définition mathématique et systématique de la notion n'est pas aisée.[^RobustnessResilience] Malgré une compréhension intuitive du phénomène, il existe nombreux modèles qui permettent de déterminer des caractéristiques diverses.
Selon que l'on souhaite une grande résistance face à la perte de noeuds dans le réseau (maximisé par un graphe complet) ou bien qu'on s'autorise à pouvoir perdre une sous-partie du réseau afin de limiter le nombre d'interconnexions (tout en gardant une cohésion globale) comme dans un réseau décentralisé, les métriques à prendre en compte sont différentes.
Mais les considérations d'ordres technologiques, économiques ou commerciales jouent en réalité un rôle prépondérant dans le choix final de l'architecture.

Finalement, outre la question du choix de la topologie, celle du choix de protocole de routage a également un poids important sur le fonctionnement du réseau.
Le développement d'algorithmes et de protocoles comme BGP[^7] ou TCP/IP[^8] par la communauté Internet ainsi que la mise au point de nombreux algorithmes[^Reseaux] permettent également au réseau de supporter l'ensemble des applications utilisants Internet grâce à l'optimisation de l'allocation de ressources et de la topologie du réseau, la résolution automatique des problèmes de pannes ponctuelles, la mise en place de priorités, ou encore la modélisation et la gestion des congestions sur le réseau.

## Problématique

On comprend alors que comparer l'efficacité et la robustesse de plusieurs topologies de réseau peut permettre de significativement améliorer la rapidité et la fluidité du réseau et, in fine, des applications reposant sur son bon fonctionnement.

## Objectifs

Afin de donner des éléments de réponse à ce problème, je vais tenter de développer un environnement de simulation permettant de déterminer une mesure de l'efficacité et de la robustesse d'un réseau composé de serveurs, routeurs et clients. Ensuite, je tenterais de simuler le routage de paquets selon différents scénarii d'utilisation du réseau et pour différentes topologies de réseau.

## Positionnement thématique

Informatique - Informatique Théorique
Informatique - Informatique Pratique

## Mots-clés

### Français
- routage heuristique
- topologie de réseau
- simulation de réseau
- routage de paquets
- politique de routage

### Anglais
- heuritstic routing
- network topology
- network simulation
- packet routing
- routing policy

## Bibliographie

[^Difficulty]: S. Floyd and V. Paxson, "Difficulties in simulating the Internet", IEEE/ACM Transactions on Networking, vol. 9, no. 4, pp. 392-403, Aug. 2001, DOI: 10.1109/90.944338, <https://ieeexplore.ieee.org/document/944338>
[^Reseaux]: Andrew Tanenbaum, David Wetherall, "Réseaux", Pearson, 5e édition, 2011
[^Model]: K. L. Calvert, M. B. Doar and E. W. Zegura, "Modeling Internet topology", IEEE Communications Magazine, vol. 35, no. 6, pp. 160-163, June 1997, DOI 10.1109/35.587723, <https://ieeexplore.ieee.org/document/587723/>
[^Backbone]: Mitchell L. Moss, Anthony M. Townsend, "The Internet Backbone and the American Metropolis", The Information Society, 16:1, 35-47, 2000, DOI 10.1080/019722400128310, <https://www.tandfonline.com/doi/abs/10.1080/019722400128310>
[^RobustnessResilience]: Klau G.W., Weiskircher R., "Robustness and Resilience", In: Brandes U., Erlebach T. (eds) Network Analysis, Lecture Notes in Computer Science, vol 3418. Springer, Berlin, Heidelberg, 2005, DOI 10.1007/978-3-540-31955-9_15 <https://link.springer.com/chapter/10.1007%2F978-3-540-31955-9_15>
[^5]: Cisco, "Global 2021 Forecast Highlights", 2016
[^7]: Rekhter, Y. et P. Gross, "Application of the Border Gateway Protocol in the Internet", RFC 1772, DOI 10.17487/RFC1772, 1995, <https://www.rfc-editor.org/info/rfc1772>
[^8]: Postel, J., "Internet Protocol", STD 5, RFC 791, DOI 10.17487/RFC0791, 1981, <https://www.rfc-editor.org/info/rfc791>
