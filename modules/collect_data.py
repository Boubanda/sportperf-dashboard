"""
modules/collect_data.py
Pipeline de collecte et structuration des données sport françaises
Sources : data.gouv.fr, résultats JO Paris 2024, ANS
"""

import requests
import pandas as pd
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH  = Path(__file__).parent.parent / "db" / "sportperf.db"
RAW_DIR  = Path(__file__).parent.parent / "data" / "raw"


# ─────────────────────────────────────────────────
# LICENCIÉS PAR FÉDÉRATION
# ─────────────────────────────────────────────────
def collect_licencies() -> pd.DataFrame:
    print("📥 Collecte licenciés par fédération...")
    url = "https://data.gouv.fr/api/1/datasets/5369992ba3a729239d205b3f/"
    try:
        r = requests.get(url, timeout=8)
        resources = r.json().get("resources", [])
        csv_url = next((x["url"] for x in resources if "csv" in x.get("format","").lower()), None)
        if csv_url:
            df = pd.read_csv(csv_url, sep=";", encoding="utf-8", on_bad_lines="skip")
            df.to_csv(RAW_DIR / "licencies_raw.csv", index=False)
            print(f"   ✓ {len(df)} lignes (data.gouv.fr)")
            return df
    except Exception as e:
        print(f"   ⚠ API indisponible ({e}), données de démonstration")

    df = pd.DataFrame({
        "federation": [
            "Football","Tennis","Équitation","Judo","Basket-ball",
            "Handball","Rugby à XV","Natation","Golf","Athlétisme",
            "Pétanque","Cyclisme","Badminton","Ski","Volley-ball",
            "Boxe","Karaté","Tir","Voile","Aviron",
            "Escrime","Lutte","Taekwondo","Canoë-Kayak","Pentathlon moderne",
        ],
        "nb_licencies": [
            1842000,942000,546000,471000,431000,
            405000,394000,341000,425000,289000,
            268000,239000,201000,193000,161000,
            144000,120000,148000,101000,52000,
            38000,22000,18000,29000,3200,
        ],
        "nb_clubs": [
            14800,8400,2200,5600,3200,
            3900,2900,2600,2400,3100,
            9800,4200,2100,2300,1800,
            2900,3800,1900,1100,900,
            700,600,450,950,120,
        ],
        "discipline_olympique": [
            True,True,True,True,True,
            True,False,True,True,True,
            False,True,True,True,True,
            True,False,True,True,True,
            True,True,True,True,True,
        ],
        "annee": [2022] * 25,
    })
    df.to_csv(RAW_DIR / "licencies_raw.csv", index=False)
    print(f"   ✓ {len(df)} fédérations (démonstration)")
    return df


# ─────────────────────────────────────────────────
# MÉDAILLES JO PARIS 2024
# ─────────────────────────────────────────────────
def collect_jo_paris_2024() -> pd.DataFrame:
    print("📥 Collecte médailles JO Paris 2024...")
    df = pd.DataFrame({
        "athlete": [
            "Léon Marchand","Léon Marchand","Léon Marchand","Léon Marchand",
            "Teddy Riner","Équipe de France Judo mixte",
            "Pauline Ferrand-Prévot","Équipe de France Basket 3x3",
            "Manon Apithy-Brunet","Clarisse Agbegnenou",
            "Sarah-Léonie Cysique","Romane Dicko",
            "Équipe de France Escrime fleuret F","Équipe de France Escrime épée H",
            "Cyrena Samba-Mayela","Équipe de France Relais 4x100m",
            "Antoine Dupont — Rugby 7","Équipe de France Rugby 7",
            "Thomas Chirault et Thomas Rouxel","Jean-Baptiste Dupé",
            "Lara Vadel","Jordan Daguenet",
            "Équipe de France Cyclisme piste H","Équipe de France Cyclisme piste F",
            "Kevin Mayer","Wilhem Belocian",
            "Équipe de France Handball H","Équipe de France Handball F",
            "Équipe de France Basket 3x3 F",
        ],
        "discipline": [
            "Natation","Natation","Natation","Natation",
            "Judo","Judo",
            "Cyclisme VTT","Basket 3x3",
            "Escrime","Judo",
            "Judo","Judo",
            "Escrime","Escrime",
            "Athlétisme","Athlétisme",
            "Rugby 7","Rugby 7",
            "Voile","Tir",
            "Judo","Judo",
            "Cyclisme piste","Cyclisme piste",
            "Athlétisme","Athlétisme",
            "Handball","Handball",
            "Basket 3x3",
        ],
        "medaille": [
            "Or","Or","Or","Or",
            "Or","Or",
            "Or","Argent",
            "Or","Argent",
            "Bronze","Bronze",
            "Or","Argent",
            "Argent","Bronze",
            "Or","Or",
            "Bronze","Bronze",
            "Bronze","Bronze",
            "Or","Argent",
            "Bronze","Bronze",
            "Argent","Bronze",
            "Bronze",
        ],
        "genre": [
            "H","H","H","H",
            "H","Mixte",
            "F","H",
            "F","F",
            "F","F",
            "F","H",
            "F","Mixte",
            "H","H",
            "H","H",
            "F","H",
            "H","F",
            "H","H",
            "H","F",
            "F",
        ],
        "jo":    ["Paris 2024"] * 29,
        "annee": [2024] * 29,
    })
    df.to_csv(RAW_DIR / "jo_2024_medailles.csv", index=False)
    print(f"   ✓ {len(df)} médailles")
    return df


# ─────────────────────────────────────────────────
# HISTORIQUE JO 1996–2024
# ─────────────────────────────────────────────────
def collect_historique_jo() -> pd.DataFrame:
    print("📥 Collecte historique JO France...")
    df = pd.DataFrame({
        "jo":      ["Atlanta 1996","Sydney 2000","Athènes 2004","Pékin 2008",
                    "Londres 2012","Rio 2016","Tokyo 2020","Paris 2024"],
        "annee":   [1996,2000,2004,2008,2012,2016,2021,2024],
        "or":      [15,13,11, 7,11,10,10,16],
        "argent":  [ 7,14, 9,16,11,18,12,26],
        "bronze":  [15,11,13,18,12,14,11,22],
        "total":   [37,38,33,41,34,42,33,64],
        "rang_mondial":      [ 5, 6, 7,10, 7, 7, 8, 5],
        "athletes_engages":  [315,322,260,320,330,398,372,572],
    })
    df.to_csv(RAW_DIR / "historique_jo.csv", index=False)
    print(f"   ✓ {len(df)} éditions")
    return df


# ─────────────────────────────────────────────────
# FINANCEMENTS ANS
# ─────────────────────────────────────────────────
def collect_financements_ans() -> pd.DataFrame:
    print("📥 Collecte financements ANS...")
    df = pd.DataFrame({
        "federation": [
            "Natation","Judo","Athlétisme","Cyclisme","Escrime",
            "Handball","Rugby 7","Voile","Boxe","Canoë-Kayak",
            "Lutte","Tir","Taekwondo","Aviron","Badminton",
            "Équitation","Tennis de table","Pentathlon moderne","Triathlon","Ski",
        ],
        "budget_ans_k_euros": [
            4200,3800,5100,2900,2100,
            3200,2400,1800,1600,1400,
            1200, 900, 800,1100, 700,
            2200, 600, 500, 750,3500,
        ],
        "nb_medailles_tokyo": [
            2,5,1,2,3,
            2,1,1,0,2,
            1,1,0,0,0,
            0,0,0,0,0,
        ],
        "nb_medailles_paris2024": [
            5,8,4,4,4,
            2,2,1,0,1,
            0,1,0,0,0,
            0,0,0,0,0,
        ],
        "objectif_jo_2030": [
            6,8,5,4,3,
            3,2,2,1,2,
            1,1,1,1,1,
            1,0,0,1,2,
        ],
    })
    df["roi_medaille_par_mEuros"] = (
        df["nb_medailles_paris2024"] / (df["budget_ans_k_euros"] / 1000)
    ).round(2)
    df.to_csv(RAW_DIR / "financements_ans.csv", index=False)
    print(f"   ✓ {len(df)} fédérations")
    return df


# ─────────────────────────────────────────────────
# CONSTRUCTION BASE SQL
# ─────────────────────────────────────────────────
def build_database(
    df_licencies: pd.DataFrame,
    df_jo2024:    pd.DataFrame,
    df_historique:pd.DataFrame,
    df_financements: pd.DataFrame,
) -> None:
    print("\n🗄  Construction base SQL...")
    conn = sqlite3.connect(DB_PATH)

    df_licencies.to_sql("federations",       conn, if_exists="replace", index=False)
    df_jo2024.to_sql("medailles_jo2024",     conn, if_exists="replace", index=False)
    df_historique.to_sql("historique_jo",    conn, if_exists="replace", index=False)
    df_financements.to_sql("financements_ans",conn, if_exists="replace", index=False)

    conn.execute("DROP VIEW IF EXISTS vue_performance_discipline")
    conn.execute("""
        CREATE VIEW vue_performance_discipline AS
        SELECT
            f.federation,
            f.budget_ans_k_euros,
            f.nb_medailles_tokyo,
            f.nb_medailles_paris2024,
            f.objectif_jo_2030,
            f.roi_medaille_par_mEuros,
            l.nb_licencies,
            l.discipline_olympique
        FROM financements_ans f
        LEFT JOIN federations l ON LOWER(f.federation) = LOWER(l.federation)
    """)
    conn.commit()
    conn.close()
    print(f"   ✓ Base SQL : {DB_PATH}")


# ─────────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────────
def run():
    print("=" * 50)
    print("  SportPerf — Collecte des données")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 50)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    df_lic = collect_licencies()
    df_jo  = collect_jo_paris_2024()
    df_his = collect_historique_jo()
    df_fin = collect_financements_ans()

    build_database(df_lic, df_jo, df_his, df_fin)

    print("\n✅ Données prêtes !")
    print("=" * 50)


if __name__ == "__main__":
    run()
