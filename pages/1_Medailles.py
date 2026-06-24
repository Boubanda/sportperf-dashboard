"""
pages/1_Medailles.py
Page 1 — Médailles France · JO Paris 2024
"""

import sys
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.database import load_medailles, load_federations

st.set_page_config(page_title="Médailles · SportPerf", page_icon="🥇", layout="wide")

COULEURS = {"Or": "#C8963E", "Argent": "#888780", "Bronze": "#7B4A2D"}
BLEU     = "#003D7C"
VERT     = "#1D9E75"

medailles   = load_medailles()
federations = load_federations()

# ── Sidebar filtres ──────────────────────────────
with st.sidebar:
    st.markdown("## 🥇 Filtres")
    disciplines = ["Toutes"] + sorted(medailles["discipline"].unique().tolist())
    disc_sel    = st.selectbox("Discipline", disciplines)
    med_types   = ["Toutes", "Or", "Argent", "Bronze"]
    med_sel     = st.selectbox("Médaille", med_types)
    genres      = ["Tous", "H", "F", "Mixte"]
    genre_sel   = st.selectbox("Genre", genres)

df = medailles.copy()
if disc_sel  != "Toutes": df = df[df["discipline"] == disc_sel]
if med_sel   != "Toutes": df = df[df["medaille"] == med_sel]
if genre_sel != "Tous":   df = df[df["genre"] == genre_sel]

# ── Header ───────────────────────────────────────
st.title("🥇 Médailles France — Paris 2024")
st.markdown("---")

# ── KPIs ────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total",    len(df))
c2.metric("🥇 Or",    len(df[df["medaille"]=="Or"]))
c3.metric("🥈 Argent",len(df[df["medaille"]=="Argent"]))
c4.metric("🥉 Bronze",len(df[df["medaille"]=="Bronze"]))
c5.metric("Disciplines", df["discipline"].nunique())

st.markdown("---")

# ── Graphiques ───────────────────────────────────
col_l, col_r = st.columns(2)

with col_l:
    st.subheader("Médailles par discipline")
    by_disc = df.groupby(["discipline","medaille"]).size().reset_index(name="n")
    fig = px.bar(
        by_disc, x="n", y="discipline", color="medaille",
        color_discrete_map=COULEURS, orientation="h",
    )
    fig.update_layout(height=440, yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("Répartition Or / Argent / Bronze")
    pie = df["medaille"].value_counts().reset_index()
    pie.columns = ["medaille","n"]
    fig2 = px.pie(
        pie, values="n", names="medaille",
        color="medaille", color_discrete_map=COULEURS, hole=0.45,
    )
    fig2.update_layout(height=220)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Répartition par genre")
    genre_df = df["genre"].value_counts().reset_index()
    genre_df.columns = ["genre","n"]
    fig3 = px.bar(
        genre_df, x="genre", y="n", color="genre",
        color_discrete_map={"H": BLEU, "F": VERT, "Mixte": "#C8963E"},
    )
    fig3.update_layout(height=190, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Tableau détaillé")
st.dataframe(
    df[["athlete","discipline","medaille","genre"]].reset_index(drop=True),
    use_container_width=True, height=280,
)
