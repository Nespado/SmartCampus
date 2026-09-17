from .report_factory import ReportFactory


class PDFReportFactory(ReportFactory):
    """Construit le contenu textuel ; l'export en fichier PDF n'est pas implémenté."""

    def create_header(self) -> str:
        header = f"[PDF] {self.report.titre} - {self.report.date_creation.isoformat()}"
        print("[PDFReportFactory] En-tête construit.")
        return header

    def create_body(self) -> str:
        body = str(self.report.donnees.data)
        print("[PDFReportFactory] Corps construit à partir des données du rapport.")
        return body
