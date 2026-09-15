# Projet Notifications — SmartCampus

Système de notifications du campus basé sur plusieurs patrons de conception :

- **Observer** : les modules du campus publient des événements et le service de notification les reçoit ;
- **Factory** : création centralisée des notifications ;
- **Strategy** : choix des canaux d’envoi SMS, e-mail, push ou Slack ;
- **Decorator** : ajout dynamique d’une signature, d’un en-tête urgent ou d’un chiffrement.

Le projet est volontairement simple : les stratégies d’envoi simulent actuellement un envoi avec un affichage dans la console. Elles peuvent ensuite être remplacées par de vrais fournisseurs SMS, e-mail, push ou Slack.

## 1. Structure du projet

| Fichier | Rôle |
|---|---|
| `evenements.py` | Définit les événements produits par le campus. |
| `sujets_observateurs.py` | Définit les interfaces Observer : sujet et observateur. |
| `modules.py` | Contient les modules du campus et `ServiceNotification`. |
| `notifications.py` | Définit les types de notifications : SMS, e-mail, push et Slack. |
| `factory.py` | Crée une notification avec `NotificationFactory`. |
| `strategies_envoi.py` | Définit les stratégies d’envoi. |
| `decorateurs.py` | Ajoute des fonctionnalités aux notifications. |
| `teste.py` | Démonstration complète de l’application. |
| `test_notifications.py` | Tests automatisés. |
| `uml.md` | Diagramme UML Mermaid du projet. |

## 2. Installation et lancement

### Prérequis

- Python **3.10 ou supérieur** ;
- aucune bibliothèque externe n’est nécessaire.

Depuis le dossier `project-notif`, lancer la démonstration :

```text
python teste.py
```

Lancer les tests :

```text
python -m unittest discover -v
```

Vérifier la syntaxe de tous les fichiers Python :

```text
python -m compileall -q .
```

## 3. Architecture Observer

### Fonctionnement

1. Un module du campus détecte un événement.
2. Il crée un objet `Evenement` spécialisé.
3. Il conserve l’événement dans son historique.
4. Il notifie tous ses observateurs.
5. `ServiceNotification` reçoit l’événement.
6. Le service crée une notification et la transmet à toutes les stratégies d’envoi.

### Classes principales

| Classe du projet | Nom du contrat Groupe 1 | Responsabilité |
|---|---|---|
| `ModuleCampus` | `EventPublisher` | Sujet observable qui ajoute, retire et notifie des observateurs. |
| `ServiceNotification` | `NotificationService` | Observateur qui traite les événements et envoie les notifications. |
| `Observateur` | `EventObserver` | Interface avec `update(event)`. |
| `ModuleAcces` | — | Produit un événement `Incendie`. |
| `ModuleEcoGestion` | — | Produit un événement `AlerteConso`. |
| `ModuleReservation` | — | Produit un événement `CoursAnnule`. |

Les noms anglais du contrat sont disponibles comme alias. Les noms français historiques restent également utilisables.

### Méthodes Observer

| Classe | Méthode | Arguments | Retour |
|---|---|---|---|
| `ModuleCampus` | `add_observer(observer)` | observateur | `None` |
| `ModuleCampus` | `remove_observer(observer)` | observateur | `None` |
| `ModuleCampus` | `notify_observers(event)` | événement | `None` |
| `ServiceNotification` | `update(event)` | événement | `None` |
| `ServiceNotification` | `handle_event(event)` | événement | `None` |
| `ServiceNotification` | `send(notification)` | notification | `None` |

## 4. Événements du campus

| Classe | Attributs spécifiques |
|---|---|
| `Evenement` | `date`, `description` |
| `Incendie` | `localisation` |
| `AlerteConso` | `niveau`, `consommation` |
| `CoursAnnule` | `nomCours`, `raison` |
| `Salle` | `nom`, méthode `interagir(event)` |

Exemple de création d’un événement :

```python
from datetime import date
from evenements import Incendie

event = Incendie(
	date.today(),
	"Départ de feu détecté",
	"Bâtiment B - Étage 2",
)
```

## 5. Factory des notifications

`NotificationFactory` centralise la construction des notifications et évite de créer directement les classes concrètes dans le reste de l’application.

| Classe | Méthode | Arguments | Retour |
|---|---|---|---|
| `NotificationFactory` | `create(event, recipient)` | événement, destinataire | `Notification` |
| `NotificationFactory` | `creer(type, destinataire, contenu)` | ancienne API française | `Notification` |

Avec le contrat Groupe 1 :

```python
from factory import NotificationFactory

notification = NotificationFactory.create(
	event,
	"admin@campus.fr",
)
print(notification.generate_content())
```

L’appel `create(event, recipient)` crée par défaut une notification e-mail contenant la description de l’événement.

Les types disponibles sont `SMS`, `EMAIL`, `PUSH` et `SLACK` via `TypeNotification`.

## 6. Types de notifications

| Classe | Résultat de `generate_content()` |
|---|---|
| `SMS` | `SMS: ...` |
| `Email` | `EMAIL: ...` |
| `Push` | `PUSH: ...` |
| `Slack` | `SLACK: ...` |
| `BaseNotification` | contenu sans préfixe |

Chaque notification possède :

- `destinataire` : adresse, numéro ou identifiant du destinataire ;
- `contenu` : contenu initial ;
- `generate_content()` : génération du message final.

## 7. Décorateurs

Les décorateurs enveloppent une notification existante sans modifier sa classe originale.

| Décorateur | Fonction |
|---|---|
| `WithSignature` | Ajoute `Signature : ...`. |
| `WithUrgentHeader` | Ajoute l’en-tête `URGENT`. |
| `EncryptedNotification` | Ajoute le marqueur `[CHIFFRÉ]`. |

Exemple de composition :

```python
from decorateurs import (
	BaseNotification,
	WithSignature,
	WithUrgentHeader,
	EncryptedNotification,
)

notification = BaseNotification(
	"admin@campus.fr",
	"Alerte de sécurité maximale.",
)
notification = WithSignature(notification, "Direction du Campus")
notification = WithUrgentHeader(notification)
notification = EncryptedNotification(notification)

print(notification.generate_content())
```

Résultat :

```text
[CHIFFRÉ] URGENT
Alerte de sécurité maximale.
Signature : Direction du Campus
```

## 8. Stratégies d’envoi

| Classe française | Nom du contrat Groupe 1 | Canal |
|---|---|---|
| `EnvoiSMS` | `SmsDeliveryStrategy` | SMS |
| `EnvoiEmail` | `EmailDeliveryStrategy` | E-mail |
| `EnvoiPush` | `PushDeliveryStrategy` | Notification push |
| `EnvoiSlack` | `SlackDeliveryStrategy` | Slack |
| `StrategieEnvoi` | `DeliveryStrategy` | Interface commune |

Chaque stratégie implémente :

```python
send(notification) -> None
```

Le service peut utiliser plusieurs stratégies pour un même événement :

```python
from modules import ServiceNotification
from strategies_envoi import EnvoiEmail, EnvoiSMS

service = ServiceNotification([
	EnvoiEmail(),
	EnvoiSMS(),
])
```

## 9. Exemple complet Observer

```python
from datetime import date

from modules import ModuleAcces, ServiceNotification
from strategies_envoi import EnvoiEmail, EnvoiSMS

module = ModuleAcces()
service = ServiceNotification([
	EnvoiEmail(),
	EnvoiSMS(),
])

module.add_observer(service)
module.detecter_incendie(
	date.today(),
	"Départ de feu détecté au bâtiment B",
	"Bâtiment B - Étage 2",
)
```

Le service reçoit automatiquement l’événement et déclenche les deux stratégies d’envoi.

## 10. Compatibilité des noms

Le projet respecte le tableau Groupe 1 en exposant les noms anglais suivants :

| Contrat Groupe 1 | Implémentation |
|---|---|
| `EventPublisher` | alias de `ModuleCampus` |
| `EventObserver` | alias de `Observateur` |
| `NotificationService` | alias de `ServiceNotification` |
| `DeliveryStrategy` | alias de `StrategieEnvoi` |
| `NotificationFactory.create` | méthode principale de création |
| `Notification.generate_content` | méthode principale de génération |
| `EncryptedNotification.encrypt` | méthode de chiffrement |

Les méthodes françaises `ajouter_observateur`, `retirer_observateur`, `notifier_observateurs`, `mettre_a_jour`, `traiter_evenement`, `envoyer`, `creer`, `generer_contenu` et `chiffrer` sont conservées pour assurer la compatibilité avec le code existant.

## 11. Validation

Le projet contient des tests couvrant :

- la composition des décorateurs ;
- la création par la Factory ;
- l’ajout et le retrait d’un observateur ;
- l’envoi par stratégie ;
- la compatibilité avec l’ancienne API française.

La commande recommandée est :

```text
python -m unittest discover -v
```

Le diagramme complet des relations entre les classes se trouve dans [`uml.md`](uml.md).

## 12. Évolutions possibles

- connecter `EnvoiEmail` à un serveur SMTP ou à un service transactionnel ;
- connecter `EnvoiSMS` à un fournisseur SMS ;
- ajouter une configuration des destinataires par type d’événement ;
- remplacer le chiffrement simulé par un chiffrement réel ;
- ajouter une journalisation structurée et une gestion des erreurs d’envoi ;
- stocker les événements et l’historique des notifications dans une base de données.
