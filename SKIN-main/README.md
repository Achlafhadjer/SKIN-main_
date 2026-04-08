# Skin AI Microservices

Projet microservices complet avec exigences pédagogiques.

## Architecture

- `traefik` : reverse proxy + load balancer
- `consul` : registry / service discovery
- `rabbitmq` : message queue / asynchrone
- `postgres` : base de données métier
- `auth` : authentification _JWT_ et rôles (`user` / `admin`)
- `api` : service métier REST CRUD patients + analyses + publication RabbitMQ
- `ml` : service prédiction deep learning via `/api/predict/`
- `worker` : worker asynchrone RabbitMQ pour exécuter le modèle ML
- `web` : UI statique (Nginx) et front-end JS (depuis ../frond-end)

## Points couverts (vérifiés)

1. Application REST métier (CRUD patients, analyses)
2. Service d'authentification JWT (inscription/login, token, rôles)
3. UI web + authentification / appels API
4. Communication asynchrone RabbitMQ (`skin_predictions`)
5. Service registry Consul (services s'enregistrent à démarrage)
6. Reverse proxy Traefik pour routage dynamique
7. Déploiement multi-services (containers indépendants)

## Deep Learning (entraînement local)

- Hyperparamètres : `ml/training/config.yaml`
- Script : `ml/training/skin_disease_classifier.py`
- Dépendances entraînement : `pip install -r ml/training/requirements-training.txt`
- Notebook : `notebooks/01_skin_lesions_deep_learning.ipynb`
- Après entraînement, copiez le `.h5` attendu par Docker : fichier `skin_disease_model_final.h5` **au même niveau que le dossier du dépôt** (voir `docker-compose.yml`, volume du service `ml`), ou définissez `MODEL_PATH` sur le conteneur.

## Exécution locale (Docker)

1. À la racine du dépôt (dossier contenant `docker-compose.yml`).
2. Démarrer :

```bash
docker compose up --build -d
```

3. Vérifier état:

```bash
docker compose ps
```

4. Accéder UI:

- http://localhost/
- traefik dashboard: http://localhost:8080
- consul UI: http://localhost:8500
- rabbitmq UI: http://localhost:15672  (login `skin` / `skin_secret`)

## Endpoints utiles

### Auth
- POST `/auth/register` body JSON `{ "email": "user@example.com", "password": "...", "role": "user" }` (`role` optionnel, défaut `user`)
- POST `/auth/login` form-data OAuth2 : champs `username` (**votre email**), `password`
- GET `/auth/me`, `/auth/verify` (token bearer)

### API métier
- GET `/api/v1/patients`
- POST `/api/v1/patients` body `{ "name": "Nom", "notes": "..." }`
- GET `/api/v1/analyses`
- POST `/api/v1/analyses` (multipart image + patient_id)

### ML
- POST `/ml/api/predict/` (multipart image)
- GET `/ml/api/health`

### Worker asynchrone
- Le `worker` consomme RabbitMQ queue `skin_predictions` et met à jour la table `analyses`.

## Tests rapides

1. Créer utilisateur et login, récupérer token.
2. Créer patient, lister patients.
3. Upload analyse, vérifier `list_analyses` en attente + worker traite et peut-être résultat.
4. Vérifier routes KS via Traefik (bande passante 80 et path rewrite).
5. Smoke test stack (API/Auth/ML/Consul/RabbitMQ) :

```bash
python scripts/smoke_test_stack.py
```

## Remise (conforme au cahier des charges)

- Rapport technique + présentation: à compléter selon consignes enseignant.
- Déploiement multi-serveurs: architecture prête, en production déployer chaque service sur VM/container distinct.
- Trame de preuve multi-serveurs : `docs/PREUVE_MULTI_SERVEURS.md`.

## Remarques d'intégrité

- Sans fichier de poids, le service `ml` démarre avec `model_loaded: false`. Le compose monte optionnellement `../skin_disease_model_final.h5` vers `/app/training_artifacts/skin_model_best.h5`.
- UI : dossier `frond-end/` (build Docker `web`).
- Conformité détaillée : `docs/CONFORMITE_CHECKLIST.md`.
