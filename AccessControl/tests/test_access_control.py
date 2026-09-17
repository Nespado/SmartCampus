import os
import sys
import unittest
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AccessControlService import AccessControlService
from AccessRequest import AccessRequest
from Badge import Badge
from Professor import Professor
from SecurityRegistry import SecurityRegistry
from Student import Student

from fakes import FakeRoom, FakeScheduleService, RecordingObserver

AT_NOON = datetime.datetime(2026, 9, 17, 12, 0)
AT_NIGHT = datetime.datetime(2026, 9, 17, 22, 0)
TOMORROW = datetime.date(2026, 9, 18)
YESTERDAY = datetime.date(2026, 9, 16)


class AccessControlTestCase(unittest.TestCase):
    """Couvre les quatre maillons, le registre et le rôle de Sujet."""

    def setUp(self):
        """Réinitialise le singleton et reconstruit le service, deux personnes, deux salles."""
        self.registry = SecurityRegistry.get_instance()
        self.registry.reset()

        self.schedule = FakeScheduleService()
        self.service = AccessControlService(schedule_service=self.schedule,
                                            security_registry=self.registry)

        self.student = Student("Amine")
        self.professor = Professor("Dr. Haddad")
        self.classroom = FakeRoom("A101", clearance_level=1)
        self.laboratory = FakeRoom("LAB-3", clearance_level=3)

    def badge_of(self, person, expires_on=TOMORROW, active=True):
        """Crée un badge appartenant à cette personne."""
        return Badge(f"BDG-{person.get_name()}", person.get_id(), expires_on, active)

    def test_student_enters_an_open_classroom(self):
        """Cas nominal : les quatre maillons laissent passer."""
        request = AccessRequest(self.student, self.badge_of(self.student),
                                self.classroom, AT_NOON)
        decision = self.service.check_access(request)
        self.assertTrue(decision.is_granted(), decision.get_reason())

    def test_expired_badge_is_refused(self):
        """Maillon 1 : badge expiré refusé."""
        badge = self.badge_of(self.student, expires_on=YESTERDAY)
        decision = self.service.check_access(
            AccessRequest(self.student, badge, self.classroom, AT_NOON))
        self.assertFalse(decision.is_granted())
        self.assertEqual("BadgeValidityHandler", decision.get_refused_by())

    def test_deactivated_badge_is_refused(self):
        """Maillon 1 : badge désactivé refusé."""
        badge = self.badge_of(self.student, active=False)
        decision = self.service.check_access(
            AccessRequest(self.student, badge, self.classroom, AT_NOON))
        self.assertEqual("BadgeValidityHandler", decision.get_refused_by())

    def test_badge_of_somebody_else_is_refused(self):
        """Maillon 1 : badge emprunté refusé."""
        decision = self.service.check_access(
            AccessRequest(self.student, self.badge_of(self.professor),
                          self.classroom, AT_NOON))
        self.assertEqual("BadgeValidityHandler", decision.get_refused_by())

    def test_missing_badge_is_refused(self):
        """Maillon 1 : demande sans badge refusée."""
        decision = self.service.check_access(
            AccessRequest(self.student, None, self.classroom, AT_NOON))
        self.assertEqual("BadgeValidityHandler", decision.get_refused_by())

    def test_closed_room_is_refused(self):
        """Maillon 2 : salle fermée refusée."""
        decision = self.service.check_access(
            AccessRequest(self.student, self.badge_of(self.student),
                          self.classroom, AT_NIGHT))
        self.assertEqual("ScheduleCheckHandler", decision.get_refused_by())

    def test_closed_room_is_granted_with_a_reservation(self):
        """Maillon 2 : une réservation ouvre une salle fermée."""
        self.schedule.add(self.student.get_id(), self.classroom,
                          AT_NIGHT - datetime.timedelta(hours=1),
                          AT_NIGHT + datetime.timedelta(hours=1))
        decision = self.service.check_access(
            AccessRequest(self.student, self.badge_of(self.student),
                          self.classroom, AT_NIGHT))
        self.assertTrue(decision.is_granted(), decision.get_reason())

    def test_student_cannot_enter_the_laboratory(self):
        """Maillon 3 : habilitation insuffisante refusée."""
        decision = self.service.check_access(
            AccessRequest(self.student, self.badge_of(self.student),
                          self.laboratory, AT_NOON))
        self.assertEqual("RolePermissionHandler", decision.get_refused_by())

    def test_professor_can_enter_the_laboratory(self):
        """Maillon 3 : habilitation suffisante acceptée."""
        decision = self.service.check_access(
            AccessRequest(self.professor, self.badge_of(self.professor),
                          self.laboratory, AT_NOON))
        self.assertTrue(decision.is_granted(), decision.get_reason())

    def test_blacklisted_badge_is_refused(self):
        """Maillon 4 : badge sur liste noire refusé."""
        badge = self.badge_of(self.student)
        self.registry.blacklist_badge(badge.get_badge_id(), "Badge volé")
        decision = self.service.check_access(
            AccessRequest(self.student, badge, self.classroom, AT_NOON))
        self.assertEqual("BlacklistHandler", decision.get_refused_by())
        self.assertIn("Badge volé", decision.get_reason())

    def test_first_failing_link_stops_the_chain(self):
        """Le premier maillon en échec arrête la chaîne."""
        badge = self.badge_of(self.student, expires_on=YESTERDAY)
        self.registry.blacklist_badge(badge.get_badge_id(), "Badge volé")
        decision = self.service.check_access(
            AccessRequest(self.student, badge, self.laboratory, AT_NIGHT))
        self.assertEqual("BadgeValidityHandler", decision.get_refused_by())

    def test_every_request_is_journalised(self):
        """Accordée ou refusée, toute demande est journalisée."""
        badge = self.badge_of(self.student)
        self.service.check_access(AccessRequest(self.student, badge, self.classroom, AT_NOON))
        self.service.check_access(AccessRequest(self.student, badge, self.laboratory, AT_NOON))

        history = self.registry.get_history(badge.get_badge_id())
        self.assertEqual(2, len(history))
        self.assertTrue(history[0].is_granted())
        self.assertFalse(history[1].is_granted())
        self.assertEqual("A101", history[0].get_room_id())

    def test_registry_is_a_singleton(self):
        """get_instance() retourne toujours le même objet, le constructeur est fermé."""
        self.assertIs(SecurityRegistry.get_instance(), SecurityRegistry.get_instance())
        with self.assertRaises(RuntimeError):
            SecurityRegistry()

    def test_a_refusal_notifies_the_observers(self):
        """Seul un refus est publié, un observateur désabonné ne reçoit rien."""
        observer = RecordingObserver()
        self.service.add_observer(observer)

        self.service.check_access(AccessRequest(self.student, self.badge_of(self.student),
                                                self.classroom, AT_NOON))
        self.assertEqual([], observer.events)

        self.service.check_access(AccessRequest(self.student, self.badge_of(self.student),
                                                self.laboratory, AT_NOON))
        self.assertEqual(1, len(observer.events))
        self.assertIn("LAB-3", observer.events[0].get_description())

        self.service.remove_observer(observer)
        self.service.check_access(AccessRequest(self.student, self.badge_of(self.student),
                                                self.laboratory, AT_NOON))
        self.assertEqual(1, len(observer.events))


if __name__ == "__main__":
    unittest.main(verbosity=2)

