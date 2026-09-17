from .report_factory import ReportFactory

class ExcelReportFactory(ReportFactory):
    def create_header(self):
        return "En-tête du rapport Excel"

    def create_body(self):
        return "Corps du rapport Excel"