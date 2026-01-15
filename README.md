# AstroBot — Agent IA d’astronomie (Hephaestus / MCP)

AstroBot est une application web qui intègre un agent conversationnel d’astronomie capable de :
- comprendre une question en langage naturel,
- décider d’utiliser (ou non) un tool externe via un serveur MCP,
- récupérer des données réelles (scraping RSS),
- puis formuler une réponse en s’appuyant sur ces données.

## Architecture (vue d’ensemble)

- **Frontend (React)** : interface vitrine + chat
- **Backend (FastAPI)** : orchestrateur (logique agentique, mémoire de conversation, appels au modèle et au MCP)
- **LLM local (Ollama + qwen3:4b)** : génération de la réponse
- **MCP Server (FastAPI)** : expose des tools (scraping RSS, archive, image search, positions célestes)

Flux simplifié :
`User → Frontend → Backend → (LLM décide / Backend orchestre) → MCP tool → Backend → LLM → Frontend → User`

## Stack technique

### Frontend
- React (Create React App)
- Fetch API (appels HTTP vers le backend)

### Backend (orchestrateur)
- Python + FastAPI
- Uvicorn (serveur ASGI)
- Requests (appels HTTP vers Ollama et MCP)
- Pydantic (validation des requêtes)

### MCP Server (tools)
- Python + FastAPI
- Uvicorn (serveur ASGI)
- Tools :
  - Scraping RSS : `urllib` + `xml.etree.ElementTree` + nettoyage HTML (`re`, `html`)
  - Archives (optionnel) : `requests` vers Spaceflight News API (v4)

### LLM local
- Ollama (runtime local)
- Modèle : qwen3:4b (choisi comme compromis entre qualité, ressources, latence)


## Arborescence

- backend/ (orchestrateur)
- frontend/ (UI)
- mcp/ (tools MCP)


## Prérequis

- **Python 3.10+** (backend + MCP)
- **Node.js 18+** (frontend)
- **Ollama** installé et fonctionnel
- Modèle Ollama : **qwen3:4b**

> Remarque modèle : qwen3:4b a été choisi comme compromis qualité / ressources (CPU/RAM) sur machine locale
> En cas de contrainte de latence pour la démo, un modèle plus léger peut être utilisé

## Ports

- Frontend : `http://localhost:3000`
- Backend : `http://localhost:8000`
- MCP : `http://localhost:9000`
- Ollama : `http://localhost:11434`

---

# Lancement du projet (4 services)

## 1) Lancer Ollama + modèle

Vérifier qu’Ollama répond :
```bash
curl http://127.0.0.1:11434/api/tags
```
Si le modèle n’est pas présent :
```bash
ollama pull qwen3:4b
```

## 2) Lancer le MCP

```bash
cd mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 9000
````
Vérifier :
- Swagger : `http://127.0.0.1:9000/docs`

## 3) Lancer le backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Vérifier :
- Swagger : `http://localhost:8000/docs`

## 4) Lancer le frontend

```bash
cd frontend
npm install
npm start
````
Ouvrir :
- `http://localhost:3000`

# API Backend

## POST /chat

Exemple de requête :
```json
{
  "message": "Explique-moi Jupiter en 2 phrases",
  "conversation_id": "demo"
}
```
Réponse :
```json
{
  "reply": "...",
  "conversation_id": "demo"
}
```

# Tools MCP (principaux)

## 1) Scraping RSS (données récentes)

- Route : POST `/tools/scrape_astronomy_news``
- Input :
```json
{ "keyword": "mars", "limit": 10 }
```
- Output : liste d’articles RSS (title/date/source/link/summary)

## 2) Archives (année)

- Route : POST `/tools/search_astronomy_archive``
- Input :
```json
{ "year": 2022, "keyword": "mars", "limit": 10 }
```
- Output : articles formatés (title/summary/url/published_at/source)

> **Note : ce tool sert à répondre à des requêtes temporelles (ex: année 2022), il est présenté comme un complément au scraping existant**

## 3) Autres tools (à voir si utilisés)

- POST `/tools/astronomy_image_search`
- POST `/tools/celestial_position`

# Fonctionnement de l’agent

1. Le frontend envoie `{message, conversation_id}` au backend
2. Le backend :
   - stocke l’historique en RAM (mémoire de conversation)
   - détecte si la question nécessite des données récentes ou par rapport à une année précise
   - appelle le MCP si nécessaire
   - injecte les données tool dans le contexte du LLM
3. Ollama génère une réponse finale en français
4. Le backend renvoie `{reply}` au frontend

5. Au niveau de la Sécurité :
   - les données tool sont traitées comme externes
   - consigne explicite au LLM d’ignorer toute instruction potentielle contenue dans ces données

# Limites connues

- Latence : selon la machine et le modèle, une réponse peut prendre entre 1 à 2 minutes, voir plus
- Le scraping RSS dépend de la disponibilité des sources et de leur pertinence
- Le tool d’archives dépend d’une source externe et on peut manquer d'information sur un sujet précis selon le contexte temporel

# Auteurs

Ce projet a été réalisé dans le cadre du module Hephaestus du cursus MSc MSI par :
- Jade
- Rita
- Théo
- Christian
- Kemil
