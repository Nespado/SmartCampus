from contextlib import redirect_stdout
from datetime import date
from inspect import signature
from io import StringIO
import unittest
from typing import get_type_hints

from data_management.data_management_service import DataManagementService
from data_management.reports.excel_report_factory import ExcelReportFactory
from data_management.reports.pdf_report_factory import PDFReportFactory
from data_management.reports.report import Report
from data_management.reports.report_factory import ReportFactory
from data_management.systeme import Systeme
from data_management.unified_data import UnifiedData


class SimulatedAdapter:
    """Double de test uniquement : aucun fichier n'est lu."""

    def __init__(self, data):
        self.data = data

    def adapt(self):
        return self.data


class DataManagementTests(unittest.TestCase):
    def setUp(self):
        self.output = StringIO()
        capture = redirect_stdout(self.output)
        capture.__enter__()
        self.addCleanup(capture.__exit__, None, None, None)
        self.data = UnifiedData([{"salle": "A101", "reservations": 3}])

    def test_pdf_contract_signatures(self):
        contracts = [
            (DataManagementService, "import_data", UnifiedData),
            (DataManagementService, "retrieve_data", UnifiedData),
            (DataManagementService, "generate_report", Report),
        ]
        for factory in (ReportFactory, PDFReportFactory, ExcelReportFactory):
            contracts.extend((factory, method, str) for method in ("create_header", "create_body"))
        for cls, method_name, return_type in contracts:
            with self.subTest(cls=cls.__name__, method=method_name):
                method = getattr(cls, method_name)
                self.assertEqual(list(signature(method).parameters), ["self"])
                self.assertIs(get_type_hints(method)["return"], return_type)

    def test_import_retrieve_and_generate_both_formats(self):
        for factory, format_name in ((PDFReportFactory, "PDF"), (ExcelReportFactory, "Excel")):
            with self.subTest(format=format_name):
                service = Systeme(SimulatedAdapter(self.data), factory, "Occupation des salles")
                self.assertIs(service.import_data(), self.data)
                self.assertIs(service.retrieve_data(), self.data)
                report = service.generate_report()
                self.assertIsInstance(report, Report)
                self.assertIs(report.donnees, self.data)
                self.assertEqual(report.titre, "Occupation des salles")
                self.assertEqual(report.date_creation, date.today())
                self.assertIn(format_name, report.header)
                self.assertIn(report.titre, report.header)
                self.assertIn("A101", report.body)
                self.assertEqual(service.rapports, [report])
                self.assertIn("Rapport construit", self.output.getvalue())

    def test_missing_adapter(self):
        with self.assertRaises(RuntimeError):
            DataManagementService().import_data()
        self.assertIn("aucun adapter", self.output.getvalue())
        self.assertNotIn("Import réussi", self.output.getvalue())

    def test_no_data_cannot_be_retrieved_or_reported(self):
        service = DataManagementService()
        with self.assertRaises(RuntimeError):
            service.retrieve_data()
        with self.assertRaises(RuntimeError):
            service.generate_report()
        self.assertEqual(service.rapports, [])
        self.assertNotIn("Rapport construit", self.output.getvalue())

    def test_invalid_adapter_return_is_rejected(self):
        service = DataManagementService(SimulatedAdapter({"invalid": True}))
        with self.assertRaises(TypeError):
            service.import_data()
        with self.assertRaises(RuntimeError):
            service.retrieve_data()
        self.assertNotIn("Import réussi", self.output.getvalue())

    def test_adapter_failure_is_propagated(self):
        class FailingAdapter:
            def adapt(self):
                raise OSError("Source indisponible")

        service = DataManagementService(FailingAdapter())
        with self.assertRaisesRegex(OSError, "Source indisponible"):
            service.import_data()
        self.assertIn("ERREUR pendant l'import", self.output.getvalue())
        self.assertNotIn("Import réussi", self.output.getvalue())

    def test_failed_report_is_not_saved(self):
        class FailingFactory(PDFReportFactory):
            def create_body(self) -> str:
                raise ValueError("Construction impossible")

        service = DataManagementService(SimulatedAdapter(self.data), FailingFactory)
        service.import_data()
        with self.assertRaisesRegex(ValueError, "Construction impossible"):
            service.generate_report()
        self.assertEqual(service.rapports, [])
        self.assertIn("ERREUR pendant la construction", self.output.getvalue())
        self.assertNotIn("Rapport construit", self.output.getvalue())

    def test_non_string_report_content_is_rejected(self):
        class InvalidFactory(PDFReportFactory):
            def create_body(self):
                return None

        service = DataManagementService(SimulatedAdapter(self.data), InvalidFactory)
        service.import_data()
        with self.assertRaises(TypeError):
            service.generate_report()
        self.assertEqual(service.rapports, [])
        self.assertNotIn("Rapport construit", self.output.getvalue())

    def test_successive_reports_are_kept_in_history(self):
        service = DataManagementService(SimulatedAdapter(self.data))
        service.import_data()
        first = service.generate_report()
        second = service.generate_report()
        self.assertIsNot(first, second)
        self.assertEqual(service.rapports, [first, second])


if __name__ == "__main__":
    unittest.main()
