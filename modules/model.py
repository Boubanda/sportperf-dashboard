"""
modules/model.py
Logique XGBoost + SHAP — séparée de l'interface Streamlit.
La page pages/4_Prédictions.py importe ce module.
"""

import numpy as np
import pandas as pd
import shap
from xgboost import XGBRegressor
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error
import warnings
warnings.filterwarnings("ignore")

FEATURES = [
    "budget_ans_k_euros",
    "nb_medailles_tokyo",
    "nb_licencies",
    "nb_clubs",
    "discipline_olympique",
    "ratio_licencies_budget",
    "historique_moyen",
    "progression",
    "budget_par_club",
]

FEATURES_FR = {
    "budget_ans_k_euros":       "Budget ANS (k€)",
    "nb_medailles_tokyo":       "Médailles Tokyo",
    "nb_licencies":             "Nb licenciés",
    "nb_clubs":                 "Nb clubs",
    "discipline_olympique":     "Discipline olympique",
    "ratio_licencies_budget":   "Ratio licenciés / budget",
    "historique_moyen":         "Historique moyen médailles",
    "progression":              "Progression Tokyo → Paris",
    "budget_par_club":          "Budget par club",
}


def build_features(financements: pd.DataFrame, federations: pd.DataFrame) -> pd.DataFrame:
    """Construit le DataFrame de features à partir des tables SQL."""
    df = financements.merge(
        federations[["federation", "nb_licencies", "nb_clubs", "discipline_olympique"]],
        on="federation", how="left",
    )
    df["nb_licencies"]          = df["nb_licencies"].fillna(df["nb_licencies"].median())
    df["nb_clubs"]              = df["nb_clubs"].fillna(df["nb_clubs"].median())
    df["discipline_olympique"]  = df["discipline_olympique"].fillna(True).astype(int)
    df["ratio_licencies_budget"]= df["nb_licencies"] / (df["budget_ans_k_euros"] + 1)
    df["historique_moyen"]      = (df["nb_medailles_tokyo"] + df["nb_medailles_paris2024"]) / 2
    df["progression"]           = df["nb_medailles_paris2024"] - df["nb_medailles_tokyo"]
    df["budget_par_club"]       = df["budget_ans_k_euros"] / (df["nb_clubs"] + 1)
    return df


def train(df: pd.DataFrame):
    """Entraîne le modèle et calcule les valeurs SHAP."""
    X = df[FEATURES].fillna(0)
    y = df["nb_medailles_paris2024"]

    model = XGBRegressor(
        n_estimators=200, max_depth=3, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        reg_alpha=0.1, reg_lambda=1.0,
        random_state=42, verbosity=0,
    )

    loo      = LeaveOneOut()
    cv_mae   = -cross_val_score(model, X, y, cv=loo, scoring="neg_mean_absolute_error").mean()
    model.fit(X, y)

    y_pred   = model.predict(X)
    r2       = r2_score(y, y_pred)
    mae      = mean_absolute_error(y, y_pred)

    explainer   = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    metrics = {
        "r2":       round(r2, 3),
        "mae":      round(mae, 3),
        "mae_cv":   round(cv_mae, 3),
    }
    return model, explainer, shap_values, X, y, metrics


def predict_2030(model, df: pd.DataFrame, budget_boost: float = 1.15) -> pd.DataFrame:
    """Prédit les médailles JO 2030 avec simulation budgétaire."""
    d = df.copy()
    d["budget_ans_k_euros"]     = (d["budget_ans_k_euros"] * budget_boost).round(0)
    d["nb_medailles_tokyo"]     = d["nb_medailles_paris2024"]
    d["progression"]            = d["progression"].clip(lower=0)
    d["historique_moyen"]       = (d["nb_medailles_tokyo"] + d["nb_medailles_paris2024"]) / 2
    d["ratio_licencies_budget"] = d["nb_licencies"] / (d["budget_ans_k_euros"] + 1)
    d["budget_par_club"]        = d["budget_ans_k_euros"] / (d["nb_clubs"] + 1)

    X_2030  = d[FEATURES].fillna(0)
    preds   = np.round(model.predict(X_2030)).clip(0).astype(int)
    d["pred_medailles_2030"] = preds
    return d
