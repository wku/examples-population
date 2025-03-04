import sys
import pandas as pd
from sqlalchemy import create_engine, text
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
            # Проверка существования таблицы
            pd.read_sql("SELECT 1 FROM population LIMIT 1", engine)
            break
        except:
            print("Waiting for population table to be created...")
            time.sleep(1)
    else:
        raise Exception("Table 'population' was not created in time.")
    
    # Компактный SQL-запрос для статистики
    sql_query = text("""
    SELECT
      c."UN continental region[1]" as region,
      SUM(c."Population (1 July 2023)") total,
      MAX(c."Country or territory") FILTER(WHERE c."Population (1 July 2023)"=(SELECT MAX("Population (1 July 2023)") FROM population WHERE "UN continental region[1]"=c."UN continental region[1]")) big_name,
      MAX(c."Population (1 July 2023)") max_pop,
      MAX(c."Country or territory") FILTER(WHERE c."Population (1 July 2023)"=(SELECT MIN("Population (1 July 2023)") FROM population WHERE "UN continental region[1]"=c."UN continental region[1]")) small_name,
      MIN(c."Population (1 July 2023)") min_pop
    FROM
      population c
    WHERE 
      c."UN continental region[1]" IS NOT NULL
    GROUP BY
      c."UN continental region[1]"
    ORDER BY
      total DESC;
    """)
    
    # Выполнение запроса
    results = pd.read_sql(sql_query, engine)
    
    # Вывод результатов
    for _, row in results.iterrows():
        print(f"Назва регіону: {row['region']}")
        print(f"Загальне населення регіону: {row['total']}")
        print(f"Назва найбільшої країни в регіоні: {row['big_name']}")
        print(f"Населення найбільшої країни в регіоні: {row['max_pop']}")
        print(f"Назва найменшої країни в регіоні: {row['small_name']}")
        print(f"Населення найменшої країни в регіоні: {row['min_pop']}\n")

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "parse": parse()
    elif command == "stats": stats()
