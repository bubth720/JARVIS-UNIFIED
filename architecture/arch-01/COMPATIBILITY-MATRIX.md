# Matrice de compatibilité des modules existants avec l'architecture PC + Android

Audit en lecture seule des huit dépôts (13/11/2026), sur les branches de développement les plus récentes : V1 livrée, M55, finals. « Compatible » signifie que le module n'a **pas besoin d'être modifié** pour que l'architecture soit valide. Cela ne veut pas dire que l'intégration PC est réalisée.

| Module | Dépôt / référence auditée | Contrat existant pertinent | Compatibilité ARCH-01 | Adaptation future |
|---|---|---|---|---|
| CORE | JAVIS-Local-v2 `5da9838` (épinglé par la V1) | `LocalLanguageModel`, `InferenceRequest`, `InferenceCapabilities`, `InferenceRefusal`, `StopResult`, `UnloadResult`, `SessionCoordinator` | **Compatible** : enveloppé par `LegacyLocalModelBackend` ; méthodes et valeurs vérifiées par test contre l'historique Git | Mission d'implémentation : `ModelBackend` Kotlin + registre + routeur dans CORE ; `SessionCoordinator` appelle le routeur au lieu du moteur unique |
| LLM | JARVIS-LLM `2e01177` (V1), `m55-b` (1.7B étudié) | moteur A02 scellé, contrat A02 v1, manifestes de modèles épinglés (SHA) | **Compatible** : devient le backend `android-local` ; manifestes réutilisables pour `ModelIdentity` | Mesures réelles (p50/p95) pour `Performance.measured` ; aucun changement du moteur |
| INTERFACE | JARVIS-INTERFACE V1 `9599d99`, V3 `labs/v3` | états observables CORE (cockpit) | **Compatible** : consomme des états, ne commande pas le moteur | Afficher l'emplacement du moteur et l'état de la liaison (sans nouvel état du moteur) |
| VOICE | JARVIS-VOICE `92d0745` (Pocket), `voiceBridgeContract` | `VoiceRendererPort`, `AuthorizationPort`, `CoreVoiceRequestV1` | **Compatible** : indépendant du moteur texte | Option : TTS/STT côté PC, avec la même règle (profils non universels, consentement) |
| NEXUS | JARVIS-NEXUS `feat/nexus-final-01` | `KnowledgeReadPort`, `CatalogResult`, `KnowledgeError` | **Compatible** : lu par CORE ; fournit le `context` de la requête | Les documents voyagent par référence (taille de liaison limitée à 64 Kio) |
| SERVICES | JARVIS-SERVICES `feat/services-final-01` | `RequestEnvelope` v1 (desktop), ports Android SAF | **Compatible** : les bots appellent CORE ; `required_tools` route vers un moteur capable | Déclarer les identifiants d'outils dans `capabilities.tools` ; la confirmation des actions reste sous CORE |
| EVOLUTION | JARVIS-VOLUTION- `feat/evolution-final-01` | `Module`, `EventCode`, `MeasurementOrigin` (HOST_OBSERVATION / SYNTHETIC) | **Compatible** : la télémétrie alimente `Performance.measured` sans agir | Reste désactivé ; ne pilote jamais le routage |
| UNIFIED | `contracts/v1` (5 schémas), `ARCHITECTURE.md` | capability-manifest, request/response-envelope, resource-lease, health-status | **Partiellement compatible** : v1 fermé ; `platform` sans windows ; `offline_required: true` | Contrats v2 négociés (voir RISQUES) ; pas de modification de v1 |

## Points vérifiés par test (`tooling/arch01/tests`)

- L'adaptateur couvre exactement les méthodes de `LocalLanguageModel` (CORE `5da9838`). Les valeurs de `StopResult`, `UnloadResult` et `InferenceRefusal` ainsi que les valeurs par défaut 2048/256 sont identiques. Les empreintes de blobs Git sont vérifiables avec `ARCH01_CORE_REPO`.
- La validation reproduit les refus `CONTRACT`, `SYSTEM_PROMPT` et `BUDGET` de CORE, avec la même règle d'octets et le même rendu de prompt.
- Le paquet de contrats n'importe aucune bibliothèque réseau ou processus et ne référence aucun modèle ni URL (vérification statique).
