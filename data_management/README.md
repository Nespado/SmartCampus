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

Aucune classe `Fichiers` ni aucun adapter concret n'est implémenté ici.
Le service attend un objet possédant `adapt() -> UnifiedData`.
`AdapterProtocol` décrit uniquement ce contrat.

Le PDF ne précise pas la structure interne de `UnifiedData` : le conteneur
minimal `UnifiedData(donnees=...)` est donc une proposition à harmoniser avec
l'autre partie du groupe. La relation `Systeme` / `Fichiers` du diagramme et
les échanges avec les autres groupes restent à vérifier avec leur code.

Une fois l'adapter réel disponible :

```python
from data_management.data_management_service import DataManagementService
from data_management.reports.excel_report_factory import ExcelReportFactory

# adapter_reel est créé par la partie fichiers et renvoie notre UnifiedData.
service = DataManagementService(
    file_adapter=adapter_reel,
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

Les tests simulent `adapt()` en mémoire. Ils vérifient les deux factories,
les signatures du PDF, les données conservées dans le rapport, l'historique
et les erreurs. Ils ne valident pas l'intégration avec les adapters réels.
