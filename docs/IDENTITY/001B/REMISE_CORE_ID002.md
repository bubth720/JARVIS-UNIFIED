# Remise à CORE ID-002 — gate de revue, aucune activation

Architecture/constitution approuvées à1748cb0 ; **format candidat001B.1 à accepter**.
La revue doit épingler SHA du commit UNIFIED + BUNDLE.json.bundle_sha256, bornes,
styles et vecteurs. Publier ce candidat ne satisfait pas à lui seul le gate ID-002.
Une acceptation ultérieure se consigne séparément, sans modifier les octets normatifs
pour les faire passer rétroactivement pour déjà approuvés.

## Écarts explicites par rapport au draft ID-001

| Draft | Candidat001B.1 / décision à accepter |
|---|---|
| identity_id/schema_version et références libres | id/version/schema_revision, UUID/révisions/digests stricts et bonne sorte référencée |
| Traits/allowed_styles non bornés | Six clés et enums fixes de STYLE_TABLE, B et fr-FR, aucun prompt libre/permission dans manifest |
| IdentityPolicy sérialisable envisagée | Politique effective de confiance **hors manifeste**, policy_revision est référence et non grant ; pas de nouveau schéma de permissions |
| snapshot content_digest | Hash externe D(snapshot), pas hash de soi. Listes de préférences/consents vides dans profil de consommation ID-002 |
| Proposition mutable avec décision/application | Candidat PENDING immuable, événements decision et application séparés ; vue APPROVED/REJECTED calculée et sans cycle de hash |
| Préférences privées et persistance future | Types séparés pour revue, personal-preference EPHEMERAL_ONLY ; aucun writer dans IdentityPort ID-002 |
| Expression et sens critique proposés | Schémas d’intention expressive/Assessment non gelés ici, réservés aux missions suivantes |
| Bases/modèles compatibles encore ouverts | Pas de base CORE imposée, pas de modèle supplémentaire ; revue004D/intermédiaires et tokenizer SYSTEM réel avant consommation |

## Revue de compatibilité requise côté CORE, sans code ici

CORE audité da40ed7155409b85860a22c1dbbfe35029cea29a : InferenceRequest conserve
systemPrompt séparé, session/request IDs, contexte/sources et limites ; validation
actuelle en octets n’est pas un comptage natif réel. SessionCoordinator est
single-flight, stop demandé puis drainage NonCancellable, expiration ≠ fin native.
Le nouveau snapshot se rattache à ces sessions sans créer une session d’autorité
concurrente, ni déduire nativeDone=true depuis une persona.

ID-002 ne doit pas supposer CORE004D opérationnelle, consommer le candidat /2 bloqué,
fusionner automatiquement les bases ou changer le corpus des fixtures. Base réelle
à choisir et SHA à annoncer après revue ; conserver opt-in et application historique
API24 sans nouvelle permission, stockage, moteur ou changement des seuils.

SERVICES0f462c8 : Guard confirme principal/opération/digest/délai60s/usage unique
in-process, Memory.save écrit après consume ; ce n’est pas un stockage IDENTITY
transactionnel déjà raccordé. Aucun accès à ce Context via JSON ou autre APK.
VOICE521e613 : CoreVoiceRequestV1 fermé, identité/profil/pack exacts et300caractères ;
styles SERIOUS/HUMOROUS ne sont pas des modulations acoustiques validées. Rien
n’est ajouté à ses enums/champs. NEXUS/EVOLUTION non opérationnels présumés.

## Checklist d’acceptation avant consommation

1. Accepter version/style B, enums/locale et bornes bytes/listes/profondeur/tokenizer.
2. Accepter proposition immuable et séparation décisions/applications, port strictement
   lecture seule et aucune donnée personnelle persistée sous cette mission.
3. Épingler les14 fichiers normatifs et digest réel du bundle ; vérifier six vecteurs
   dans le futur codec Kotlin/Java de CORE, pas seulement Python/JavaScript.
4. Qualifier l’adaptateur SYSTEM, le budget **rendu total**, l’absence de duplication
   native, les réponses tardives/révocation/cancel et la compatibilité historique.
5. Revoir base CORE et périmètre opt-in ; si format/base pas validés, **ne pas lancer
   un runtime utilisant un contrat prétendument figé**. Aucun bypass pour l’Alpha.

L’accord préparatoire ID-002 reste borné par cette porte. Écritures ID-003, transport,
restauration/migration privée, raccordement et qualification appareils nécessitent
leurs propres décisions. CORE004D possède un autre gate : clarification protocole,
correction LLM et nouveau bundle /2 testé puis revu. Aucun gate ne remplace l’autre.
