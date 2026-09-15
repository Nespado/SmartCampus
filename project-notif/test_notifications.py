import unittest
from datetime import date

from decorateurs import BaseNotification, EncryptedNotification, WithSignature, WithUrgentHeader
from evenements import Incendie
from factory import NotificationFactory, TypeNotification
from modules import ModuleAcces, ServiceNotification
from notifications import Email
from strategies_envoi import StrategieEnvoi


class RecordingStrategy(StrategieEnvoi):
    def __init__(self):
        self.notifications = []

    def send(self, notification):
        self.notifications.append(notification)


class NotificationsTestCase(unittest.TestCase):
    def test_decorators_compose_content(self):
        notification = BaseNotification("admin@campus.fr", "Alerte")
        notification = EncryptedNotification(
            WithUrgentHeader(WithSignature(notification, "Direction"))
        )

        self.assertEqual(
            notification.generate_content(),
            "[CHIFFRÉ] URGENT\nAlerte\nSignature : Direction",
        )
        self.assertEqual(notification.generer_contenu(), notification.generate_content())

    def test_factory_supports_group_one_contract(self):
        event = Incendie(date.today(), "Feu détecté", "Bâtiment B")
        notification = NotificationFactory.create(event, "admin@campus.fr")

        self.assertIsInstance(notification, Email)
        self.assertEqual(notification.destinataire, "admin@campus.fr")
        self.assertEqual(notification.generate_content(), "EMAIL: Feu détecté")

    def test_observer_notifies_and_can_be_removed(self):
        strategy = RecordingStrategy()
        service = ServiceNotification([strategy])
        module = ModuleAcces()

        module.add_observer(service)
        module.detecter_incendie(date.today(), "Feu", "Bâtiment B")
        self.assertEqual(len(strategy.notifications), 1)

        module.remove_observer(service)
        module.detecter_incendie(date.today(), "Second feu", "Bâtiment C")
        self.assertEqual(len(strategy.notifications), 1)

    def test_legacy_factory_and_strategy_names_still_work(self):
        notification = NotificationFactory.creer(
            TypeNotification.SMS, "0600000000", "Bonjour"
        )
        strategy = RecordingStrategy()
        ServiceNotification([strategy]).send(notification)
        self.assertIs(strategy.notifications[0], notification)


if __name__ == "__main__":
    unittest.main()
