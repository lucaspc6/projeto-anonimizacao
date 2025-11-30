import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import hashlib
import os

INPUT_FILE = "data/generated_raw_data.csv"
OUTPUT_FILE = "data/anonymized_data.csv"

# ============================================================
# 1 — CARREGAMENTO
# ============================================================

def load_data():
    return pd.read_csv(INPUT_FILE)

# ============================================================
# 2 — ANONIMIZAÇÃO
# ============================================================

def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]  # reduzido p/ não reidentificar

def anonymize_direct_identifiers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Identificadores diretos
    df["player_id"] = df["player_id"].apply(hash_value)
    df["name"] = df["name"].apply(hash_value)
    df["nationality"] = df["nationality"].apply(lambda x: x[:3])  # generalização mínima

    return df

# ============================================================
# 3 — SUPRESSÃO E GENERALIZAÇÃO
# ============================================================

def generalize_numerical(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Faixas de idade
    df["age"] = pd.cut(
        df["age"],
        bins=[0, 20, 25, 30, 35, 100],
        labels=["<=20", "21-25", "26-30", "31-35", ">=36"]
    )

    # Altura arredondada para generalização
    df["height"] = df["height"].apply(lambda x: round(x, 1))

    return df

# ============================================================
# 4 — AGRUPAMENTO K-MEANS PARA SIMILARIDADE
# ============================================================

CLUSTER_FEATURES = [
    "overall_rating",
    "pace", "shooting", "passing",
    "dribbling", "defending", "physical",
    "weight", "height"
]

def group_by_similarity(df: pd.DataFrame, n_clusters=8) -> pd.DataFrame:
    df = df.copy()

    scaler = StandardScaler()
    X = scaler.fit_transform(df[CLUSTER_FEATURES])

    model = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = model.fit_predict(X)

    return df

# ============================================================
# 5 — EXECUÇÃO FINAL
# ============================================================

def save(df: pd.DataFrame):
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Arquivo salvo: {OUTPUT_FILE}")

def anonymize_dataset(df):
    df = anonymize_direct_identifiers(df)
    df = generalize_numerical(df)
    return df

if __name__ == "__main__":
    raw = load_data()
    anon = anonymize_dataset(raw)
    grouped = group_by_similarity(anon, n_clusters=8)
    save(grouped)
