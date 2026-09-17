from .report_factory import ReportFactory

class PDFReportFactory(ReportFactory):
    def create_header(self):
        return "En-tête du rapport PDF"

    def create_body(self):
        return "Corps du rapport PDF"
    