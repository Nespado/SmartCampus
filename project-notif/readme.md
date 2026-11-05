# Projet Notifications — SmartCampus

Système de notifications du campus conforme au document de référence **SmartCampus (Groupe 1 - Notifications)** basé sur plusieurs patrons de conception :

- **Observer** : les modules du campus (`EventPublisher`) publient des événements (`CampusEvent`) et le service de notification (`NotificationService`) les reçoit en tant qu'observateur (`EventObserver`) ;
- **Factory** : création centralisée des notifications avec `NotificationFactory.create(event, recipient)` ;
- **Strategy** : canaux d’envoi interchangeables (`SmsDeliveryStrategy`, `EmailDeliveryStrategy`, `PushDeliveryStrategy`, `SlackDeliveryStrategy`) implémentant `DeliveryStrategy` ;
- **Decorator** : ajout dynamique d'une signature (`WithSignature`), d'un en-tête urgent (`WithUrgentHeader`) ou d'un chiffrement (`EncryptedNotification`).


## 1. Structure du projet

| Fichier | Rôle |
|---|---|
| `evenements.py` / `events.py` | Définit les événements du campus (`CampusEvent`, `Incendie`, `CoursAnnule`, `AlerteConso`). |
| `sujets_observateurs.py` / `publishers_observers.py` | Définit les interfaces Observer (`EventPublisher`, `EventObserver`). |
| `modules.py` | Modules du campus (`ModuleCampus`, `ModuleAcces`, etc.) et `NotificationService`. |
| `notifications.py` | Définit `Notification`, `BaseNotification`, `SMS`, `Email`, `Push`, `Slack`. |
| `factory.py` | Crée les notifications avec `NotificationFactory`. |
| `strategies_envoi.py` / `delivery_strategies.py` | Définit les stratégies d’envoi (`DeliveryStrategy`, etc.). |
| `decorateurs.py` / `decorators.py` | Décorateurs de notifications (`NotificationDecorator`, `EncryptedNotification`, etc.). |
| `teste.py` | Démonstration complète de l’application. |
| `test_notifications.py` | Tests automatisés validant l'ensemble des signatures du référentiel. |
| `uml.md` | Diagramme UML Mermaid du projet. |

## 2. Tableau de référence Groupe 1

| Classe | Méthode | Arguments | Retour |
|---|---|---|---|
| `EventPublisher` | `add_observer()` | `observer: EventObserver` | `None` |
| `EventPublisher` | `remove_observer()` | `observer: EventObserver` | `None` |
| `EventPublisher` | `notify_observers()` | `event: CampusEvent` | `None` |
| `EventObserver` | `update()` | `event: CampusEvent` | `None` |
| `NotificationService` | `update()` | `event: CampusEvent` | `None` |
| `NotificationService` | `handle_event()` | `event: CampusEvent` | `None` |
| `NotificationService` | `send()` | `notification: Notification` | `None` |
| `NotificationFactory` | `create()` | `event: CampusEvent, recipient: str` | `Notification` |
| `Notification` | `generate_content()` | `-` | `str` |
| `BaseNotification` | `generate_content()` | `-` | `str` |
| `NotificationDecorator` | `generate_content()` | `-` | `str` |
| `WithSignature` | `generate_content()` | `-` | `str` |
| `WithUrgentHeader` | `generate_content()` | `-` | `str` |
| `EncryptedNotification` | `generate_content()` | `-` | `str` |
| `EncryptedNotification` | `encrypt()` | `-` | `str` |
| `DeliveryStrategy` | `send()` | `notification: Notification` | `None` |
| `SmsDeliveryStrategy` | `send()` | `notification: Notification` | `None` |
| `EmailDeliveryStrategy` | `send()` | `notification: Notification` | `None` |
| `PushDeliveryStrategy` | `send()` | `notification: Notification` | `None` |
| `SlackDeliveryStrategy` | `send()` | `notification: Notification` | `None` |

## 3. Installation et lancement

### Prérequis

- Python **3.10 ou supérieur** ;
- aucune bibliothèque tierce requise (uniquement la bibliothèque standard).

### Exécution des tests

Depuis le dossier `project-notif` :

```bash
python -m unittest discover -v
```

### Lancement de la démonstration

```bash
python teste.py
```

### Vérification de syntaxe

```bash
python -m compileall -q .
```

## 4. Exemple d'utilisation conforme au contrat

```python
from datetime import date
from events import CampusEvent, Incendie
from modules import ModuleAcces, NotificationService
from delivery_strategies import EmailDeliveryStrategy, SmsDeliveryStrategy
from decorateurs import BaseNotification, WithSignature, WithUrgentHeader, EncryptedNotification

# 1. Mise en place du service et de ses stratégies
service = NotificationService([
    EmailDeliveryStrategy(),
    SmsDeliveryStrategy(),
])

# 2. Enregistrement auprès d'un publisher
module_acces = ModuleAcces()
module_acces.add_observer(observer=service)

# 3. Émission d'un événement
module_acces.detecter_incendie(
    date_ev=date.today(),
    desc="Départ de feu détecté",
    localisation="Bâtiment B",
)

# 4. Utilisation du pattern Decorator
notif = BaseNotification("admin@campus.fr", "Alerte système")
notif = WithSignature(notif, "Direction")
notif = WithUrgentHeader(notif)
notif_chiffree = EncryptedNotification(notif)

# Méthode encrypt() sans argument
print(notif_chiffree.encrypt())
# Résultat: [CHIFFRÉ] URGENT\nAlerte système\nSignature : Direction
```
