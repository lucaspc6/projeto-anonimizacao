import pandas as pd
import uuid
import numpy as np

# ============================================================
# Generalização fina dos atributos
# ============================================================

def bucket_age_fine(age):
    if age <= 20: return "≤20"
    if age <= 25: return "21–25"
    if age <= 30: return "26–30"
    if age <= 35: return "31–35"
    return ">35"

def bucket_height_fine(h):
    if h < 170: return "<170"
    if h < 180: return "170–179"
    if h < 190: return "180–189"
    return "≥190"

def nat_to_region_fine(n):
    eu = ["France", "Germany", "Spain", "Italy", "Portugal", "England"]
    sa = ["Brazil", "Argentina"]
    if n in eu: return "Europe"
    if n in sa: return "South America"
    return "Other"

# ============================================================
# Perturbação numérica
# ============================================================

def add_noise_value(val):
    noise = np.random.uniform(-0.04, 0.04)
    return int(val * (1 + noise))

# ============================================================
# AGRUPAMENTO POR SIMILARIDADE (NOVO REQUISITO)
# ============================================================

def group_players_by_similarity(df: pd.DataFrame) -> dict:
    """
    Agrupa jogadores por características similares:
    - age_bucket
    - height_bucket
    - pos_group
    """
    groups = {}

    for idx, row in df.iterrows():
        key = (
            str(row["age_bucket"]),
            str(row["height_bucket"]),
            str(row["pos_group"]),
        )

        if key not in groups:
            groups[key] = []

        groups[key].append(idx)

    return groups


def add_group_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Atribui um UUID para cada grupo de jogadores semelhantes.
    """
    out = df.copy()
    groups = group_players_by_similarity(df)

    out["group_id"] = None

    for key, idx_list in groups.items():
        gid = uuid.uuid4().hex
        out.loc[idx_list, "group_id"] = gid

    return out

# ============================================================
# K-ANONIMIDADE SUAVE
# ============================================================

def enforce_k_soft(df, quasi_identifiers, k=3):
    """
    Verifica se cada combinação QID tem pelo menos k elementos.
    Se não tiver, generaliza automaticamente.
    """
    out = df.copy()

    for q in quasi_identifiers:
        out[q] = out[q].astype(str)

    while True:
        counts = out.groupby(quasi_identifiers).size()

        violators = counts[counts < k]

        if len(violators) == 0:
            break

        for key in violators.index:
            mask = np.ones(len(key), dtype=bool)
            generalization = "OTHER"
            out.loc[
                (out[quasi_identifiers] == key).all(axis=1),
                quasi_identifiers[-1]
            ] = generalization

    return out

# ============================================================
# PIPELINE COMPLETA DE ANONIMIZAÇÃO
# ============================================================

def anonymize(raw: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    anon = pd.DataFrame()

    # 1. Criar identificador irreversível
    anon["player_id"] = [uuid.uuid4().hex for _ in range(len(raw))]

    # 2. Generalizações
    anon["age_bucket"]    = raw["age"].map(bucket_age_fine)
    anon["height_bucket"] = raw["height_cm"].map(bucket_height_fine)
    anon["pos_group"]     = raw["position"]
    anon["region_nat"]    = raw["nationality"].map(nat_to_region_fine)

    # 3. Atributos não identificadores
    anon["pace"] = raw["pace"]
    anon["market_value_eur_noisy"] = raw["market_value_eur"].map(add_noise_value)

    # 4. Agrupamento por similaridade (NOVO)
    anon = add_group_id(anon)

    # 5. K-anonymity
    QIDS = ["age_bucket", "height_bucket", "pos_group", "region_nat"]
    anon = enforce_k_soft(anon, QIDS, k=k)

    return anon

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    raw = pd.read_csv("data/players_raw.csv")
    anon = anonymize(raw)
    anon.to_csv("data/players_anon.csv", index=False)
    print("Arquivo gerado: data/players_anon.csv")
