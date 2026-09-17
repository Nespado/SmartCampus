from adc import ABC, abstractmethod

class ReportFactory(ABC):
    @abstractmethod
    def create_header(self):
        pass

    @abstractmethod
    def create_body(self):
        pass
    