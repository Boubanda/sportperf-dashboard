"""
modules/database.py
Chargement centralisé des données depuis la base SQLite.
Toutes les pages importent depuis ce module — une seule source de vérité.
"""

import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "sportperf.db"


def db_exists() -> bool:
    return DB_PATH.exists()


@st.cache_data
def load_medailles() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM medailles_jo2024", conn)
    conn.close()
    return df


@st.cache_data
def load_historique() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM historique_jo ORDER BY annee", conn)
    conn.close()
    return df


@st.cache_data
def load_financements() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM financements_ans", conn)
    conn.close()
    return df


@st.cache_data
def load_federations() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM federations", conn)
    conn.close()
    return df


def load_all():
    """Charge toutes les tables en une seule fois."""
    return (
        load_medailles(),
        load_historique(),
        load_financements(),
        load_federations(),
    )
