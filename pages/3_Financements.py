"""
pages/3_Financements.py
Page 3 — Financements ANS & ROI budgétaire
"""

import sys
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.database import load_financements

st.set_page_config(page_title="Financements · SportPerf", page_icon="💰", layout="wide")

VERT = "#1D9E75"
BLEU = "#003D7C"
BRZ  = "#7B4A2D"

fin = load_financements()

st.title("💰 Financements ANS & Retour sur investissement")
st.markdown("---")

# ── KPIs ────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Budget total analysé",  f"{fin['budget_ans_k_euros'].sum()/1000:.1f} M€")
c2.metric("Disciplines suivies",   len(fin))
c3.metric("Total médailles 2024",  int(fin["nb_medailles_paris2024"].sum()))
c4.metric("ROI moyen",
    f"{fin[fin['nb_medailles_paris2024']>0]['roi_medaille_par_mEuros'].mean():.2f} méd/M€")

st.markdown("---")

# ── ROI par discipline ────────────────────────────
st.subheader("ROI budgétaire par discipline — médailles Paris 2024 par million € investi")
fig1 = px.bar(
    fin.sort_values("roi_medaille_par_mEuros", ascending=True),
    x="roi_medaille_par_mEuros", y="federation", orientation="h",
    color="roi_medaille_par_mEuros",
    color_continuous_scale=[[0,"#E1F5EE"],[1,"#0F6E56"]],
    labels={"roi_medaille_par_mEuros":"Médailles / M€","federation":""},
)
fig1.update_layout(height=520, coloraxis_showscale=False)
st.plotly_chart(fig1, use_container_width=True)

col_l, col_r = st.columns(2)

with col_l:
    st.subheader("Budget vs Médailles")
    fig2 = px.scatter(
        fin,
        x="budget_ans_k_euros", y="nb_medailles_paris2024",
        size=fin["nb_medailles_paris2024"].clip(lower=0.5),
        color="roi_medaille_par_mEuros",
        hover_name="federation",
        color_continuous_scale=[[0,"#E1F5EE"],[1,"#0F6E56"]],
        labels={"budget_ans_k_euros":"Budget (k€)", "nb_medailles_paris2024":"Médailles"},
    )
    fig2.update_layout(height=380, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

with col_r:
    st.subheader("Évolution Tokyo → Paris 2024")
    fin_evo = fin.copy()
    fin_evo["delta"] = fin_evo["nb_medailles_paris2024"] - fin_evo["nb_medailles_tokyo"]
    fin_evo = fin_evo[fin_evo["delta"] != 0].sort_values("delta", ascending=False)
    fig3 = px.bar(
        fin_evo, x="delta", y="federation", orientation="h",
        color="delta",
        color_continuous_scale=[[0,BRZ],[0.5,"#EEEEEE"],[1,VERT]],
        labels={"delta":"Δ médailles","federation":""},
    )
    fig3.update_layout(height=380, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Tableau complet")
st.dataframe(fin, use_container_width=True)
