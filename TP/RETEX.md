# Retour d'Expérience - TP Techniques de Test 2025/2026

Ce TP m'a fait découvrir l'importance des tests dans le développement logiciel. L'approche TDD était très formatrice pour moi.

J'ai trouvé que mon plan initial était bien structuré avec une séparation claire entre tests unitaires, d'intégration et de performance. Cette organisation m'a facilité le développement.

Cependant, la réalité était différente de ce que j'avais imaginé. L'implémentation de l'algorithme de triangulation Delaunay était plus complexe que prévu, et j'ai dû utiliser scipy.spatial.Delaunay au lieu d'une implémentation from scratch afin d'avoir une fonctionnalité fonctionnel.

Au cours du développement, j'ai dû ajouter ou modifier de nombreux tests :
- Tests supplémentaires pour gérer des cas d'erreur oubliés (points colinéaires)
- Adaptation des tests de performance selon les vraies capacités de l'algorithme
- Tests d'intégration plus poussés pour la communication inter-services

Certains tests que j'avais prévus se sont révélés moins pertinents, tandis que d'autres aspects ont nécessité plus de couverture que je ne l'avais anticipé.

Cette expérience m'a montré que les tests ne sont pas une corvée en plus mais un élément central du développement. Ils me permettent de valider la qualité du code et de refactorer en toute sécurité.
L'ajout et la modification de fonctionnalités est assuré par les tests car ça permet de vérifier si on casse ou pas les autres fonctionnalités.

Mes métriques finales :
- 36 tests au total, avec 97 % de réussite. Le seul qui ne passe pas c'est les points alignés, car mathématiquement c'est correct mais pas pour une triangulation.
- Couverture de code : 95%
- Performance : triangulation de 10000 points en < 1 seconde

Le coverage est très bon mais il est bien remonté par les tests de pointsets et de triangles (serialize et parse) mais pour la triangulation j'ai du 89% ce qui est faible pour une fonctionnalité majeure.

