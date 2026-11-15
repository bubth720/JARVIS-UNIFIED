# Contrat technique `ModelBackend` (version 2.0.0-draft)

Référence exécutable : `tooling/arch01/` (Python standard, aucune dépendance). Tests : `tooling/arch01/tests/`, uniquement sur des moteurs simulés. Le contrat v1 de UNIFIED est fermé (`contracts/v1/SEMANTICS.md`) : ce contrat est une **v2 à négocier**, sans déploiement.

## 1. Interface cible (Kotlin, pour la mission d'implémentation future)

```kotlin
interface ModelBackend {
    fun descriptor(): BackendDescriptor
    fun health(nowMs: Long): Health
    /** Valide comme validateInference (CORE), diffuse le texte dans l'ordre, renvoie le résultat complet.
     *  Lève InferenceRejected(refusal) ; ne renvoie jamais un succès accompagné d'une erreur. */
    suspend fun generate(request: GenerationRequest, onText: (String) -> Unit): GenerationResult
    /** Idempotent. Une demande d'arrêt n'est ni la fin du travail natif ni une libération. */
    fun requestStop(requestId: String): StopResult           // = CORE StopResult
    /** Seul CONFIRMED autorise le chargement d'un autre moteur lourd dans le même processus. */
    suspend fun release(): UnloadResult                      // = CORE UnloadResult
}
```

Le moteur actuel est **enveloppé** par `LegacyLocalModelBackend` : délégation 1:1 vers `LocalLanguageModel` (CORE `5da9838`, blobs `c54f469c` et `87df84dd`).
- Le prompt système reste un argument séparé.
- Pas de flux : le texte est livré en un seul fragment.
- Valeurs par défaut 2048 / 256.
- Une libération `UNKNOWN` rend le moteur `DEGRADED` et non routable, comme le veut la règle CORE « must never authorize switching ».

## 2. Descripteur et registre de capacités

| Champ | Sens | Règle |
|---|---|---|
| `backend_id` | identifiant stable | un autre modèle sous le même id provoque un retrait puis un réenregistrement |
| `location` | `on_device` \| `pc_local` | **pas de `cloud`** |
| `platform` | android, linux, windows, macos | `on_device` ⇒ android ; windows et macos sont nouveaux en v2 |
| `model` | SHA-256, famille, paramètres, quantification, licence | le SHA identifie le modèle, jamais le nom |
| `capabilities.max_context_tokens` / `max_output_tokens` | limites qualifiées | la requête prend le minimum, jamais une hausse |
| `capabilities.memory_available_bytes` | mémoire disponible | `None` = inconnu, pas illimité |
| `capabilities.modalities` | text_in/out, image_in, audio_in, tool_calls, embeddings | toutes les modalités requises doivent être couvertes |
| `capabilities.tools` | identifiants d'outils SERVICES appelables | tous les outils requis doivent être couverts |
| `capabilities.streaming`, `cancellation`, `separate_system_prompt` | comportements | prompt système non séparé ⇒ refus `SYSTEM_PROMPT` |
| `performance` | origine (mesuré / déclaré / inconnu), 1er jeton p50/p95, jetons/s, nombre d'échantillons, appareil | seul `measured` avec au moins 5 échantillons sert au classement |
| `qualification` | valeurs v1 (unknown … physical_verified) | une capacité annoncée n'autorise pas son appel |
| santé | available / degraded / unavailable / unknown, horodatée par le registre | périmée au-delà de `ttl_ms` ⇒ `unknown` ⇒ non éligible ; battements désordonnés ignorés |

## 3. Requête

`GenerationRequest` reprend les champs de l'`InferenceRequest` CORE v1 :
- `session_id`, `request_id`, `system_prompt`, `question`, `context`, `contextSize`, `maxTokens`, `contract_version = 1` ;
- rendu de prompt identique à `renderPrompt()`.

Elle ajoute :
- `required_modalities` et `required_tools`, pour la compatibilité avec les futurs bots SERVICES ;
- `data_class` : public, personal ou sensitive.

## 4. Refus

Ce sont les refus de CORE, inchangés :
- `BUSY`, `CONTRACT`, `SYSTEM_PROMPT`, `BUDGET` ;
- `STALE_RESPONSE`, `STOP_REQUESTED`, `RELEASE_UNCONFIRMED` ;
- `DELEGATE_DISABLED`, `PROCESS_ENGINE_HELD`.

S'y ajoutent `MODALITY` et `NO_ELIGIBLE_BACKEND` pour le routage.

Les erreurs de liaison sont des codes fermés :
- `NOT_PAIRED`, `VERSION_MAJOR`, `NO_HELLO`, `KIND_NOT_ALLOWED` ;
- `REPLAY`, `TOO_LARGE`, `FORBIDDEN_FIELD`, `DEADLINE`, `CHUNK_ORDER` ;
- `NETWORK_DISABLED`.

## 5. Politique de routage (`RoutingPolicy`, choix du propriétaire)

- `pc_authorized = false` par défaut.
- `pc_data_classes = {public, personal}` ; `sensitive` reste toujours sur le téléphone.
- `prefer_pc = true` ; `accept_degraded = false`.
- Une requête en cours n'est jamais re-routée. En cas de perte du moteur, elle est rapportée interrompue et n'est pas rejouée.

## 6. Correspondance avec les contrats v1 existants

| v1 (UNIFIED) | v2-draft (ARCH-01) |
|---|---|
| `capability-manifest` : `platform` ∈ {android, linux, unknown}, `offline_required: true` | `platform` + windows/macos ; « hors ligne » précisé : sans Internet, LAN local appairé autorisé seulement dans la variante hybride |
| `request-envelope.limits` (max_output_tokens, timeout_ms, declared_memory_bytes) | `GenerationRequest` + `remaining_ms` sur la liaison |
| `health-status` (unknown ≠ OK) | `Health` + fraîcheur `ttl_ms` |
| `resource-lease` (stop ≠ fin native ≠ libération) | `requestStop` / `release` + blocage si `RELEASE_UNCONFIRMED` |
| `text.generate` exige le digest du modèle | `ModelIdentity.sha256` obligatoire |
