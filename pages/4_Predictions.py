"""
pages/4_Predictions.py
Page 4 — Modèle prédictif XGBoost + SHAP · JO 2030
"""

import sys
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.database import load_financements, load_federations
from modules.model    import build_features, train, predict_2030, FEATURES, FEATURES_FR

st.set_page_config(page_title="Prédictions · SportPerf", page_icon="🔮", layout="wide")

VERT = "#1D9E75"
BLEU = "#003D7C"
OR   = "#C8963E"
ROUGE= "#E24B4A"

# ── Sidebar ─────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Paramètres")
    budget_pct   = st.slider("Hausse budget ANS (%)", 0, 50, 15, 5)
    budget_boost = 1 + budget_pct / 100

st.title("🔮 Modèle Prédictif — JO 2030")
st.markdown("**XGBoost + SHAP · Simulation budgétaire · Ambition Bleue ANS**")
st.markdown("---")

# ── Chargement & entraînement ───────────────────
financements = load_financements()
federations  = load_federations()

with st.spinner("Entraînement du modèle XGBoost..."):
    df = build_features(financements, federations)
    model, explainer, shap_values, X, y, metrics = train(df)
    df_2030 = predict_2030(model, df, budget_boost)

# ── KPIs modèle ─────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("R² (entraînement)",  metrics["r2"])
c2.metric("MAE cross-val LOO",  f"{metrics['mae_cv']:.2f} médailles")
c3.metric("Prédiction 2030",
    int(df_2030["pred_medailles_2030"].sum()),
    f"+{int(df_2030['pred_medailles_2030'].sum()) - int(y.sum())} vs Paris 2024")
c4.metric("Simulation budget",  f"+{budget_pct}%")

st.markdown("---")

col_l, col_r = st.columns(2)

# ── Graphique prédictions ────────────────────────
with col_l:
    st.subheader("Paris 2024 vs Prédiction 2030")
    df_plot = df_2030[["federation","nb_medailles_paris2024","pred_medailles_2030"]].sort_values(
        "pred_medailles_2030", ascending=True
    )
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=df_plot["nb_medailles_paris2024"], y=df_plot["federation"],
        name="Paris 2024", marker_color=BLEU, orientation="h",
    ))
    fig1.add_trace(go.Bar(
        x=df_plot["pred_medailles_2030"], y=df_plot["federation"],
        name="Prédiction 2030", marker_color=VERT, orientation="h",
    ))
    fig1.update_layout(
        barmode="group", height=520,
        legend=dict(orientation="h", y=-0.15),
        xaxis_title="Nombre de médailles",
    )
    st.plotly_chart(fig1, use_container_width=True)

# ── Importance SHAP ──────────────────────────────
with col_r:
    st.subheader("Importance des variables (SHAP)")
    shap_df = (
        __import__("pandas").DataFrame({
            "feature":    [FEATURES_FR.get(f, f) for f in FEATURES],
            "importance": np.abs(shap_values).mean(axis=0),
        })
        .sort_values("importance", ascending=True)
    )
    fig2 = px.bar(
        shap_df, x="importance", y="feature", orientation="h",
        color="importance",
        color_continuous_scale=[[0,"#E1F5EE"],[1,"#0F6E56"]],
        labels={"importance":"Impact SHAP moyen","feature":""},
    )
    fig2.update_layout(height=300, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Réel vs Prédit — Paris 2024")
    y_pred = model.predict(X)
    fig3   = go.Figure()
    fig3.add_trace(go.Scatter(
        x=y, y=y_pred, mode="markers+text",
        text=df["federation"], textposition="top center",
        marker=dict(color=BLEU, size=8),
    ))
    fig3.add_trace(go.Scatter(
        x=[0, int(y.max())], y=[0, int(y.max())],
        mode="lines", line=dict(dash="dash", color="gray"),
        name="Prédiction parfaite",
    ))
    fig3.update_layout(
        height=280, showlegend=False,
        xaxis_title="Réel", yaxis_title="Prédit",
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── SHAP waterfall discipline ────────────────────
st.markdown("---")
st.subheader("Explication SHAP — Détail par discipline")
disc_sel = st.selectbox("Discipline", df["federation"].tolist())
idx      = df[df["federation"] == disc_sel].index[0]

import pandas as pd
shap_disc = pd.DataFrame({
    "feature": [FEATURES_FR.get(f, f) for f in FEATURES],
    "valeur":  X.iloc[idx].values,
    "shap":    shap_values[idx],
}).sort_values("shap", key=abs, ascending=True)

colors = [ROUGE if v < 0 else VERT for v in shap_disc["shap"]]
pred   = df_2030[df_2030["federation"] == disc_sel]["pred_medailles_2030"].values[0]

fig4 = go.Figure(go.Bar(
    x=shap_disc["shap"], y=shap_disc["feature"],
    orientation="h", marker_color=colors,
    text=[f"{v:+.2f}" for v in shap_disc["shap"]],
    textposition="outside",
))
fig4.update_layout(
    title=f"{disc_sel} — Prédiction 2030 : {pred} médaille(s)",
    height=360,
    xaxis_title="Impact SHAP (vert = augmente, rouge = diminue)",
)
st.plotly_chart(fig4, use_container_width=True)

# ── Tableau récap ─────────────────────────────────
st.subheader("Tableau récapitulatif")
recap = df_2030[[
    "federation","budget_ans_k_euros","nb_medailles_paris2024",
    "pred_medailles_2030","roi_medaille_par_mEuros",
]].copy()
recap["delta"] = recap["pred_medailles_2030"] - recap["nb_medailles_paris2024"]
recap.columns  = ["Discipline","Budget (k€)","Paris 2024","Prédiction 2030","ROI (méd/M€)","Δ"]
st.dataframe(
    recap.sort_values("Prédiction 2030", ascending=False).reset_index(drop=True),
    use_container_width=True, height=400,
)
