import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()

OUTPUT_FILE = "data/generated_raw_data.csv"

def generate_player():
    return {
        "player_id": fake.uuid4(),
        "name": fake.name(),
        "age": random.randint(16, 40),
        "height": round(random.uniform(1.60, 2.05), 2),
        "weight": random.randint(55, 110),
        "nationality": fake.country(),
        "overall_rating": random.randint(50, 99),
        "pace": random.randint(20, 99),
        "shooting": random.randint(20, 99),
        "passing": random.randint(20, 99),
        "dribbling": random.randint(20, 99),
        "defending": random.randint(20, 99),
        "physical": random.randint(20, 99)
    }

def generate_dataset(n=500):
    return pd.DataFrame([generate_player() for _ in range(n)])

def ensure_data_folder():
    if not os.path.exists("data"):
        os.makedirs("data")

if __name__ == "__main__":
    ensure_data_folder()
    df = generate_dataset(500)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Arquivo gerado: {OUTPUT_FILE}")
