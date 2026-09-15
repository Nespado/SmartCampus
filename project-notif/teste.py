from datetime import date

from modules import (
    ModuleAcces,
    ModuleEcoGestion,
    ModuleReservation,
    ServiceNotification
)

from strategies_envoi import (
    EnvoiSMS,
    EnvoiEmail,
    EnvoiPush,
    EnvoiSlack
)

from factory import (
    NotificationFactory,
    TypeNotification
)

from decorateurs import (
    BaseNotification,
    WithSignature,
    WithUrgentHeader,
    EncryptedNotification
)


def main():

    print("========================================")
    print("   SYSTÈME DE NOTIFICATIONS CAMPUS")
    print("========================================")

    print("\n--- Initialisation des stratégies ---")

    strategies = [
        EnvoiSMS(),
        EnvoiEmail(),
        EnvoiPush(),
        EnvoiSlack()
    ]

    service_notif = ServiceNotification(strategies)

    print("Stratégies disponibles :")
    print("- SMS")
    print("- Email")
    print("- Push")
    print("- Slack")

    print("\n--- Initialisation des modules ---")

    module_acces = ModuleAcces()
    module_eco = ModuleEcoGestion()
    module_reservation = ModuleReservation()

    module_acces.ajouter_observateur(service_notif)
    module_eco.ajouter_observateur(service_notif)
    module_reservation.ajouter_observateur(service_notif)

    print("ServiceNotification enregistré comme observateur.")

    print("\n========================================")
    print("        TEST DU PATTERN OBSERVER")
    print("========================================")

    print("\n--- Incendie ---")

    module_acces.detecter_incendie(
        date_ev=date.today(),
        desc="Départ de feu détecté au bâtiment B",
        localisation="Bâtiment B - Étage 2"
    )

    print("\n--- Alerte consommation ---")

    module_eco.detecter_alerte_conso(
        date_ev=date.today(),
        desc="Consommation électrique anormalement élevée",
        niveau="ÉLEVÉ",
        consommation=875.5
    )

    print("\n--- Cours annulé ---")

    module_reservation.annuler_cours(
        date_ev=date.today(),
        desc="Le cours est annulé.",
        nom_cours="Architecture Logicielle",
        raison="Absence de l'enseignant"
    )

    print("\n========================================")
    print("        TEST DU PATTERN FACTORY")
    print("========================================")

    notification = NotificationFactory.creer(
        TypeNotification.EMAIL,
        "etudiants@campus.fr",
        "Coupure de courant prévue."
    )

    print("\nNotification créée avec la Factory :")
    print(notification.generate_content())

    print("\n========================================")
    print("       TEST DU PATTERN DECORATOR")
    print("========================================")

    notification = WithSignature(
        notification,
        "Direction du Campus"
    )

    print("\nAprès WithSignature :")
    print(notification.generate_content())

    notification = WithUrgentHeader(notification)

    print("\nAprès WithUrgentHeader :")
    print(notification.generate_content())

    notification = EncryptedNotification(notification)

    print("\nAprès EncryptedNotification :")
    print(notification.generate_content())

    print("\n========================================")
    print("      TEST DE COMPOSITION COMPLÈTE")
    print("========================================")

    notification_complete = BaseNotification(
        destinataire="admin@campus.fr",
        contenu="Alerte de sécurité maximale."
    )

    notification_complete = WithSignature(
        notification_complete,
        "Direction du Campus"
    )

    notification_complete = WithUrgentHeader(
        notification_complete
    )

    notification_complete = EncryptedNotification(
        notification_complete
    )

    print("\nNotification finale :")
    print(notification_complete.generate_content())

    print("\n========================================")
    print("             FIN DES TESTS")
    print("========================================")


if __name__ == "__main__":
    main()
