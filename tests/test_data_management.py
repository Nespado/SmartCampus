from contextlib import redirect_stdout
from datetime import date
from inspect import signature
from io import BytesIO, StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from typing import get_type_hints

from data_management.data_management_service import DataManagementService
from data_management.reports.excel_report_factory import ExcelReportFactory
from data_management.reports.pdf_report_factory import PDFReportFactory
from data_management.reports.report import Report
from data_management.reports.report_factory import ReportFactory
from data_management.systeme import Systeme
from data_management.unified_data import UnifiedData as LegacyUnifiedData
from data_management.fichiers.api_rest_adapter import ApiRestThirdPartyAdapter
from data_management.fichiers.csv_adapter import CSVAdapter
from data_management.fichiers.legacy_file import LegacyFile
from data_management.fichiers.unified_data import UnifiedData
from data_management.fichiers.xml_apogee_adapter import XmlApogeeAdapter


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

    def test_old_import_uses_the_files_class(self):
        self.assertIs(LegacyUnifiedData, UnifiedData)

    def assert_adapter_reports(self, adapter, expected_data):
        for factory, format_name in ((PDFReportFactory, "PDF"), (ExcelReportFactory, "Excel")):
            with self.subTest(adapter=type(adapter).__name__, format=format_name):
                service = DataManagementService(adapter, factory, "Bilan des salles")
                data = service.import_data()
                self.assertIsInstance(data, UnifiedData)
                self.assertEqual(data.data, expected_data)
                self.assertIs(service.retrieve_data(), data)
                report = service.generate_report()
                self.assertIs(report.donnees, data)
                self.assertEqual(report.body, str(expected_data))
                self.assertIn(format_name, report.header)
                self.assertIn("Bilan des salles", report.header)
                self.assertEqual(service.rapports, [report])

    def test_csv_adapter_to_reports(self):
        with TemporaryDirectory(prefix="smartcampus-test-") as directory:
            path = Path(directory) / "salles.csv"
            path.write_text("salle,reservations\nA101,3\n", encoding="utf-8")
            adapter = CSVAdapter(LegacyFile("salles", str(path), "csv"))
            self.assert_adapter_reports(adapter, {
                "source": "CSV",
                "nom": "salles",
                "donnees": [{"salle": "A101", "reservations": "3"}],
            })

    def test_xml_adapter_to_reports(self):
        with TemporaryDirectory(prefix="smartcampus-test-") as directory:
            path = Path(directory) / "salles.xml"
            path.write_text(
                "<salles><salle><nom>A101</nom><reservations>3</reservations></salle></salles>",
                encoding="utf-8",
            )
            adapter = XmlApogeeAdapter(LegacyFile("salles", str(path), "xml"))
            self.assert_adapter_reports(adapter, {
                "source": "XML APOGEE",
                "nom": "salles",
                "donnees": [{"nom": "A101", "reservations": "3"}],
            })

    def test_api_adapter_to_reports(self):
        url = "https://example.invalid/salles"
        payload = b'[{"salle": "A101", "reservations": 3}]'
        with patch(
            "data_management.fichiers.api_rest_adapter.urlopen",
            side_effect=lambda requested_url: BytesIO(payload),
        ) as request:
            self.assert_adapter_reports(ApiRestThirdPartyAdapter(url), {
                "source": "API REST",
                "url": url,
                "donnees": [{"salle": "A101", "reservations": 3}],
            })
            self.assertEqual(request.call_count, 2)
            request.assert_called_with(url)


if __name__ == "__main__":
    unittest.main()
