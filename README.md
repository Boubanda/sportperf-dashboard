# 🏅 SportPerf Dashboard
**Analyse de la performance sportive française — Agence Nationale du Sport**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://boubanda-sportperf-dashboard.streamlit.app)
[![Python](https://img.shields.io/badge/Py

**Tables SQL créées :**

| Table | Description | Lignes |
|---|---|---|
| `federations` | 25 fédérations sportives avec licenciés et clubs | 25 |
| `medailles_jo2024` | 29 médailles France — JO Paris 2024 | 29 |
| `historique_jo` | Historique des JO France 1996-2024 | 8 |
| `financements_ans` | Budgets ANS et ROI par discipline | 20 |

---

### Module 2 — Dashboard Streamlit interactif (`pages/`)

Dashboard multi-pages déployé sur Streamlit Cloud avec navigation automatique.

**Page 1 — Médailles Paris 2024** 🥇
- Filtres interactifs par discipline, type de médaille et genre
- KPIs : total médailles, or/argent/bronze, disciplines médaillées
- Graphique médailles par discipline (barres empilées)
- Répartition par genre (H/F/Mixte)
- Tableau détaillé des 29 médailles

**Page 2 — Historique olympique** 📈
- Évolution des médailles France sur 8 éditions (1996-2024)
- Barres empilées or/argent/bronze par JO
- Courbe du classement mondial de la France
- Évolution du nombre d'athlètes engagés

**Page 3 — Financements ANS & ROI** 💰
- Classement des disciplines par ROI budgétaire (médailles / M€ investi)
- Scatter plot Budget vs Médailles avec taille proportionnelle au ROI
- Comparaison Tokyo 2020 → Paris 2024 par discipline
- Tableau complet des financements

**Page 4 — Prédictions JO 2030** 🔮
- Slider interactif pour simuler des hausses de budget ANS (0% à +50%)
- Comparaison Paris 2024 vs Prédictions 2030 par discipline
- Importance des variables (graphique SHAP)
- Graphique Réel vs Prédit (validation du modèle)
- Explication SHAP détaillée par discipline sélectionnée
- Tableau récapitulatif avec indicateur delta

---

### Module 3 — Modèle prédictif XGBoost + SHAP (`modules/model.py`)

Modèle de machine learning prédisant le potentiel de médailles françaises par discipline aux JO 2030.

**Features utilisées :**

| Feature | Description |
|---|---|
| `budget_ans_k_euros` | Budget alloué par l'ANS (k€) |
| `nb_medailles_tokyo` | Médailles obtenues à Tokyo 2020 |
| `nb_licencies` | Nombre de licenciés dans la fédération |
| `nb_clubs` | Nombre de clubs de la fédération |
| `discipline_olympique` | Discipline aux JO (booléen) |
| `ratio_licencies_budget` | Ratio licenciés / budget (feature construite) |
| `historique_moyen` | Moyenne médailles Tokyo + Paris 2024 |
| `progression` | Delta médailles Tokyo → Paris 2024 |
| `budget_par_club` | Budget ANS par club (feature construite) |

**Résultats du modèle :**

| Métrique | Valeur |
|---|---|
| R² (entraînement) | 1.000 |
| MAE (Leave-One-Out cross-validation) | **0.51 médaille** |
| Prédiction JO 2030 (+15% budget ANS) | **38 médailles** (+6 vs Paris 2024) |
| Feature la plus influente (SHAP) | `historique_moyen` |

**Méthodologie :**
- Validation croisée Leave-One-Out (LOO) pour robustesse sur petit dataset
- Explicabilité SHAP (TreeExplainer) pour chaque discipline
- Simulation budgétaire paramétrable (+0% à +50%)

---

## 📊 Résultats clés

### JO Paris 2024 — France
- **64 médailles** au total (record depuis Atlanta 1996)
- **16 médailles d'or** — meilleur résultat depuis Atlanta
- **11 disciplines** médaillées
- **Rang mondial : #5**

### Top 5 disciplines par ROI budgétaire ANS
| Discipline | Budget (k€) | Médailles 2024 | ROI (méd/M€) |
|---|---|---|---|
| Judo | 3 800 | 8 | 2.11 |
| Escrime | 2 100 | 4 | 1.90 |
| Cyclisme | 2 900 | 4 | 1.38 |
| Natation | 4 200 | 5 | 1.19 |
| Tir | 900 | 1 | 1.11 |

### Prédiction JO 2030 (simulation +15% budget)
- **38 médailles prédites** (+6 vs Paris 2024)
- **Judo et Natation** : disciplines les plus prometteuses (8 médailles chacune)
- **Athlétisme** : potentiel de progression confirmé par SHAP

---

## 🚀 Installation locale

### Prérequis
- Python 3.11+
- Git

### Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/Boubanda/sportperf-dashboard.git
cd sportperf-dashboard

# 2. Créer l'environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Générer la base de données
python modules/collect_data.py

# 5. Lancer le dashboard
streamlit run app.py
```

Le dashboard s'ouvre automatiquement sur **http://localhost:8501**

---

## 🌐 Déploiement

L'application est déployée sur **Streamlit Community Cloud** :

🔗 **[https://boubanda-sportperf-dashboard.streamlit.app](https://boubanda-sportperf-dashboard.streamlit.app)**

La base SQLite est générée automatiquement au premier lancement via `init_db.py`.

---

## 🛠️ Stack technique

| Catégorie | Technologies |
|---|---|
| **Langage** | Python 3.11 |
| **Dashboard** | Streamlit |
| **Visualisation** | Plotly |
| **Data manipulation** | Pandas, NumPy |
| **Machine Learning** | XGBoost, scikit-learn |
| **Explicabilité IA** | SHAP |
| **Base de données** | SQLite, SQLAlchemy |
| **Collecte données** | Requests (API data.gouv.fr) |
| **Versioning** | Git, GitHub |
| **Déploiement** | Streamlit Community Cloud |

---

## 📁 Sources de données

| Source | Description | URL |
|---|---|---|
| data.gouv.fr / INJEP | Licenciés par fédération sportive | [data.gouv.fr](https://data.gouv.fr) |
| paris2024.org | Résultats officiels JO Paris 2024 | [paris2024.org](https://paris2024.org) |
| Agence Nationale du Sport | Rapports annuels & budgets | [agencedusport.fr](https://agencedusport.fr) |
| Historique olympique | Résultats France 1996-2024 | Open data |

---

## 🔮 Évolutions prévues

- [ ] **Module 4** — Assistant RAG : chatbot permettant d'interroger les données en langage naturel ("Quelle discipline a le meilleur ROI par euro investi ?")
- [ ] Intégration des données réelles via API data.gouv.fr en temps réel
- [ ] Ajout des données athlètes individuels (âge, résultats récents)
- [ ] Modèle de clustering des fédérations par profil de performance
- [ ] Export PDF des rapports d'analyse

---

## 👤 À propos de l'auteur

**Levi Junior BOUBANDA** — Étudiant en 4e année du MSc IA & Data Science à **Aivancity Paris** (Bac+5, n°1 Eduniversal), en recherche d'alternance Data Scientist / Data Engineer à partir de septembre 2026.

**Expériences principales :**
- 🔬 **SEED / Aivancity** — Data Engineer : pipeline NLP XGBoost (87% précision, -60% temps de traitement)
- 🌿 **Fairmat / Aivancity** — Data Scientist : pipeline ETL 12 000+ données, dashboards Power BI
- ❤️ **Uiz.care / Aivancity** — Data Engineer : ingestion 15 000+ points IoT santé

**Portfolio** : [mon-portfolio-nine-lime.vercel.app](https://mon-portfolio-nine-lime.vercel.app)

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

*Projet développé dans le cadre d'une candidature à l'Agence Nationale du Sport — Pôle Data Analyse, Pôle Haute Performance. Données issues de sources publiques officielles.*
thon-3.11-blue.svg)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-orange.svg)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Présentation

**SportPerf Dashboard** est un projet data end-to-end développé dans le cadre d'une candidature à l'**Agence Nationale du Sport (ANS)** — Pôle Data & Analyse, Pôle Haute Performance.

Il analyse la performance sportive française à travers les Jeux Olympiques, les financements ANS et les licenciés par fédération, et prédit le potentiel de médailles pour les **Jeux Olympiques 2030** grâce à un modèle XGBoost avec explicabilité SHAP.

> **Auteur** : Levi Junior BOUBANDA  
> **Formation** : MSc IA & Data Science — Aivancity Paris (Bac+5, n°1 Eduniversal)  
> **Contact** : leviboubanda07@gmail.com  
> **LinkedIn** : [linkedin.com/in/lévi-junior016](https://linkedin.com/in/lévi-junior016)  
> **GitHub** : [github.com/Boubanda](https://github.com/Boubanda)

---

## 🎯 Objectifs du projet

Ce projet répond directement aux missions du **Pôle DATA ANALYSE de l'ANS** :

| Mission ANS | Réalisation dans le projet |
|---|---|
| Modélisation de l'entrepôt des données sport | Pipeline Python + base SQLite structurée |
| Tableaux de bord de pilotage | Dashboard Streamlit 4 pages interactif |
| Analyse de la haute performance | Suivi médailles JO Paris 2024 par discipline |
| Financements et ROI | Analyse ROI budgétaire ANS par fédération |
| Développement de cas d'usage IA | Modèle prédictif XGBoost + explicabilité SHAP |
| Objectifs JO 2030 — Ambition Bleue | Simulation budgétaire et prédiction médailles |

---

## 🏗️ Architecture du projet

```
sportperf_v2/
│
├── app.py                        # Point d'entrée unique — streamlit run app.py
├── init_db.py                    # Initialisation automatique de la base
├── requirements.txt              # Dépendances Python
├── runtime.txt                   # Version Python forcée (3.11)
├── .python-version               # Python 3.11
├── .gitignore
├── README.md
│
├── modules/                      # Logique métier Python pure
│   ├── collect_data.py           # Module 1 — Pipeline collecte & SQL
│   ├── database.py               # Chargement centralisé des données
│   └── model.py                  # Module 3 — XGBoost + SHAP
│
├── pages/                        # Pages Streamlit (navigation auto)
│   ├── 1_Medailles.py            # Page 1 — Médailles JO Paris 2024
│   ├── 2_Historique.py           # Page 2 — Historique 1996-2024
│   ├── 3_Financements.py         # Page 3 — Financements ANS & ROI
│   └── 4_Predictions.py          # Page 4 — Prédictions XGBoost JO 2030
│
├── data/
│   └── raw/                      # Données brutes CSV
│       ├── licencies_raw.csv
│       ├── jo_2024_medailles.csv
│       ├── historique_jo.csv
│       └── financements_ans.csv
│
├── db/
│   └── sportperf.db              # Base SQLite (générée automatiquement)
│
└── .streamlit/
    └── config.toml               # Configuration Streamlit Cloud
```

---

## 📦 Modules développés

### Module 1 — Collecte & Structuration des données (`modules/collect_data.py`)

Pipeline Python de collecte et structuration des données sport françaises.

**Sources de données :**
- 🏛️ **data.gouv.fr / INJEP** — Licenciés par fédération sportive (2022)
- 🏅 **paris2024.org** — Résultats et médailles JO Paris 2024
- 💰 **Rapports ANS** — Budgets alloués aux fédérations olympiques
- 📊 **Open data olympique** — Historique des JO France (1996-2024)

**Ce que le module fait :**
- Collecte automatique via API data.gouv.fr (fallback sur données de démonstration)
- Nettoyage et structuration des données
- Construction d'une base SQLite avec 4 tables et 1 vue consolidée
- Rapport de validation automatique avec statistiques clés