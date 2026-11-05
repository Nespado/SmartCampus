"""Building states and their heating/lighting policies."""

from abc import ABC, abstractmethod

from .contracts import HeatingContext, LightingContext


class RoomState(ABC):
    @abstractmethod
    def regulate_heating(self, context: HeatingContext) -> None:
        pass

    @abstractmethod
    def regulate_lighting(self, context: LightingContext) -> None:
        pass

    def regulate(self, context: HeatingContext, lighting_context: LightingContext) -> None:
        self.regulate_heating(context)
        self.regulate_lighting(lighting_context)


class Occupied(RoomState):
    def regulate_heating(self, context: HeatingContext) -> None:
        level = context.regulator.calculate_regulation(context.regulation_input)
        context.set_heating_level(level)

    def regulate_lighting(self, context: LightingContext) -> None:
        context.set_lighting_level(1.0)


class EcoMode(RoomState):
    def regulate_heating(self, context: HeatingContext) -> None:
        command = context.regulator.calculate_regulation(context.regulation_input)
        context.set_heating_level(command * 0.5)

    def regulate_lighting(self, context: LightingContext) -> None:
        context.set_lighting_level(0.3)


class Night(RoomState):
    def regulate_heating(self, context: HeatingContext) -> None:
        command = context.regulator.calculate_regulation(context.regulation_input)
        context.set_heating_level(command * 0.3)

    def regulate_lighting(self, context: LightingContext) -> None:
        context.set_lighting_level(1.0 if context.occupancy > 0 else 0.0)


class Emergency(RoomState):
    def regulate_heating(self, context: HeatingContext) -> None:
        context.set_heating_level(0.0)

    def regulate_lighting(self, context: LightingContext) -> None:
        context.set_lighting_level(1.0)