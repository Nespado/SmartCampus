from .report_factory import ReportFactory


class ExcelReportFactory(ReportFactory):
    """Construit le contenu textuel ; l'export en fichier Excel n'est pas implémenté."""

    def create_header(self) -> str:
        header = f"[Excel] {self.report.titre} - {self.report.date_creation.isoformat()}"
        print("[ExcelReportFactory] En-tête construit.")
        return header

    def create_body(self) -> str:
        body = str(self.report.donnees.data)
        print("[ExcelReportFactory] Corps construit à partir des données du rapport.")
        return body
