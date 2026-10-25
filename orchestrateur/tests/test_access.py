"""
Tests unitaires pour le module de Contrôle d'Accès & Sécurité (Groupe 3 / Intégration Orchestrateur).
Teste :
- AccessRequest et AccessDecision
- SecurityRegistry (permissions)
- Handlers du Chain of Responsibility (AuthenticationHandler, PermissionHandler)
- AccessControlServiceStub (chaîne complète)
"""
import unittest

from orchestrateur.services import (
    AccessRequest,
    AccessDecision,
    SecurityRegistry,
    AccessHandler,
    AuthenticationHandler,
    PermissionHandler,
    AccessControlService,
    AccessControlServiceStub,
)


class TestAccessControl(unittest.TestCase):

    def setUp(self):
        self.security_registry = SecurityRegistry()
        self.access_service = AccessControlServiceStub()

    # --------------------------------------------------------------------------
    # 1. TESTS DES MODÈLES (AccessRequest, AccessDecision)
    # --------------------------------------------------------------------------

    def test_access_request_creation(self):
        req = AccessRequest(user_id="STUDENT_42", resource="Amphi Turing", action="reserve")
        self.assertEqual(req.user_id, "STUDENT_42")
        self.assertEqual(req.resource, "Amphi Turing")
        self.assertEqual(req.action, "reserve")
        self.assertIn("STUDENT_42", str(req))

    def test_access_decision_creation(self):
        decision_ok = AccessDecision(allowed=True, reason="Autorisé")
        self.assertTrue(decision_ok.allowed)
        self.assertEqual(decision_ok.reason, "Autorisé")
        self.assertIn("allowed=True", str(decision_ok))

        decision_ko = AccessDecision(allowed=False, reason="Refusé")
        self.assertFalse(decision_ko.allowed)
        self.assertEqual(decision_ko.reason, "Refusé")

    # --------------------------------------------------------------------------
    # 2. TESTS DU REGISTRE DE SÉCURITÉ (SecurityRegistry)
    # --------------------------------------------------------------------------

    def test_security_registry_permissions(self):
        # Étudiant autorisé sur Amphi Turing en lecture et réservation
        self.assertTrue(self.security_registry.has_permission("STUDENT_42", "Amphi Turing", "reserve"))
        self.assertTrue(self.security_registry.has_permission("STUDENT_42", "Amphi Turing", "read"))

        # Étudiant non autorisé en gestion
        self.assertFalse(self.security_registry.has_permission("STUDENT_42", "Amphi Turing", "manage"))

        # Admin autorisé partout
        self.assertTrue(self.security_registry.has_permission("ADMIN_01", "Amphi Turing", "manage"))
        self.assertTrue(self.security_registry.has_permission("ADMIN_01", "Bibliotheque", "manage"))

        # Utilisateur inconnu ou ressource inconnue
        self.assertFalse(self.security_registry.has_permission("UNKNOWN_USER", "Amphi Turing", "read"))
        self.assertFalse(self.security_registry.has_permission("STUDENT_42", "Salle Inconnue", "read"))

    # --------------------------------------------------------------------------
    # 3. TESTS DES HANDLERS DE LA CHAÎNE (AuthenticationHandler, PermissionHandler)
    # --------------------------------------------------------------------------

    def test_authentication_handler_denies_empty_user(self):
        auth_handler = AuthenticationHandler()
        req_invalid = AccessRequest(user_id="", resource="Amphi Turing", action="read")
        decision = auth_handler.handle(req_invalid)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "Utilisateur non authentifié")

    def test_authentication_handler_allows_valid_user_without_next(self):
        auth_handler = AuthenticationHandler()
        req_valid = AccessRequest(user_id="STUDENT_42", resource="Amphi Turing", action="read")
        decision = auth_handler.handle(req_valid)

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "Utilisateur authentifié")

    def test_permission_handler_verifies_rights(self):
        perm_handler = PermissionHandler(self.security_registry)

        # Autorisé
        req_allowed = AccessRequest(user_id="STUDENT_42", resource="Amphi Turing", action="reserve")
        decision_allowed = perm_handler.handle(req_allowed)
        self.assertTrue(decision_allowed.allowed)
        self.assertEqual(decision_allowed.reason, "Permission accordée")

        # Refusé
        req_denied = AccessRequest(user_id="STUDENT_42", resource="Amphi Turing", action="manage")
        decision_denied = perm_handler.handle(req_denied)
        self.assertFalse(decision_denied.allowed)
        self.assertEqual(decision_denied.reason, "Permission refusée")

    # --------------------------------------------------------------------------
    # 4. TESTS DU SERVICE COMPLET (AccessControlServiceStub - Chaîne de responsabilité)
    # --------------------------------------------------------------------------

    def test_access_control_chain_granted(self):
        # Requête légitime : utilisateur authentifié avec les bonnes permissions
        req = AccessRequest(user_id="STUDENT_42", resource="Amphi Turing", action="reserve")
        decision = self.access_service.check_access(req)

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "Permission accordée")

    def test_access_control_chain_denied_unauthenticated(self):
        # Requête sans user_id -> rejeté au 1er maillon (AuthenticationHandler)
        req = AccessRequest(user_id="", resource="Amphi Turing", action="reserve")
        decision = self.access_service.check_access(req)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "Utilisateur non authentifié")

    def test_access_control_chain_denied_forbidden_action(self):
        # Requête authentifiée mais action interdite -> rejeté au 2e maillon (PermissionHandler)
        req = AccessRequest(user_id="STUDENT_42", resource="Amphi Turing", action="manage")
        decision = self.access_service.check_access(req)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "Permission refusée")

    def test_access_control_chain_denied_unknown_user(self):
        # Utilisateur qui n'existe pas dans le registre
        req = AccessRequest(user_id="GUEST_99", resource="Amphi Turing", action="read")
        decision = self.access_service.check_access(req)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "Permission refusée")


if __name__ == "__main__":
    unittest.main()
