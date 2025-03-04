import sys
import pandas as pd
from sqlalchemy import create_engine
import time

URL = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
DB_URL = "postgresql://user:password@db:5432/population_db"

def parse():
    print("Starting parsing...")
    df = pd.read_html(URL)[0]
    print("Data parsed successfully, saving to DB...")
    engine = create_engine(DB_URL)
    df.to_sql("population", engine, if_exists="replace", index=False)
    print("Data saved to population table.")

def stats():
    print("Starting stats calculation...")
    engine = create_engine(DB_URL)

    for _ in range(10):
        try:
            df = pd.read_sql("SELECT * FROM population", engine)
            break
        except:
            print("Waiting for population table to be created...")
            time.sleep(1)
    else:
        raise Exception("Table 'population' was not created in time.")
    
    df["Population (1 July 2023)"] = pd.to_numeric(df["Population (1 July 2023)"], errors="coerce")
    agg = df.groupby("UN continental region[1]").agg(
        total_pop=("Population (1 July 2023)", "sum"),
        max_country=("Country or territory", lambda x: x[df.loc[x.index, "Population (1 July 2023)"].idxmax()]),
        max_pop=("Population (1 July 2023)", "max"),
        min_country=("Country or territory", lambda x: x[df.loc[x.index, "Population (1 July 2023)"].idxmin()]),
        min_pop=("Population (1 July 2023)", "min")
    ).dropna()
    for region, row in agg.iterrows():
        print(f"Назва регіону: {region}")
        print(f"Загальне населення регіону: {row['total_pop']}")
        print(f"Назва найбільшої країни в регіоні: {row['max_country']}")
        print(f"Населення найбільшої країни в регіоні: {row['max_pop']}")
        print(f"Назва найменшої країни в регіоні: {row['min_country']}")
        print(f"Населення найменшої країни в регіоні: {row['min_pop']}\n")

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "parse": parse()
    elif command == "stats": stats()

    