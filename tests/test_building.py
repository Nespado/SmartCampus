import unittest

from project_building import (
    Building,
    Emergency,
    Occupied,
    QuickThresholdAlgorithm,
    RegulationController,
    RegulationInput,
    Night,
)


def make_building(state):
    data = RegulationInput(current_temperature=18, target_temperature=21, occupancy=1)
    controller = RegulationController(QuickThresholdAlgorithm())
    return Building(state, controller, data, occupancy=data.occupancy)


class FixedRegulationService:
    def calculate_regulation(self, data):
        return 0.25


class BuildingTests(unittest.TestCase):
    def test_occupied_state_regulates_heating_and_lighting(self):
        building = make_building(Occupied())

        building.regulate()

        self.assertEqual(building.heating_level, 1.0)
        self.assertEqual(building.lighting_level, 1.0)


    def test_night_turns_light_on_when_someone_is_present(self):
        building = make_building(Night())

        building.regulate_lighting()

        self.assertEqual(building.lighting_level, 1.0)


    def test_emergency_disables_heating_and_forces_lighting(self):
        building = make_building(Emergency())

        building.regulate()

        self.assertEqual(building.heating_level, 0.0)
        self.assertEqual(building.lighting_level, 1.0)


    def test_state_can_be_changed_at_runtime(self):
        building = make_building(Occupied())

        building.change_state(Emergency())
        building.regulate()

        self.assertIsInstance(building.state, Emergency)
        self.assertEqual(building.heating_level, 0.0)


    def test_controller_can_switch_algorithm(self):
        building = make_building(Occupied())
        controller = building.regulator
        controller.set_strategy(QuickThresholdAlgorithm(threshold=4))

        self.assertEqual(controller.calculate_regulation(building.regulation_input), 0.0)


    def test_invalid_state_is_rejected(self):
        with self.assertRaises(TypeError):
            make_building(object())

    def test_building_depends_on_regulation_abstraction(self):
        data = RegulationInput(current_temperature=20, target_temperature=21)
        building = Building(Occupied(), FixedRegulationService(), data)

        building.regulate_heating()

        self.assertEqual(building.heating_level, 0.25)