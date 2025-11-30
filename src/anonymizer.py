import os
import uuid
import numpy as np
import pandas as pd

def bucket_age_fine(age: pd.Series) -> pd.Series:
    bins   = [0, 20, 24, 29, 34, 40, 120]
    labels = ["<=20", "21-24", "25-29", "30-34", "35-40", "40+"]
    return pd.cut(age, bins=bins, labels=labels, include_lowest=True)

def bucket_height_fine(h: pd.Series) -> pd.Series:
    bins   = [0, 170, 175, 180, 185, 190, 300]
    labels = ["<170", "170-174", "175-179", "180-184", "185-189", "190+"]
    return pd.cut(h, bins=bins, labels=labels, include_lowest=True)

def nat_to_region_fine(nat: pd.Series) -> pd.Series:
    m = {
        "Brazil": "SA", "Argentina": "SA",
        "Spain": "EU", "Germany": "EU",
        "USA": "NA", "Japan": "AS", "Nigeria": "AF",
    }
    return nat.map(m).fillna("OTHER")


AGE_COARSE_MAP = {
    "<=20": "<=24",
    "21-24": "<=24",
    "25-29": "25-34",
    "30-34": "25-34",
    "35-40": "35+",
    "40+": "35+",
}
HEIGHT_COARSE_MAP = {
    "<170": "<=175",
    "170-174": "<=175",
    "175-179": "176-185",
    "180-184": "176-185",
    "185-189": ">=186",
    "190+": ">=186",
}
POS_COARSE_MAP = {"GK": "GK", "DEF": "OUTFIELD", "MID": "OUTFIELD", "FWD": "OUTFIELD"}


def generalize_series_with_map(sr: pd.Series, mapping: dict) -> pd.Series:
    as_str = sr.astype(str)
    return as_str.map(lambda v: mapping.get(v, v))

def add_noise_value(v: pd.Series, sigma: float = 0.12, seed: int = 42) -> pd.Series:
    rng = np.random.default_rng(seed)
    noise = rng.lognormal(mean=0, sigma=sigma, size=len(v))
    return (v * noise).round(-2)

# ============================================================
# k-anonimato sem '*'
# ============================================================
def enforce_k_soft(anon: pd.DataFrame, qids: list[str], k: int = 3, seed: int = 7) -> pd.DataFrame:
    out = anon.copy()
    rng = np.random.default_rng(seed)

    for q in qids:
        out[q] = out[q].astype(object)

    def group_counts(df):
        return df.groupby(qids, observed=False).size().reset_index(name="n")

    def rare_mask(df):
        g = group_counts(df)
        rare = g[g["n"] < k][qids]
        if rare.empty:
            return pd.Series(False, index=df.index)
        m = df.merge(rare.assign(_r=1), on=qids, how="left")["_r"].fillna(0).astype(int).eq(1)
        return m

    # Paso 1 a 5
    for col, mapping in [
        ("height_bucket", HEIGHT_COARSE_MAP),
        ("age_bucket", AGE_COARSE_MAP),
        ("pos_group", POS_COARSE_MAP)
    ]:
        mask = rare_mask(out)
        if mask.any():
            out.loc[mask, col] = generalize_series_with_map(out.loc[mask, col], mapping)

    mask = rare_mask(out)
    if mask.any():
        out.loc[mask, "region_nat"] = "GLOBAL"

    mask = rare_mask(out)
    if mask.any():
        common_region = out["region_nat"].value_counts().idxmax()
        out.loc[mask, "region_nat"] = common_region

    # Embaralhamento leve
    final_groups = out.groupby(qids, observed=False).groups
    for shuffle_cols in [["pace"], ["market_value_eur_noisy"]]:
        for _, idx in final_groups.items():
            idx = list(idx)
            if len(idx) > 1:
                for col in shuffle_cols:
                    out.loc[idx, col] = rng.permutation(out.loc[idx, col].values)

    return out

# ============================================================
# Função principal
# ============================================================
def anonymize(raw: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    anon = pd.DataFrame()

    anon["player_id"] = [uuid.uuid4().hex for _ in range(len(raw))]

    anon["age_bucket"]    = bucket_age_fine(raw["age"])
    anon["height_bucket"] = bucket_height_fine(raw["height_cm"])
    anon["pos_group"]     = raw["position"]
    anon["region_nat"]    = nat_to_region_fine(raw["nationality"])

    anon["pace"] = raw["pace"]

    anon["market_value_eur_noisy"] = add_noise_value(raw["market_value_eur"])

    QIDS = ["age_bucket", "height_bucket", "pos_group", "region_nat"]
    anon = enforce_k_soft(anon, QIDS, k=k)

    return anon

# Execução direta
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    xlsx_path = "data/players_raw.xlsx"
    csv_path  = "data/players_raw.csv"

    if os.path.exists(xlsx_path):
        raw = pd.read_excel(xlsx_path, sheet_name="Players", engine="openpyxl")
    elif os.path.exists(csv_path):
        raw = pd.read_csv(csv_path)
    else:
        raise SystemExit("Nenhum arquivo de entrada encontrado em data/.")

    out = anonymize(raw, k=3)

    out.to_csv("data/players_anon.csv", sep=';', index=False, encoding='utf-8-sig')
    print("CSV gerado -> data/players_anon.csv")

    with pd.ExcelWriter("data/players_anon.xlsx", engine="openpyxl") as writer:
        out.to_excel(writer, sheet_name="AnonPlayers", index=False)
    print("Excel gerado -> data/players_anon.xlsx")