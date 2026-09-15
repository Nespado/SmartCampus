```mermaid
classDiagram
    direction TB

    class ModuleCampus {
        <<abstract>>
        +emettreEvenement()
    }

    class ModuleAcces {
        +detecterIncendie()
    }

    class ModuleEcoGestion {
        +detecterAlerteConso()
    }

    class ModuleReservation {
        +annulerCours()
    }

    ModuleCampus <|-- ModuleAcces
    ModuleCampus <|-- ModuleEcoGestion
    ModuleCampus <|-- ModuleReservation


    class Evenement {
        <<abstract>>
        +date : Date
        +description : String
    }

    class Incendie {
        +localisation : String
    }

    class CoursAnnule {
        +nomCours : String
        +raison : String
    }

    class AlerteConso {
        +niveau : StringSujet
        +consommation : double
    }

    class Salle {
        +nom : String
        +interagir(e : Evenement)
    }

    Salle ..> Evenement
    Evenement <|-- Incendie
    Evenement <|-- CoursAnnule
    Evenement <|-- AlerteConso

    ModuleCampus "1" --> "0..*" Evenement : produit


    class Sujet {
        <<interface>>
        +add_observer(observer : Observateur)
        +remove_observer(observer : Observateur)
        +notify_observers(event : Evenement)
    }

    class Observateur {
        <<interface>>
        +update(event : Evenement)
    }

    class ServiceNotification {
        +update(event : Evenement)
        +handle_event(event : Evenement)
        +send(notification : Notification)
    }

    class Admin {
        +gerer_sujet(sujet : Sujet)
    }

    Admin --> Sujet 
    Sujet <|.. ModuleCampus
    Observateur <|.. ServiceNotification

    ModuleCampus "1" o-- "0..*" Observateur : notifie


    class StrategieEnvoi {
        <<interface>>
        +send(notification : Notification)
    }

    class EnvoiSMS {
        +send(notification : Notification)
    }

    class EnvoiEmail {
        +send(notification : Notification)
    }

    class EnvoiPush {
        +send(notification : Notification)
    }

    class EnvoiSlack {
        +send(notification : Notification)
    }

    StrategieEnvoi <|.. EnvoiSMS
    StrategieEnvoi <|.. EnvoiEmail
    StrategieEnvoi <|.. EnvoiPush
    StrategieEnvoi <|.. EnvoiSlack

    ServiceNotification "1" --> "1..*" StrategieEnvoi : utilise


    class Notification {
        <<abstract>>
        +destinataire : String
        +contenu : String
        +generate_content() : String
    }

    class SMS {
        +generate_content() : String
    }

    class Email {
        +generate_content() : String
    }

    class Push {
        +generate_content() : String
    }

    class Slack {
        +generate_content() : String
    }

    Notification <|-- SMS
    Notification <|-- Email
    Notification <|-- Push
    Notification <|-- Slack


    class NotificationDecorator {
        <<abstract>>
        #notification : Notification
        +generate_content() : String
    }

    class BaseNotification {
        +generate_content() : String
    }

    class WithSignature {
        +signature : String
        +generate_content() : String
    }

    class WithUrgentHeader {
        +generate_content() : String
    }

    class EncryptedNotification {
        +generate_content() : String
        +encrypt() : String
    }

    Notification <|-- NotificationDecorator
    NotificationDecorator <|-- WithSignature
    NotificationDecorator <|-- WithUrgentHeader
    NotificationDecorator <|-- EncryptedNotification
    Notification <|-- BaseNotification

    NotificationDecorator "1" o-- "1" Notification : enveloppe


    class NotificationFactory {
        <<factory>>
        +create(event : Evenement, recipient : String) : Notification
    }
    NotificationFactory "1" --> "1" Notification : crée
