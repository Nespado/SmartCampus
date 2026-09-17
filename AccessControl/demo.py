"""Démonstration du Groupe 3 : lancer avec `python3 demo.py`.

Room et ScheduleService ne sont pas encore livrées, les doublures de
tests/fakes.py servent en attendant les classes des Groupes 2 et 4.
"""

import os
import sys
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"))

from AccessControlService import AccessControlService
from AccessRequest import AccessRequest
from Badge import Badge
from Professor import Professor
from SecurityRegistry import SecurityRegistry
from Student import Student
from fakes import FakeRoom, FakeScheduleService

NOON = datetime.datetime(2026, 9, 17, 12, 0)
NIGHT = datetime.datetime(2026, 9, 17, 22, 0)


class ConsoleObserver:
    """Tient lieu de NotificationService du Groupe 1."""

    def update(self, event):
        """Affiche l'événement publié par le service."""
        print(f"      -> observateur notifié : {event.get_description()}")


def main():
    """Joue cinq scénarios d'accès puis affiche le journal de sécurité."""
    registry = SecurityRegistry.get_instance()
    schedule = FakeScheduleService()
    service = AccessControlService(schedule_service=schedule, security_registry=registry)
    service.add_observer(ConsoleObserver())

    amine = Student("Amine")
    haddad = Professor("Dr. Haddad")

    classroom = FakeRoom("A101", clearance_level=1)
    laboratory = FakeRoom("LAB-3", clearance_level=3)

    amine_badge = Badge("BDG-001", amine.get_id(), datetime.date(2026, 12, 31))
    haddad_badge = Badge("BDG-002", haddad.get_id(), datetime.date(2026, 12, 31))
    stolen_badge = Badge("BDG-003", amine.get_id(), datetime.date(2026, 12, 31))
    registry.blacklist_badge("BDG-003", "Déclaré volé le 15/09")

    schedule.add(amine.get_id(), classroom, NIGHT, NIGHT + datetime.timedelta(hours=2))

    scenarios = [
        ("Amine dans la salle de cours à midi", amine, amine_badge, classroom, NOON),
        ("Amine dans le laboratoire à midi", amine, amine_badge, laboratory, NOON),
        ("Dr. Haddad dans le laboratoire à midi", haddad, haddad_badge, laboratory, NOON),
        ("Amine dans la salle de cours à 22h", amine, amine_badge, classroom, NIGHT),
        ("Amine avec le badge volé", amine, stolen_badge, classroom, NOON),
    ]

    for label, person, badge, room, at in scenarios:
        decision = service.check_access(AccessRequest(person, badge, room, at))
        print(f"{label:40s} : {decision}")

    print("\n--- Journal de sécurité ---")
    for entry in registry.get_access_log():
        print(f"  {entry}")


if __name__ == "__main__":
    main()

