# ARCH-01 — Architecture distribuée JARVIS MOBILE + JARVIS CENTRAL

Statut : **validation architecturale**. Aucun moteur n'est remplacé, aucun modèle n'est téléchargé, aucune connexion réseau n'est active. Ce document décrit une cible et les contrats qui la rendent possible. Il ne décrit pas un fonctionnement réel.

Référence demandée : « JARVIS_Vision_Architecture_Cahier_des_Charges_2026 ». Ce document est **introuvable** dans les huit dépôts (toutes branches) et dans les fichiers transmis. ARCH-01 s'appuie donc sur l'ordre de mission ARCH-01 et sur `ARCHITECTURE.md` (profils TABLET / MOBILE / CENTRAL, section « Futur mode hybride »). À réconcilier dès que le document sera fourni.

## 1. Vue d'ensemble

```
             ┌──────────────────────── JARVIS MOBILE (Android, autonome, hors ligne) ─────────────────────────┐
             │ INTERFACE ─▶ CORE (orchestrateur, autorité session / historique / souvenirs)                    │
             │                │  ├─ CapabilityRegistry ◀── descripteurs + santé (battement) des moteurs        │
             │                │  └─ Router ─────────────┬─▶ ModelBackend « android-local » (A02 + Qwen3 0.6B)    │
             │ VOICE, NEXUS, SERVICES, EVOLUTION        │     via LegacyLocalModelBackend (moteur actuel inchangé) │
             │ (ports existants, inchangés)             └─▶ ModelBackend « pc-* » (proxy de liaison) ──┐        │
             └──────────────────────────────────────────────────────────────────────────────────────────│────────┘
                       variante Android SÉPARÉE avec permission réseau, appairage, chiffrement          │ LAN local
             ┌──────────────────────── JARVIS CENTRAL (PC du propriétaire, futur) ──────────────────────▼────────┐
             │ Hôte de moteurs : ModelBackend « pc-* » (llama.cpp, autre…) ; aucune autorité sur la mémoire     │
             │ Peut proposer des souvenirs, jamais les confirmer ; ne pilote jamais le téléphone              │
             └──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Principes :
1. **Le téléphone reste autonome.** La variante Android locale (V1 / V3 actuelles) n'a aucune permission réseau et fonctionne seule avec le modèle local. Le PC est un accélérateur optionnel, jamais une dépendance.
2. **CORE décide, les moteurs exécutent.** SERVICES, VOICE, NEXUS et INTERFACE parlent à CORE, jamais à un moteur. Ajouter un moteur PC revient à ajouter un descripteur et une implémentation de `ModelBackend` : aucun service n'est reconstruit.
3. **Autorisation explicite et minimale.** Par défaut, le PC n'est pas autorisé. Le propriétaire autorise le PC et les classes de données qui peuvent y aller. Les données `sensitive` restent sur le téléphone.
4. **Aucun cloud.** Le contrat n'a pas de valeur `CLOUD` : un moteur distant sur Internet n'est pas exprimable.
5. **Pas de bascule silencieuse.** Une requête en cours reste liée à son moteur. Si le PC disparaît, elle est déclarée interrompue, jamais rejouée en douce. Le tour suivant est routé à nouveau, vers le téléphone.

## 2. Rôles des modules dans les deux environnements

| Module | JARVIS MOBILE (Android) | JARVIS CENTRAL (PC) | Contrat de liaison |
|---|---|---|---|
| CORE | Orchestrateur, registre, routeur, autorité mémoire | Pas de CORE autonome en V-next : le PC est un hôte de moteurs | `ModelBackend`, `CapabilityRegistry`, `Router` |
| LLM | Moteur A02 scellé + Qwen3-0.6B (V1), candidat 1.7B | Moteurs puissants futurs (taille non choisie : à qualifier) | `ModelBackend` |
| INTERFACE | Cockpit V1/V3 ; affiche l'emplacement du moteur (téléphone/PC) | — | états observables CORE |
| VOICE | Pocket TTS + whisper.cpp sur l'appareil | Option future : TTS/STT PC (profils non universels) | contrats v1 `speech.*` (inchangés) |
| NEXUS | Connaissances locales (KnowledgeReadPort) | Option future : index plus gros, toujours lu via CORE | `document.retrieve` v1 |
| SERVICES | Bots/outils via `tool.invoke` | Outils lourds possibles | `required_tools` du routage |
| EVOLUTION | Télémétrie locale, diagnostics (désactivé V1) | Analyse des mesures (proposition, jamais d'action autonome) | `Module`/`EventCode` existants |

## 3. Flux d'une requête

1. CORE construit une `GenerationRequest` : mêmes champs que l'`InferenceRequest` v1 de CORE, plus les modalités et outils requis et la classe de données.
2. `Router.select` lit le `CapabilityRegistry`. Un moteur est éligible s'il remplit toutes les conditions suivantes :
   - disponibilité fraîche (battement de moins de `ttl_ms`) ; `UNKNOWN` n'est jamais éligible ;
   - autorisation du PC et classe de données permise ;
   - validation identique à `validateInference` de CORE (budget, prompt système séparé, version) ;
   - modalités et outils couverts.
3. Classement : PC préféré s'il est autorisé, puis disponible avant dégradé, puis latence **mesurée** uniquement. Une performance déclarée ne classe rien.
4. `begin` lie la requête au moteur ; `end` la libère. Une perte de moteur rend la liste des requêtes interrompues.
5. Si aucun moteur n'est éligible : refus explicite `NO_ELIGIBLE_BACKEND`, avec la raison de chaque exclusion. Jamais de dégradation silencieuse : une demande trop grande pour le téléphone n'est pas tronquée en douce.

## 4. Liaison PC ↔ Android (contrat seulement)

- Transport futur : LAN local uniquement, appairage hors bande confirmé par le propriétaire, authentification mutuelle, chiffrement, pas de relais, pas de découverte automatique, pas d'exposition du serveur loopback existant.
- Protocole 2.x, négociation par `HELLO` ; un écart de version majeure est refusé.
- Numéros de séquence strictement croissants (anti-rejeu) ; taille maximale 64 Kio par message (les documents voyagent par référence) ; champs interdits (`url`, `path`, `token`…).
- Le délai voyage comme un **délai restant borné**, appliqué avec l'horloge du receveur. Une deadline monotone ne traverse pas les machines.
- Rôles :
  - le téléphone envoie `GENERATE`, `CANCEL` et `MEMORY_SNAPSHOT` ;
  - le PC envoie `CAPABILITIES`, `CHUNK`, `COMPLETE` et `MEMORY_PROPOSAL` ;
  - un PC ne peut ni piloter le téléphone ni imposer un souvenir.
- `CANCEL` est idempotent ; les fragments arrivés après annulation sont ignorés ; l'ordre des fragments est vérifié.
- Garde architecturale : `NETWORK_TRANSPORT_ENABLED = False`. Aucun transport réseau n'existe dans ce dépôt.

## 5. Synchronisation mémoire

- Autorité unique : CORE sur le téléphone. Le PC est un réplica partiel.
- Le PC **propose**. La confirmation se fait sur le téléphone, par un geste du propriétaire lié à `proposal_id` + empreinte exacte du texte + session. Un texte modifié ou une autre session impose une nouvelle confirmation.
- Une proposition fondée sur une révision périmée est rejetée (`CONFLICT`). Une suppression sur le téléphone l'emporte (`DELETED_WINS`) et se propage au PC comme marqueur de suppression.
- Le PC ne reçoit que les souvenirs confirmés que le propriétaire a explicitement marqués partageables (par défaut : aucun).

## 6. Ce qu'ARCH-01 ne fait pas

- Pas de moteur PC, pas de modèle, pas de téléchargement.
- Pas de transport réseau, pas de permission Android ajoutée, pas de nouvelle variante d'APK.
- Aucune modification de CORE, LLM, INTERFACE, VOICE, NEXUS, SERVICES ou EVOLUTION. L'adaptateur Kotlin réel sera écrit dans CORE par une mission dédiée, autorisée explicitement.
- Pas de garantie de performance : un moteur PC n'est classé qu'après mesures réelles.
