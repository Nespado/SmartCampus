from abc import ABC, abstractmethod

from .report import Report


class ReportFactory(ABC):
    def __init__(self, report: Report):
        self.report = report

    @abstractmethod
    def create_header(self) -> str:
        pass

    @abstractmethod
    def create_body(self) -> str:
        pass
