# UNI-01 — livraison du générateur de contrats

- Module UNIFIED ; dépôt `bubth720/JARVIS-UNIFIED`.
- Branche `feat/uni-01-tooling`, départ planning
  `ef1592e9598e14d2245539e2453bf26d7f26969d` contenant la base technique
  `8ddac8fe8a1861a27d3abeca81eb4ab8f110c3a9`.
- SHA final : commit contenant ce rapport, à obtenir avec `git log -1` sur cette
  branche ; pas de faux SHA autoréférent. Aucune PR ou fusion nécessaire.

Programmation : lecteur strict des schémas, manifestes adressés par SHA-256,
générateur déterministe, cinq DTO Java immuables avec enums/objets imbriqués,
cinq façades Kotlin, codec JSON strict et validations structurelles/sémantiques,
CLI `generate`/`verify-contract`. Fichiers dans `tooling/contracts`, sorties
`contracts/generated`, tests `tests/contract_tooling`.

Vérifications réellement exécutées le22octobre2026 en cloud Linux x86_64 :

- `python3 -m unittest discover -s tests/contract_tooling -v` :11/11 réussis.
- `python3 -m tooling.contracts.verify_jvm` avec JDK17.0.16+8/Kotlin2.0.21 local :
  compilation réelle des sources Java/Kotlin,40 vérifications Java et5 aller-retour
  Kotlin réussis. Exemples valides/invalides, clés inconnues/dupliquées, immutabilité,
  UTF-8/surrogates, Unicode canonique, limites, délais, empreinte modèle,
  fausse libération et réponse tardive sont vérifiés.
- Deux générations comparées octet par octet ; sources versionnées identiques.
- `scripts/validate_unified.py` :5 contrats/5 exemples valides/5 refus/9 dépôts.
- Suites historiques audit/contrats et registre conservées ; résultat détaillé
  communiqué dans le bilan de campagne.
- `git diff --exit-code -- contracts/v1` : aucune modification des contrats figés.

Première compilation a révélé une accolade manquante dans les objets imbriqués du
générateur ; corrigée avant livraison puis compilations et vecteurs réexécutés.
Les parseurs générés ne sont pas liés à CORE/LLM/VOICE ; aucun transport, moteur,
permission, poids, test Android physique ou preuve JNI ajouté. Les protections et
archives historiques sont conservées. Kotlin/Java doivent encore être qualifiés
dans chaque consommateur Android avant adoption.

Prochaine mission : UNI-02, registre exécutable de dépendances et de preuves.
