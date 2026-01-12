# Backend (FastAPI) — AstroBot

## Prérequis
- Python 3.10+
- Un service Ollama actif en local

## IA locale
Ce backend utilise un modèle de langage exécuté localement via Ollama.

- Runtime : Ollama
- Modèle utilisé : `qwen3:4b`
- L’API Ollama doit être accessible sur : `http://localhost:11434`

⚠️ Le backend ne lance pas Ollama lui-même.  
Le service Ollama doit être actif avant le démarrage du serveur.

## Installation
Se placer dans le dossier backend :
```bash
cd backend
````
Créer et activer l'environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate
```
Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement du serveur
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Tester que le serveur est bien lancé
### Option A — Swagger
Ouvrir : 
- [http://localhost:8000/docs](http://localhost:8000/docs)

Tester `POST /chat` avec :
```json
{
  "message": "Salut",
  "conversation_id": "test1"
}
```
Réponse attendue :
```json
{
  "reply": "Tu as dit: Salut",
  "conversation_id": "test1"
}
```

### Option B — curl
Exécuter la commande :
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Salut","conversation_id":"test1"}'
```
Réponse attendue :
```bash
{"reply":"Tu as dit: Salut","conversation_id":"test1"}
```