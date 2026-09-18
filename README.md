# Economic Intelligence Platform

Plateforme de veille économique, financière et réglementaire développée avec Python et Streamlit.

## Objectifs

Collecter automatiquement les informations provenant de :

### Institutions marocaines

- Bank Al-Maghrib (BAM)
- Ministère de l'Économie et des Finances (MEF)
- HCP
- Bourse de Casablanca
- AMMC
- MAP

### Institutions internationales

- FMI
- Banque Mondiale
- OCDE
- BAD
- BCE
- FED

## Fonctionnalités

- Collecte RSS
- Collecte API
- Scraping de sites publics
- Centralisation des actualités
- Classification automatique
- Alertes intelligentes
- Tableau de bord Streamlit
- Historisation en base de données
- Génération de synthèses IA
- Recherche documentaire RAG

---

# Architecture

```text
economic-intelligence-platform/
├── app.py
├── config/
├── connectors/
├── services/
├── repository/
├── database/
├── pages/
├── tests/
└── data/
```

---

# Installation

## Cloner le dépôt

```bash
git clone https://github.com/organisation/economic-intelligence-platform.git

cd economic-intelligence-platform
```

## Créer un environnement virtuel

Linux

```bash
python -m venv venv
## Licence

Ce projet est distribué sous licence MIT.

Copyright © 2026 Fouad Boukhnif

La licence MIT autorise librement :

- l'utilisation privée et commerciale ;
- la modification ;
- la distribution ;
- la sous-licence ;
- l'intégration dans des projets propriétaires.

Le logiciel est fourni "en l'état", sans garantie d'aucune sorte.

Voir le fichier LICENSE pour le texte intégral.
