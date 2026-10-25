from typing import Protocol

from data_management.fichiers.unified_data import UnifiedData

from .reports.pdf_report_factory import PDFReportFactory
from .reports.report import Report
from .reports.report_factory import ReportFactory


class AdapterProtocol(Protocol):
    """Contrat attendu, sans implémenter la partie fichiers."""

    def adapt(self) -> UnifiedData:
        ...


class DataManagementService:
    def __init__(
        self,
        file_adapter: AdapterProtocol | None = None,
        report_factory: type[ReportFactory] = PDFReportFactory,
        report_title: str = "Rapport SmartCampus",
    ):
        self.file_adapter = file_adapter
        self.report_factory = report_factory
        self.report_title = report_title
        self.rapports: list[Report] = []
        self._data: UnifiedData | None = None

    def import_data(self) -> UnifiedData:
        if self.file_adapter is None:
            print("[DataManagementService] ERREUR : aucun adapter de fichiers connecté.")
            raise RuntimeError("Connecter un adapter avant d'importer les données.")

        print("[DataManagementService] Début de l'import des données.")
        try:
            data = self.file_adapter.adapt()
            if not isinstance(data, UnifiedData):
                raise TypeError("adapt() doit retourner un objet UnifiedData.")
        except Exception as error:
            print(f"[DataManagementService] ERREUR pendant l'import : {error}")
            raise

        self._data = data
        print("[DataManagementService] Import réussi : objet UnifiedData reçu.")
        return data

    def retrieve_data(self) -> UnifiedData:
        if self._data is None:
            print("[DataManagementService] ERREUR : aucune donnée importée.")
            raise RuntimeError("Importer les données avant de les récupérer.")

        print("[DataManagementService] Données importées récupérées.")
        return self._data

    def generate_report(self) -> Report:
        data = self.retrieve_data()
        report = Report(self.report_title, data)
        print("[DataManagementService] Début de la construction du rapport.")
        try:
            factory = self.report_factory(report)
            report.header = factory.create_header()
            report.body = factory.create_body()
            if not isinstance(report.header, str) or not isinstance(report.body, str):
                raise TypeError("Les méthodes de la factory doivent retourner des str.")
        except Exception as error:
            print(f"[DataManagementService] ERREUR pendant la construction du rapport : {error}")
            raise

        self.rapports.append(report)
        print(
            f"[DataManagementService] Rapport construit et ajouté à l'historique "
            f"({len(self.rapports)} rapport(s)). Aucun fichier exporté."
        )
        return report
