import unittest
from datetime import date

from decorateurs import (
    BaseNotification,
    EncryptedNotification,
    WithSignature,
    WithUrgentHeader,
)
from evenements import CampusEvent, Evenement, Incendie
from factory import NotificationFactory, TypeNotification
from modules import ModuleAcces, NotificationService, ServiceNotification, ModuleCampus
from notifications import Notification, Email, BaseNotification as BaseNotificationFromNotif
from strategies_envoi import (
    DeliveryStrategy,
    StrategieEnvoi,
    SmsDeliveryStrategy,
    EmailDeliveryStrategy,
    PushDeliveryStrategy,
    SlackDeliveryStrategy,
    EnvoiSMS,
    EnvoiEmail,
    EnvoiPush,
    EnvoiSlack,
)
from sujets_observateurs import EventPublisher, EventObserver, Sujet, Observateur


class RecordingStrategy(DeliveryStrategy):

    def __init__(self):
        self.notifications = []

    def send(self, notification: Notification) -> None:
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

    def test_encrypted_notification_encrypt_without_args(self):
        """Vérifie que encrypt() peut être appelé sans argument conformément au contrat."""
        base_notif = BaseNotification("secu@campus.fr", "Code secret")
        encrypted = EncryptedNotification(base_notif)

        # Appel sans argument spécifié par le contrat : encrypt() -> str
        result = encrypted.encrypt()
        self.assertEqual(result, "[CHIFFRÉ] Code secret")
        self.assertEqual(encrypted.generate_content(), "[CHIFFRÉ] Code secret")

        # Appel avec argument optionnel pour rétrocompatibilité
        self.assertEqual(encrypted.encrypt("autre"), "[CHIFFRÉ] autre")
        self.assertEqual(encrypted.chiffrer(), "[CHIFFRÉ] Code secret")

    def test_base_notification_importable_from_notifications(self):
        """Vérifie que BaseNotification est disponible depuis notifications.py et decorateurs.py."""
        self.assertIs(BaseNotification, BaseNotificationFromNotif)
        b = BaseNotificationFromNotif("user@campus.fr", "Texte simple")
        self.assertEqual(b.generate_content(), "Texte simple")
        self.assertEqual(b.recipient, "user@campus.fr")
        self.assertEqual(b.destinataire, "user@campus.fr")
        self.assertEqual(b.content, "Texte simple")
        self.assertEqual(b.contenu, "Texte simple")

    def test_factory_supports_group_one_contract(self):
        """Vérifie NotificationFactory.create(event: CampusEvent, recipient: str) -> Notification."""
        event = Incendie(date.today(), "Feu détecté", "Bâtiment B")
        # Appel avec arguments positionnels et nommés
        notification = NotificationFactory.create(event=event, recipient="admin@campus.fr")

        self.assertIsInstance(notification, Notification)
        self.assertIsInstance(notification, Email)
        self.assertEqual(notification.destinataire, "admin@campus.fr")
        self.assertEqual(notification.generate_content(), "EMAIL: Feu détecté")

    def test_observer_publisher_contract_and_keyword_arguments(self):
        """Vérifie que add_observer, remove_observer, notify_observers, update, handle_event acceptent les bons noms d'arguments."""
        strategy = RecordingStrategy()
        service = NotificationService([strategy])
        module = ModuleAcces()

        # Vérification des noms d'arguments du contrat (observer: EventObserver)
        module.add_observer(observer=service)
        event = Incendie(date.today(), "Feu", "Bâtiment B")

        # Vérification notify_observers(event: CampusEvent)
        module.notify_observers(event=event)
        self.assertEqual(len(strategy.notifications), 1)

        # Vérification update(event: CampusEvent) direct
        service.update(event=event)
        self.assertEqual(len(strategy.notifications), 2)

        # Vérification handle_event(event: CampusEvent) direct
        service.handle_event(event=event)
        self.assertEqual(len(strategy.notifications), 3)

        # Vérification send(notification: Notification) direct
        notif = BaseNotification("test@campus.fr", "Message direct")
        service.send(notification=notif)
        self.assertEqual(len(strategy.notifications), 4)
        self.assertEqual(strategy.notifications[-1].generate_content(), "Message direct")

        # Vérification remove_observer(observer: EventObserver)
        module.remove_observer(observer=service)
        module.notify_observers(event=event)
        # N'a pas augmenté car l'observateur est retiré
        self.assertEqual(len(strategy.notifications), 4)

    def test_all_delivery_strategies(self):
        """Vérifie les 4 stratégies de livraison du Groupe 1."""
        notif = BaseNotification("dest@campus.fr", "Test stratégie")
        strategies = [
            SmsDeliveryStrategy(),
            EmailDeliveryStrategy(),
            PushDeliveryStrategy(),
            SlackDeliveryStrategy(),
        ]
        for st in strategies:
            self.assertIsInstance(st, DeliveryStrategy)
            st.send(notification=notif)

    def test_aliases_and_subtyping(self):
        """Vérifie l'exactitude des hiérarchies et alias."""
        self.assertTrue(issubclass(ModuleCampus, EventPublisher))
        self.assertTrue(issubclass(NotificationService, EventObserver))
        self.assertIs(ServiceNotification, NotificationService)
        self.assertIs(Sujet, EventPublisher)
        self.assertIs(Observateur, EventObserver)
        self.assertIs(Evenement, CampusEvent)
        self.assertIs(StrategieEnvoi, DeliveryStrategy)
        self.assertIs(EnvoiSMS, SmsDeliveryStrategy)
        self.assertIs(EnvoiEmail, EmailDeliveryStrategy)
        self.assertIs(EnvoiPush, PushDeliveryStrategy)
        self.assertIs(EnvoiSlack, SlackDeliveryStrategy)

    def test_legacy_factory_and_strategy_names_still_work(self):
        """Vérifie que l'ancienne API française continue de fonctionner."""
        notification = NotificationFactory.creer(
            TypeNotification.SMS, "0600000000", "Bonjour"
        )
        strategy = RecordingStrategy()
        ServiceNotification([strategy]).envoyer(notification)
        self.assertIs(strategy.notifications[0], notification)


if __name__ == "__main__":
    unittest.main()
