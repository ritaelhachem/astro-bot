# AstroBot — Agent conversationnel IA (Projet Hephaestus)

AstroBot est un **agent conversationnel intelligent** intégré à une application web, capable de comprendre des requêtes en langage naturel et de décider d’exécuter ou non des actions via des outils externes (tooling), selon une architecture agentique modulaire.

Le projet repose sur un **modèle de langage local**, un **backend Python orchestrateur**, un **serveur MCP simulant des outils**, et un **frontend web** permettant l’interaction utilisateur.

---

## Objectifs du projet

* Concevoir un **agent IA conversationnel** fonctionnel
* Mettre en œuvre une **architecture modulaire** (Frontend / Backend / MCP / IA)
* Séparer le **raisonnement** (LLM) de l’**exécution** (tools)
* Utiliser exclusivement des **technologies open-source locales**
* Démontrer un prototype fonctionnel avec du **vrai scraping** (pas de mock)

---

## Architecture globale

```
Utilisateur
   ↓
Frontend (Web UI)
   ↓ HTTP
Backend FastAPI (Orchestrateur) ──→ Ollama (LLM local)
   ↓ HTTP
Serveur MCP (Tools)
   ↓
Scraping de données publiques
```

### Rôles des composants

* **Frontend** : interface utilisateur, envoi des messages, affichage des réponses
* **Backend** : logique agentique, gestion du contexte, décision d’appel aux tools
* **MCP Server** : expose des outils (scraping) sous forme d’API
* **Ollama** : exécute localement le modèle de langage
* **Modèle LLM** : raisonnement et génération des réponses

---

## IA locale

* **Runtime** : Ollama (service local)
* **Modèle utilisé** : `qwen3:4b`
* **Type** : LLM open-source exécuté localement
* **Utilisation** : raisonnement, génération de réponses, décision d’appel aux tools

Le modèle n’est **pas exécuté en continu**.
Il est **chargé à la demande** lors des requêtes envoyées par le backend.

---

## MCP & Tooling

Le projet simule un **Model Context Protocol (MCP)** permettant de séparer :

* le **raisonnement** (LLM)
* l’**exécution d’actions réelles** (tools)

### Tools implémentés

* **Scraping de données publiques**

  * Sites accessibles sans authentification
  * Faible fréquence de requêtes
  * Données utilisées uniquement à des fins pédagogiques

Les tools sont exposés via un **serveur MCP** et appelés par le backend lorsque l’agent en décide la nécessité.

---

## Frontend

* Application web permettant :

  * l’interaction avec le chatbot
  * l’envoi de messages en langage naturel
  * l’affichage des réponses de l’agent
* Communication avec le backend via **API REST**

Voir `frontend/README.md` pour les détails d’installation et de lancement.

---

## Backend

* Développé en **Python (FastAPI)**
* Rôle :

  * orchestrateur de l’agent
  * gestion du contexte conversationnel
  * communication avec Ollama
  * appel au serveur MCP et aux tools

Voir `backend/README.md` pour les détails techniques.

---

## Lancement du projet (ordre recommandé)

### Prérequis système

* Python 3.10+
* Node.js
* Ollama installé et actif en local

Télécharger le modèle IA (une seule fois) :

```bash
ollama pull qwen3:4b
```

---

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Frontend

```bash
cd frontend
npm install
npm start
```

---

## Vérification rapide

* Backend : [http://localhost:8000/docs](http://localhost:8000/docs)
* Frontend : [http://localhost:3000](http://localhost:3000) (ou port affiché)
* Interaction complète : Frontend → Backend → Ollama → Réponse

---

## Limites actuelles

* Un seul domaine fonctionnel (astronomie)
* Tooling limité au scraping
* Pas de streaming des réponses
* Pas de persistance longue durée du contexte

---

## Améliorations possibles

* Ajout de nouveaux tools (API externes, calculs, fichiers)
* Streaming des réponses LLM
* Mémoire conversationnelle persistante
* Gestion multi-domaines
* Authentification utilisateur

---

## Contexte pédagogique

Projet réalisé dans le cadre du **projet Hephaestus**, visant à comprendre :

* les architectures agentiques
* l’intégration de LLMs locaux
* la séparation raisonnement / exécution
* les flux de données IA modernes

---

## Équipe

Projet réalisé en groupe de 5 personnes.
Tous les membres participent à la conception, au développement et à la soutenance.
