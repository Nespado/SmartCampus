"""Strategy context for building energy regulation."""

from .contracts import RegulationService
from .strategies import RegulationAlgorithm, RegulationInput


class RegulationController(RegulationService):
    def __init__(self, strategy: RegulationAlgorithm):
        self._strategy = strategy

    @property
    def strategy(self) -> RegulationAlgorithm:
        return self._strategy

    def set_strategy(self, strategy: RegulationAlgorithm) -> None:
        if not isinstance(strategy, RegulationAlgorithm):
            raise TypeError("strategy must implement RegulationAlgorithm")
        self._strategy = strategy

    def calculate_regulation(self, regulation_input: RegulationInput) -> float:
        return self._strategy.calculate(regulation_input)