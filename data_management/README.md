# Système et rapports — groupe 5

L'API suit la page 4 de `Methodes_Arguments (1).pdf` : classes en
PascalCase, méthodes et arguments en snake_case.

- `DataManagementService.import_data()` et `retrieve_data()` renvoient `UnifiedData`.
- `DataManagementService.generate_report()` renvoie `Report`.
- `create_header()` et `create_body()` renvoient `str` pour les deux factories.
- Ces méthodes s'appellent sans argument. La configuration passe par les constructeurs.
- `Systeme` reprend le nom du diagramme et hérite de `DataManagementService`.

Les factories construisent un en-tête et un corps textuels à partir d'un
`Report`. Elles ne produisent pas encore de véritables fichiers `.pdf` ou `.xlsx`.
Les `print` indiquent les étapes terminées et les erreurs ; les méthodes
conservent leurs valeurs de retour et propagent les exceptions.

## Connexion avec la partie fichiers

Le service utilise les adapters du package `data_management.fichiers` et attend un objet
possédant `adapt() -> UnifiedData`. `AdapterProtocol` décrit ce contrat.

La classe commune est `data_management.fichiers.unified_data.UnifiedData`, construite avec
`UnifiedData(data=...)`. Le service conserve l'objet renvoyé par l'adapter ;
les factories lisent son attribut `.data` via `rapport.donnees.data`.
Le module `data_management.unified_data` réexporte cette même classe pour
conserver l'ancien chemin d'import, sans définir une seconde classe.

Exemple avec un fichier CSV existant (adapter le chemin à votre fichier) :

```python
from data_management.data_management_service import DataManagementService
from data_management.reports.excel_report_factory import ExcelReportFactory
from data_management.fichiers.csv_adapter import CSVAdapter
from data_management.fichiers.legacy_file import LegacyFile

fichier = LegacyFile(name="salles", path="salles.csv", type="csv")
service = DataManagementService(
    file_adapter=CSVAdapter(fichier),
    report_factory=ExcelReportFactory,
    report_title="Bilan SmartCampus",
)
service.import_data()
donnees = service.retrieve_data()
rapport = service.generate_report()
print(rapport.header)
print(rapport.body)
```

La factory PDF est utilisée par défaut. Une factory peut aussi être appelée
directement avec `PDFReportFactory(rapport)`, puis `create_header()` et
`create_body()`.

## Vérification locale

Depuis la racine du projet, avec Python 3.10 ou supérieur :

```text
python -m unittest discover -s tests -v
```

Les tests vérifient les deux factories, les signatures du PDF, les données
conservées dans le rapport, l'historique et les erreurs. Les tests d'intégration
utilisent les vrais adapters CSV et XML avec des fichiers temporaires, ainsi
que le vrai adapter API REST avec une réponse HTTP simulée. Chaque adapter
est testé jusqu'à la construction des rapports PDF et Excel ; aucun service
HTTP réel n'est contacté. L'assemblage avec les autres groupes reste à valider.
