import os
import numpy as np
import pandas as pd

os.makedirs('data', exist_ok=True)

np.random.seed(7)
N = 200
positions = ["GK","DEF","MID","FWD"]
nations = ["Brazil","Argentina","Spain","Germany","USA","Japan","Nigeria"]
leagues = [
    "Serie A (BR)", "LaLiga", "Bundesliga",
    "Premier League", "MLS", "J1 League", "Liga Profesional (AR)"
]

rows = []
for i in range(1, N+1):
    pos = np.random.choice(positions, p=[0.1,0.35,0.35,0.2])
    nat = np.random.choice(nations)
    league = np.random.choice(leagues)
    age = np.random.randint(17, 41)
    height = int(np.random.normal({"GK":190,"DEF":184,"MID":178,"FWD":180}[pos], 5))
    pace = int(np.clip(np.random.normal({"GK":40,"DEF":65,"MID":72,"FWD":82}[pos], 8), 20, 99))
    value = int(np.random.lognormal(mean=15, sigma=0.35))

    rows.append({
        "player_name": f"Player{i:04d}",
        "email": f"p{i:04d}@club.com",
        "age": age,
        "league": league,
        "nationality": nat,
        "position": pos,
        "height_cm": height,
        "pace": pace,
        "market_value_eur": value
    })

df = pd.DataFrame(rows)

excel_path = "data/players_raw.xlsx"
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Players", index=False)

print(f"Arquivo Excel gerado com {len(df)} linhas. Cada valor está em sua célula.")