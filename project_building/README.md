# SmartCampus - Groupe 2

Cette implémentation couvre le fonctionnement des bâtiments :

- pattern **State** pour `Occupied`, `EcoMode`, `Night` et `Emergency` ;
- pattern **Strategy** pour les algorithmes `PIDAlgorithm`, `QuickThresholdAlgorithm` et `SolarOptimizedAlgorithm` ;
- bâtiments spécialisés `LectureHall`, `Laboratory` et `Classroom`.

## Principes SOLID

- **SRP** : les états portent les politiques d’action, les algorithmes calculent
	la régulation et `Building` orchestre le cycle de fonctionnement.
- **OCP** : un nouvel état ou algorithme peut être ajouté en implémentant son
	abstraction, sans modifier les classes existantes.
- **LSP** : tous les états respectent le contrat `RoomState` et tous les
	algorithmes respectent `RegulationAlgorithm`.
- **ISP** : les politiques dépendent de petits contrats séparés pour le
	chauffage et l’éclairage.
- **DIP** : `Building` dépend de `RegulationService`, pas de
	`RegulationController`. Un service compatible peut donc être injecté pour
	les tests ou pour une autre implémentation.

## Tests

```bash
python -m pytest
```