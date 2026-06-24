"""
app.py — Point d'entrée unique du dashboard SportPerf
Lance avec : streamlit run app.py
"""

import sys
import streamlit as st
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from modules.database import db_exists

st.set_page_config(
    page_title="SportPerf Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Sidebar commune ──────────────────────────────
with st.sidebar:
    st.markdown("##  SportPerf")
    st.markdown("Analyse de la performance sportive française")
    st.markdown("---")
    st.markdown("**ANS · JO Paris 2024 · JO 2030**")
    st.markdown("---")
    st.caption("Levi Junior BOUBANDA")
    st.caption("MSc IA & Data Science · Aivancity")

# ─── Page d'accueil ───────────────────────────────
st.title(" SportPerf Dashboard")
st.markdown("### Analyse de la performance sportive française")
st.markdown("---")

if not db_exists():
    st.error("⚠️ Base de données introuvable. Lance d'abord :")
    st.code("python modules/collect_data.py", language="bash")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.info("**Page 1**\n\n🥇 Médailles\n\nParis 2024")
col2.info("**Page 2**\n\n📈 Historique\n\n1996 → 2024")
col3.info("**Page 3**\n\n💰 Financements\n\nROI & budget ANS")
col4.info("**Page 4**\n\n🔮 Prédictions\n\nXGBoost · JO 2030")

st.markdown("---")
st.markdown("""
**Navigation** : utilise le menu dans la **sidebar à gauche** pour accéder aux 4 pages.

**Sources de données**
- Licenciés par fédération : INJEP / data.gouv.fr
- Résultats JO Paris 2024 : paris2024.org
- Financements ANS : rapports annuels ANS
- Historique olympique : open data olympique
""")
st.success("✅ Base de données chargée — toutes les pages sont disponibles.")
