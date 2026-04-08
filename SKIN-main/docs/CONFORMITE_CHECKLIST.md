# Conformité aux consignes (Deep Learning + WAMS)

Ce document croise les **exigences usuelles** des documents « Feuille de route Mini-Projet Deep Learning » et « Projet WAMS » avec l’implémentation du dépôt. Si votre PDF impose un point précis (framework imposé, nombre de pages du rapport, etc.), vérifiez-le manuellement.

## Deep Learning — satisfait

| Exigence typique | Implémentation |
|------------------|----------------|
| Jeu de données + chargement | Hugging Face `ahmed-ai/skin-lesions-classification-dataset` (`skin_disease_classifier.py`) |
| Prétraitement / normalisation | Redimensionnement 224×224, valeurs [0,1] |
| Augmentation | `RandomFlip`, `RandomRotation`, `RandomZoom`, `RandomHeight`, `RandomWidth` |
| CNN / transfer learning | MobileNetV2 (ImageNet), tête dense + softmax |
| Fine-tuning | Déblocage du backbone, learning rate bas (configurable) |
| Train / validation | Splits HF `train` + `validation` ou `test` |
| Callbacks | Early stopping, `ModelCheckpoint` |
| Courbes loss / accuracy | `training_curves.png` dans `ml/training/training_artifacts/` |
| Métriques | Matrice de confusion, `classification_report` (P/R/F1) |
| Artefacts pour déploiement | `skin_model_best.h5`, `class_names.json` |
| Fichier de configuration | `ml/training/config.yaml` |
| Notebook pédagogique | `notebooks/01_skin_lesions_deep_learning.ipynb` |
| Service d’inférence | FastAPI `ml/main.py` — `POST /api/predict/`, `GET /api/health` |
| Traçabilité du modèle | Champ `model` dans la réponse JSON + `ML_MODEL_NAME` ; colonne `model_used` en base |

## Deep Learning — partiel / à confirmer selon PDF

| Point | Statut |
|-------|--------|
| **PyTorch** si imposé à la place de TensorFlow | Le projet est en **Keras/TF** ; à adapter si le PDF l’exige. |
| **Jeu de test** strictement indépendant (non vu par l’entraînement) | Évaluation sur le split validation/test du dataset HF uniquement. |
| **MLflow / W&B** | Non intégré ; les métriques sont dans des fichiers locaux. |
| **Grad-CAM / XAI** | Non implémenté. |
| **Comparaison de plusieurs architectures** | Un seul pipeline (MobileNetV2). |
| **Rapport PDF + diapos** | Livrables hors dépôt (à produire par l’équipe). |

## WAMS / microservices — satisfait

| Exigence typique | Implémentation |
|------------------|----------------|
| Plusieurs services conteneurisés | `docker-compose.yml` : auth, api, ml, worker, web, postgres, rabbitmq, consul, traefik |
| API REST métier | FastAPI CRUD patients + analyses |
| Authentification JWT | Service `auth` (rôles user/admin) |
| Base de données | PostgreSQL (métier), SQLite (auth) |
| Messagerie asynchrone | RabbitMQ, file `skin_predictions` |
| Passerelle / routage | Traefik (préfixes `/auth`, `/api/v1`, `/ml`, `/`) |
| Registre / découverte | Enregistrement Consul au démarrage |
| UI | `frond-end/` (statique) |
| Intégration ML dans le flux métier | Upload analyse → message → worker → appel `ml` → mise à jour `analyses` |

## WAMS — partiel / à confirmer selon PDF

| Point | Statut |
|-------|--------|
| **Kubernetes** | Non fourni (Compose seulement). |
| **Tests E2E** automatisés (stack complète) | Tests unitaires légers (`tests/`) ; pas de chaîne Docker automatisée. |
| **Worker via API métier** (secret partagé) | Le worker met à jour la BDD directement (SQL) ; cohérent avec une archi asynchrone simple. |

## Correctifs récents alignés sur ces attentes

- Résolution du chemin du modèle `.h5` (variables d’environnement + plusieurs emplacements) et montage Docker cohérent vers `training_artifacts/skin_model_best.h5`.
- Colonne `model_used` + migration légère au démarrage de l’API.
- Worker compatible **SQLAlchemy 2.x** (`text()`).
- Hyperparamètres externalisés dans `config.yaml` ; notebook de structuration pédagogique.

Pour extraire le texte brut de vos PDF dans le dépôt :  
`python scripts/extract_pdf_text.py` (après `pip install pypdf`).
