"""
pages/2_Historique.py
Page 2 — Historique olympique France 1996-2024
"""

import sys
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.database import load_historique

st.set_page_config(page_title="Historique · SportPerf", page_icon="📈", layout="wide")

BLEU = "#003D7C"
OR   = "#C8963E"
ARG  = "#888780"
BRZ  = "#7B4A2D"

historique = load_historique()

st.title("📈 Historique olympique France")
st.markdown("**1996 → 2024 · 8 éditions des Jeux Olympiques**")
st.markdown("---")

# ── KPIs ────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Meilleur total",   f"{historique['total'].max()} médailles",  "Paris 2024")
c2.metric("Meilleur rang",    f"#{historique['rang_mondial'].min()}",     "Atlanta & Paris")
c3.metric("Plus d'athlètes", f"{historique['athletes_engages'].max()}",  "Paris 2024")
c4.metric("Éditions analysées", len(historique))

st.markdown("---")

# ── Barres empilées ──────────────────────────────
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=historique["jo"], y=historique["or"],     name="Or",     marker_color=OR))
fig1.add_trace(go.Bar(x=historique["jo"], y=historique["argent"], name="Argent", marker_color=ARG))
fig1.add_trace(go.Bar(x=historique["jo"], y=historique["bronze"], name="Bronze", marker_color=BRZ))
fig1.update_layout(
    barmode="stack", height=380,
    title="Médailles France par édition des JO",
    xaxis_tickangle=-30,
    legend=dict(orientation="h", y=-0.25),
)
st.plotly_chart(fig1, use_container_width=True)

col_l, col_r = st.columns(2)

with col_l:
    fig2 = px.line(
        historique, x="jo", y="total",
        markers=True, title="Évolution du total de médailles",
        text="total",
    )
    fig2.update_traces(
        line_color=BLEU, marker_size=10,
        textposition="top center",
    )
    fig2.update_layout(height=320, xaxis_tickangle=-30)
    st.plotly_chart(fig2, use_container_width=True)

with col_r:
    fig3 = px.line(
        historique, x="jo", y="rang_mondial",
        markers=True, title="Classement mondial de la France",
    )
    fig3.update_yaxes(autorange="reversed", title="Rang (1 = meilleur)")
    fig3.update_traces(line_color=OR, marker_size=10)
    fig3.update_layout(height=320, xaxis_tickangle=-30)
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Données complètes")
st.dataframe(historique, use_container_width=True)
