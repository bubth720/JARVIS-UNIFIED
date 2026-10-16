# D4-02 — décisions à approuver et prochaines missions ordonnées

**Propositions techniques, aucun accord nouveau enregistré.** L’orientation ADR
option3 est déjà approuvée : elle ne doit pas être soumise une seconde fois.
Les décisions ci-dessous ne sont pas une autorisation d’intégrer ou déployer.

## Décisions à soumettre dans l’ordre

| Ordre / décision | Recommandation précise | Alternative / conséquence | Accord nécessaire |
|---|---|---|---|
| O1 Propriété et réemploi | Approuver la matrice : CORE autorité, LLM seul catalogue/moteur cible, VOICE coffre/synthèse, SERVICES fournisseurs, NEXUS façade stockage future | Une mémoire ou orchestration autonome concurrente SERVICES contredirait les frontières ADR ; transfert à NEXUS sans réemploi dupliquerait | Validation de la matrice proposée ; aucune migration incluse |
| O2 Premier pilote et prompt | Texte synthétique CORE↔LLM uniquement ; P2 port système versionné pour parité ; P1 fixture native limitée possible pour première preuve | Ignorer systemPrompt CORE est exclu ; P1 ne valide pas parité fonctionnelle et doit refuser demandes non représentables | Politique de prompt, mapping et évolution de contrat séparés ; pas de modification v1 automatique |
| O3 Transport Android/identité | Étudier Bound Service Binder explicite pour fixtures API29+, avec identités vérifiées, applications existantes conservées | Bibliothèque intra-app = extraction/build plus intrusifs ; permission signature inopérante si certificats différents | Choix transport et stratégie de confiance, sans re-signing ; API24–28 mode historique |
| O4 Ressources et cycle de vie | Un seul moteur résident et un lourd pour le pilote ; mode sélectionné avant warm-up ; tous participants valident admission et fin | Gate CORE seul insuffisant, fallback immédiat après timeout interdit ; futur multi-modèle exige qualification | Choisir emplacement/implémentation de l’arbitre, contrat end/unload et comportement en panne |
| O5 Qualification et activation | Fixtures puis émulateur IPC, puis paire réelle d’APK autorisée et modèles déjà locaux | CI verte ne suffit pas ; appareil refusant admission reste non qualifié | Accords distincts par dépôt pour code, puis installation/essai ; fusion/déploiement ultérieurs séparés |

O1 est indépendante de D4-01 PC/montre. O3 doit être coordonnée avec D4-01 et
VOICE005K, sans les attendre pour achever la présente documentation ou faire
l’inventaire. Aucune identité installée ou plateforme montre n’est devinée.

## Missions courtes proposées, une autorisation et un dépôt chacune

| Ordre / dépôt / branche suggérée | Objectif et livrables bornés | Dépendances / critères d’acceptation / non-régression |
|---|---|---|
| 1 UNIFIED / decision/d4-02-technical | Consigner uniquement les décisions O1–O4 réellement prises ; version et erreurs du protocole proposées à relire | Réponse utilisateur explicite, ne pas convertir recommandations en accords ; pas de runtime ni modification de schéma sans autorisation |
| 2 CORE / contract/inference-lifecycle | Repartir004A après vérification ; préciser le port LocalLanguageModel et factory exclusive, tests cycle de vie avec faux backend | O2/O4 + autorisation CORE ; aucun préchauffage legacy en mode de fixture délégué, annulation/retour tardif/bail bloqué testés ; préserver004A140 tests rapportés, ne pas les refaire de zéro |
| 3 LLM / contract/core-generation | Depuis003C vérifier préservation003B, définir mapping système/messages/budget et contrôle de cycle de vie ; tests purs et guards existants | O2/O4 + autorisation LLM ; pas de nouveau moteur ni seuil changé, pas d’IPC exposé avant O3 ; conserver56 domaine/21 simulés/CTest rapportés, tests natifs distincts |
| 4 UNIFIED / decision/android-pilot-trust | Note O3 : vrais certificats de fixtures, API et surfaces minimales, protocole d’admission inter-APK, pairing PC séparé | Analyses2/3 et VOICE005K, inventaire technique de clés sans divulgation ; validation humaine du transport/auth/arbitre, pas nouveau choix ADR |
| 5 LLM / fixture/core-endpoint | Endpoint isolé aux fixtures, réutilise backend et garde complets ; tests IPC négatifs puis vrai natif si autorisé | O3/O4 et missions2/3 ; contrôle d’identité, état opération, stop/unload/cleanup_failed ; aucune modification de l’APK utilisateur installée sans accord |
| 6 CORE / fixture/llm-client | Client de fixture vers endpoint5, demande synthétique et réponse corrélée ; conserver mode historique exclusif | Contrat/digest et deux SHA alignés ; preuve des deux processus et backend réel, aucun service SERVICES/VOICE/NEXUS requis ; pas de fallback automatique |
| 7 CORE / qualification/llm-e2e | Essai matériel bref autorisé, logs minimisés et recette de non-régression à la paire précise | Qualification LLM003C toujours en attente physique ; consentement installation ; mode avion, arrêt effectif, PSS/budgets et repos ; refus conservé, aucun stress ni baisse de seuil. Code LLM inchangé pendant cette mission CORE |
| 8 SERVICES / design/nexus-reuse-002b | Inventaire de réemploi DOCUMENTS/KNOWLEDGE/MEMORY/Guard, mappings de namespaces et port LlmPort honnête | O1, coordination avec002A/002B déjà annoncée, ne pas refaire fondations ; tests de refus/hôte simulé sans raccorder CORE. Aucun second catalogue/moteur ni transfert de données |
| 9 NEXUS / design/canonical-store | Spécifier façade objets/propriétaire/révision, dépendances aux bibliothèques SERVICES, stratégie backup/restore |8, O1 et accord propre NEXUS ; pas d’import de SQLite réel, aucun copier-coller massif. Toute migration reste une mission ultérieure autorisée |
| 10 VOICE / design/005k-alignment | Compléter005K existant avec protocole de ressources/session retenu, sans refaire Studio ou coffre | O3/O4 et futur parcours texte qualifié ; aucune migration de profil, UI/lecture existantes conservées, raccordement réel dans missions CORE/VOICE séparées |
| Parallèle LLM / expressions/pilot-060 | D4-03 :20 intentions/60 variantes littérales dans le catalogue existant | Autorisation LLM propre, ne dépend pas du futur E2E ; import atomique/clarification/négation/suppression et aucune charge de modèle sur réponse simple |

Les chemins précis des nouveaux fichiers d’adaptateur seront fixés dans les dépôts
propriétaires après choix techniques, pas inventés comme API actuelle. Les points
d’entrée existants sont dans ADAPTATIONS_ET_CONTRATS.md. Une mission ne donne
jamais le droit d’éditer deux dépôts. Les signatures et modèles utilisés pour une
recette ne sont pas ceux d’un autre run supposés compatibles.

## Prochaine action recommandée

Examiner O1 puis O2/O4 ; préciser O3 avec la note de confiance Android. Autoriser
ensuite2 et3 séparément, tests de cycle de vie d’abord. Aucune autorisation de
code n’est demandée comme condition pour terminer D4-02 : la mission documentaire
est livrée complète. L’intégration réelle reste bloquée volontairement par ces
décisions et qualifications, pas par un besoin de relancer l’orientation ADR.
