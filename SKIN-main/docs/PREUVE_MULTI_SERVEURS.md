# Preuve de deploiement multi-serveurs (WAMS)

Utiliser ce fichier comme trace de validation finale.

## 1) Topologie

- Serveur 1: `traefik` + `consul`
- Serveur 2: `auth` + `web`
- Serveur 3: `api` + `worker`
- Serveur 4: `ml`
- Serveur 5: `postgres` + `rabbitmq`

## 2) Preuves a joindre

- Captures ecran de chaque machine (IP + services actifs).
- Sortie `docker ps` (ou service manager) par serveur.
- Capture Traefik dashboard montrant les routes actives.
- Capture Consul montrant les services enregistres.
- Capture RabbitMQ montrant la queue `skin_predictions`.
- Test fonctionnel (login -> create patient -> upload image -> resultat `done`).

## 3) Commandes minimales de verification

Sur machine cliente:

```bash
curl -i http://<gateway>/auth/health
curl -i http://<gateway>/api/v1/health
curl -i http://<gateway>/ml/api/health
```

Test asynchrone:

1. Authentification et recuperation du token.
2. Creation patient via API.
3. Upload image via `/api/v1/analyses`.
4. Verification que `status` passe de `pending` a `done`.

## 4) Check-list finale

- [ ] Services deployes sur des serveurs distincts.
- [ ] Routage via Traefik valide.
- [ ] Discovery via Consul valide.
- [ ] Flux RabbitMQ valide.
- [ ] Rapport inclut les captures et resultats.
