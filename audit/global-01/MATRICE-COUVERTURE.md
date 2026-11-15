# Matrice de couverture — exigences → tests → niveau de preuve

**Niveaux de preuve :**

| Niveau | Signification |
|---|---|
| **J** | Test JVM (logique pure) |
| **L** | CI Linux, vrai modèle, pas Android |
| **E** | Émulateur Android API 29 et 35, mode avion, vrai moteur |
| **D** | Appareil réel uniquement (POCO X8 Pro, **non exécuté**) |
| **—** | Aucun test |

**Références des tests :**
- Fichiers JVM : `labs/v3/app/src/test/...` ;
- Tests émulateur : `V3CockpitTest` (tests a à i) ;
- Étude Linux : `JARVIS-LLM conv-01-study.yml`.

**Dernier run émulateur lu :** 43616811194 (2066753). Le run 3dd3649 est en cours.

## Conversation (CONVERSATION-01)

| Exigence | Tests | Niveau | Dernier résultat |
|---|---|---|---|
| Contexte multi-tours au-delà des 3 échanges relus | `ConversationContextTest`, émulateur f | J + E | ✅ 8/8 API 29/35 |
| Corrections de l'utilisateur | `ConversationLayerTest`, f (Marc → Léo) | J + E | ✅ |
| Référence implicite (« ce résultat ») | f (144/4), banc C06 | E + L | ✅ |
| Changement de sujet puis retour | f (âge du frère) | E | ✅ |
| Personnalité Athéna cohérente, jamais « je suis Athéna » | f, i (16 tours) | E | ✅ f ; i en cours |
| Session longue | i | E | ⏳ premier run en cours |
| Questions sans réponse connue / incertitude | banc C08 | L | partiel (0.6B) |
| Hallucinations factuelles | banc factuel 10 questions | L | ❌ 0.6B 2–6/10 (A-004) |
| Fausses déclarations d'action | `ActionGuardTest`, f | J + E | ✅ (A-006) |
| Reprise après fermeture (texte + contexte) | `ConversationLayerTest`, f (reprise UI) | J + E | ✅ |
| Mémoire avec consentement | `MemoryIntentTest`, h | J + E | ✅ API 29 ; API 35 à retester (A-011) |
| Mémoire sans consentement (refus, rien stocké) | h | E | ✅ API 29 |
| Connaissance générale vs réponse documentaire | g, `ProvenanceTest` | E + J | ✅ citée ; absence : note système à retester (A-005) |

## Voix

| Exigence | Tests | Niveau | Dernier résultat |
|---|---|---|---|
| Chaîne micro → STT → LLM → TTS | c (WAV temps réel) | E | ✅ STT ; lecture audio non probante (A-013) |
| Erreur vocale sans doublon | c | E | ✅ (V3-FIX-01) |
| Interruption | c / V1 | E | ✅ logique ; audio réel **D** |
| Réaction d'attente < 5 s | `QuickReaction` règles | J | ✅ règles ; délai réel **D** |
| Vrai micro / haut-parleur / Bluetooth | — | **D** | non validé |

## Interface V3 / Command Center V2 / Avatar

| Exigence | Tests | Niveau | Dernier résultat |
|---|---|---|---|
| Sphère immobile au repos, en réflexion et en écoute ; animée seulement pendant la réponse ; aucun geste | `V3ModelTest`, c, d | J + E | ✅ repos, réflexion, parole ; ❌→⏳ écoute (A-008) |
| Aucun texte tronqué ou superposé | c (TextFit : repos, menu, fiche, paysage, Command Center, palette) | E | ⏳ |
| Menu radial sans chevauchement du champ | `V3ModelTest`, c | J + E | ✅ |
| 10 écrans Command Center, données réelles, « à connecter » | `CommandCenterModelTest`, c | J + E | ⏳ |
| Blueprint = commits réellement épinglés | `CommandCenterModelTest` | J | ✅ |
| Palette : commandes réelles, indisponibles motivées | `CommandPaletteTest`, c | J + E | ⏳ |
| « Pourquoi ? » (provenance) | `ProvenanceTest` | J | ✅ ; E à ajouter |
| Avatar : expressions = état réel, parle seulement en réponse | `AvatarExpressionTest`, c | J + E | ⏳ |
| Rotation, arrière-plan, réouverture après arrêt forcé | c, d, reopen | E | ✅ |
| Accessibilité (TalkBack, liste radiale) | — | — | non testé |
| Tablette / grand écran | — | — | non testé |

## Documents (NEXUS) et mémoire

| Exigence | Tests | Niveau | Dernier résultat |
|---|---|---|---|
| FTS5 disponible (SQLite embarqué) | g | E | ✅ 3.46.0 |
| Réponse citée | g | E | ✅ |
| Document absent : aucune réponse inventée | g | E | ❌ (10 €) → note système, à retester |
| Documents contradictoires, corrompus, mal formatés | — | — | non testé (campagne F) |
| Base incompatible ou corrompue refusée et conservée | probe + en-tête (code) | — | non testé sur Android |
| Injection d'instructions dans un document | — | — | non testé (A-015) |
| Souvenirs : stockage isolé, suppression, rappel nouvelle session | h | E | ✅ API 29 |
| Ambiguïté de rappel (NEEDS_CONFIRMATION) | — | — | ❌ défaut de code (A-010) |

## Robustesse, sécurité, performance

| Exigence | Tests | Niveau | Dernier résultat |
|---|---|---|---|
| Une seule permission (micro), aucune permission Internet | a, inspection APK | E | ✅ |
| Hors ligne (mode avion) | tous les tests E | E | ✅ |
| Permission micro refusée | — | — | non testé |
| Mémoire basse, stockage plein, batterie faible, thermique | gardes (code) | — | non testé (simulation à prévoir) |
| Reprise après plantage | reopen (arrêt forcé) | E | ✅ partiel |
| RAM chargée / libérée (0.6B et 1.7B) | étude Android | E | ✅ 557 / 1 234 Mio PSS |
| Latences réelles, CPU, thermique, batterie | — | **D** | non validé |
| Temps de dessin (sphère V3 vs V1) | e (banc) | E (logiciel) | mesuré, non représentatif d'un GPU réel |

## Modules non intégrés dans l'application

| Module | Niveau de preuve | Commentaire |
|---|---|---|
| SERVICES | CI propre au dépôt (dernière verte le 29/10) | Non connecté à l'application |
| EVOLUTION | CI propre au dépôt (verte le 29/10) | Désactivé (décision du propriétaire) |
| LAB | Workflows `labs/*` existants | Isolation à auditer (campagne B) |
| LEARNING-L01 | — | Non démarré ; PDF de référence manquant |
