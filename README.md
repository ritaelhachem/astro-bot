# AstroBot — Agent IA d’astronomie

AstroBot est une application web qui intègre un agent conversationnel d’astronomie capable de :
- comprendre une question en langage naturel,
- décider d’utiliser (ou non) un outil externe via un serveur MCP,
- récupérer des données réelles (scraping RSS / sources publiques),
- calculer la visibilité d’objets célestes depuis une ville,
- puis formuler une réponse en s’appuyant sur ces données.

---

## Architecture générale

- **Frontend (React)** : interface vitrine + chat (texte + dictée vocale)
- **Backend (FastAPI)** : orchestrateur (logique agentique, mémoire de conversation, appels au modèle et au MCP)
- **LLM local (Ollama)** : génération de réponse (modèle configurable via `.env`)
- **MCP Server (FastAPI)** : expose les tools (scraping RSS, archive par année, position d’objets célestes)

Flux simplifié :
`User → Frontend → Backend → (LLM + orchestration) → MCP tool(s) → Backend → LLM → Frontend → User`

---

## Stack technique

### Frontend
- React (Create React App)
- Fetch API (appels HTTP vers le backend)
- Web Speech API (dictée vocale, si support navigateur)
- ReactMarkdown (affichage des réponses structurées)

### Backend (orchestrateur)
- Python + FastAPI
- Uvicorn (serveur ASGI)
- Requests (appels HTTP vers Ollama et MCP)
- Pydantic (validation des requêtes)
- Mémoire de conversation en RAM (par `conversation_id`)

### MCP Server (tools)
- Python + FastAPI
- Uvicorn (serveur ASGI)
- Tools :
  - Scraping RSS : `urllib` + `xml.etree.ElementTree` + nettoyage HTML (`re`, `html`)
  - Archives par année : `requests` vers Spaceflight News API (v4)
  - Position/visibilité : géocodage Nominatim (OpenStreetMap) + calcul alt/az via Skyfield

### LLM local
- Ollama (runtime local)
- Modèle : configurable via `backend/.env` (par défaut : `qwen3:4b`)

---

## Arborescence

```text
.
├── README.md
├── .gitignore
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── router.py
│       ├── orchestrator.py
│       ├── ollama_client.py
│       ├── mcp_client.py
│       └── memory.py
├── mcp/
│   ├── main.py
│   ├── requirements.txt
│   └── tools/
│       ├── position.py
│       ├── scrape_rss.py
│       └── astronomy_archive.py
└── frontend/
    ├── .gitignore
    ├── README.md
    ├── package-lock.json
    ├── package.json
    ├── public/
    └── src/
        ├── App.js
        ├── Components/
        └── assets/
```

### Prérequis
- Python 3.10+ (backend + MCP)
- Node.js 18+ (frontend)
- Ollama installé et fonctionnel

### Ports
- Frontend : `http://localhost:3000`
- Backend : `http://localhost:8000`
- MCP : `http://localhost:9000`
- Ollama : `http://localhost:11434`

### Configuration (.env)

Le backend utilise un fichier backend/.env pour configurer le modèle Ollama et l’URL d’accès, sans modifier le code.

Créer le fichier .env :
```bash
cp backend/.env.example backend/.env
```
Puis remplacer les valeurs par defaut de `OLLAMA_MODEL` et `OLLAMA_URL` par vos vraies valeurs.
> Remarque : le fichier `backend/.env` doit être ignoré par Git. Vous pouvez versionner un template `backend/.env.example`.

## Lancement du projet (4 services)

### 1) Lancer Ollama + modèle

Vérifier qu’Ollama répond avec :
```bash
curl http://127.0.0.1:11434/api/tags
````
Dans le cas où le modèle n'est pas présent (remplacer `qwen3:4b` par votre vrai modèle):
```bash
ollama pull qwen3:4b
```

### 2) Lancer le MCP

```bash
cd mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 9000
```
Vérifier qu'il tourne et fonctionne bien avec :
- Swagger MCP : [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs)

### 3) Lancer le backend

Assurez-vous d’avoir configuré `backend/.env` (voir section Configuration).
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
````
Vérifier qu'il tourne et fonctionne bien avec :
- Swagger backend : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4) Lancer le frontend

```bash
cd frontend
npm install
npm start
```
Ouvrir :
- [http://localhost:3000](http://localhost:3000)

---

## API Backend

### POST /chat

Requête :
```json
{
  "message": "Explique-moi Jupiter en 2 phrases",
  "conversation_id": "demo"
}
````

Réponse :
```json
{
  "reply": "...",
  "conversation_id": "demo"
}
```

## Tools MCP (principaux)

Le serveur MCP expose 3 outils. Le backend, via l'orchestrateur, choisit dynamiquement de les appeler selon l’intention détectée dans la requête.

### 1) Scraping RSS (données récentes)
- Route : POST `/tools/scrape_astronomy_news`
- Input :
```json
{ "keyword": "mars", "limit": 10 }
```
- Output : liste d’articles RSS (title/date/source/link/summary)

### 2) Archives (année) — source via API publique
- Route : POST `/tools/search_astronomy_archive`
- Input :
```json
{ "year": 2022, "keyword": "jwst", "limit": 10 }
```
- Output : articles (title/summary/url/published_at/source)
> Note : cet outil utilise une API publique (Spaceflight News API) et sert à répondre aux requêtes temporelles.

### 3) Position d’un objet céleste (visible ou non depuis une ville)
- Route : POST `/tools/position`
- Input :
```json
{ "object_name": "mars", "location": "Paris", "iso_time": null }
```
- Output : coordonnées de la ville ainsi que la visibilité de l’objet (altitude, azimut, direction) calculées via Skyfield.

---

## Fonctionnement de l’agent (orchestration)
1. Le frontend envoie {message, conversation_id} au backend
2. Le backend :
    - stocke l’historique en RAM (mémoire de conversation)
    - détecte si la question nécessite des données récentes, une recherche par année, ou un calcul de visibilité
    - appelle le MCP si nécessaire
    - injecte les données tool dans le contexte du LLM en tant que contexte externe
3. Ollama génère une réponse finale en français
4. Le backend renvoie {reply} au frontend

### Sécurité (niveau prototype)
- Les données tool sont traitées comme externes.
- Le LLM reçoit une consigne explicite d’ignorer toute instruction potentielle contenue dans ces données (mitigation prompt injection).

---

## Limites connues

- Latence : dépend de la machine et du modèle (Ollama)
- Le scraping RSS dépend de la disponibilité des sources et de leur pertinence
- Le tool d’archives dépend d’une source externe (API publique)
- La mémoire est volatile (RAM) : elle est perdue au redémarrage du backend
- La dictée vocale dépend du support navigateur (Web Speech API)

---

## Auteurs

Ce projet a été réalisé dans le cadre du module Hephaestus du cursus MSc MSI par :
- Jade
- Rita
- Théo
- Christian
- Kemil