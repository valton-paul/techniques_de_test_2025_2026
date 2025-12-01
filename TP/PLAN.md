# Plan de tests — Triangulator (TP 2025/2026)

## Objectifs
- Garantir la conformité des formats binaires `PointSet` et `Triangles`.
- Vérifier la correction de l'algorithme de triangulation.
- Valider l'API Flask (statuts, payloads, erreurs) et l'intégration avec `PointSetManager` (via mocks).
- Mesurer et contrôler les performances des conversions binaires et de l'algorithme.
- Atteindre une couverture de test pertinente et satisfaire `ruff`.

## Périmètre
- Unitaires : parsing binaire, sérialisation, primitives triangulation.
- Intégration : endpoints PointSetManager (/pointset POST, /pointset/{id} GET) et Triangulator (/triangulation/{id} GET).
- Performance : parsing et triangulation sur jeux synthétiques.

## Organisation (arborescence proposée)
- TP/
  - src/
    - triangulator
  - tests/
    - unit/
      - test_binary_format.py
      - test_triangulation_basic.py
      - test_triangulation_edgecases.py
    - integration/
      - test_pointset_api.py
      - test_triangulator_api.py
      - conftest.py
    - perf/
      - test_triangulation_perf.py

## Cas de test Exemple 

### 1) Parsing / Sérialisation (unit)
- parse_pointset_valid
  - Entrée : bytes conforme
  - Attendu : liste de tuples (x, y) avec tolérance flottante
- parse_pointset_too_short
  - Entrée : header N déclaré > données fournies
  - Attendu : ValueError ou custom ParsingError
- parse_empty_pointset
  - Entrée : N == 0
  - Attendu : []
- serialize_pointset_roundtrip
  - Entrée : liste points
  - Attendu : serialize -> parse == original

### 2) Algorithme de triangulation (unit)
- minimal_triangle
  - 3 non-colinéaires points -> 1 triangle, indices distincts
- square_case
  - 4 points carré -> 2 triangles (indices valides)
- collinear_points
  - Plusieurs points alignés -> comportement défini (0 triangles ou erreur)
- duplicate_points
  - Points identiques -> déduplication ou erreur claire
- concave_polygon
  - Forme concave -> triangulation couvrant la surface sans trous/overlap
- invariants
  - chaque triangle a 3 indices distincts, 0 <= idx < N
- randomized_small
  - points aléatoires (répéter) -> vérifier invariants et stabilité

### 3) API HTTP — PointSetManager (integration)
POST /pointset
- post_pointset_valid -> 201 + body/Location/UUID
- post_pointset_empty_body -> 400 + Error JSON
- post_pointset_malformed_binary -> 400 + Error JSON
- post_pointset_storage_down -> 503 + Error JSON

GET /pointset/{id}
- get_pointset_valid -> 200 + application/octet-stream (pointset bytes)
- get_pointset_invalid_uuid -> 400
- get_pointset_not_found -> 404
- get_pointset_storage_down -> 503

### 4) API HTTP — Triangulator (integration)
GET /triangulation/{id}
- triangulation_success
  - Mock PointSetManager returns valid bytes
  - Attendu : 200, Content-Type application/octet-stream, payload Triangles valide
- triangulation_invalid_uuid -> 400
- triangulation_pointset_not_found -> 404 (propagé)
- triangulation_pointset_malformed -> 500 (triangulation fails)
- triangulation_pointsetmanager_unavailable -> 503 (timeout / network error)
- end_to_end_cycle
  - POST -> UUID, puis GET /triangulation/{UUID} -> cohérence bout-à-bout

### 5) Performance (perf)
- parsing_perf
  - N = [1k, 10k, 100k] points, mesurer temps et mémoire
- triangulation_perf
  - N = [1k, 5k, 10k] selon capacité, définir seuils indicatifs
- concurrency
  - plusieurs requêtes simultanées (10-50) pour valider stabilité