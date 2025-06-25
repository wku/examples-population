import sys
import requests
from lxml import html
from sqlalchemy import create_engine, text

URL = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
DB_URL = "postgresql://user:password@db:5432/population_db"

def parse():
   print("Starting parsing...")
   response = requests.get(URL)
   tree = html.fromstring(response.content)
   table = tree.xpath('//table[@class="wikitable sortable"]')[0]
   rows = table.xpath('.//tr')[1:]
   
   data = []
   for row in rows:
       cells = row.xpath('.//td')
       if len(cells) >= 4:
           country = cells[0].text_content().strip()
           region = cells[1].text_content().strip()
           pop_text = cells[2].text_content().strip().replace(',', '')
           try:
               population = int(pop_text)
               data.append((country, region, population))
           except ValueError:
               continue
   
   engine = create_engine(DB_URL)
   engine.execute(text("DROP TABLE IF EXISTS population"))
   engine.execute(text("""
       CREATE TABLE population (
           "Country or territory" TEXT,
           "UN continental region[1]" TEXT,
           "Population (1 July 2023)" INTEGER
       )
   """))
   
   for country, region, pop in data:
       engine.execute(text("""
           INSERT INTO population VALUES (:country, :region, :pop)
       """), country=country, region=region, pop=pop)
   
   print("Data saved to population table.")

def stats():
   print("Starting stats calculation...")
   engine = create_engine(DB_URL)
   
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
   
   results = engine.execute(sql_query).fetchall()
   
   for row in results:
       print(f"Назва регіону: {row[0]}")
       print(f"Загальне населення регіону: {row[1]}")
       print(f"Назва найбільшої країни в регіоні: {row[2]}")
       print(f"Населення найбільшої країни в регіоні: {row[3]}")
       print(f"Назва найменшої країни в регіоні: {row[4]}")
       print(f"Населення найменшої країни в регіоні: {row[5]}\n")

if __name__ == "__main__":
   command = sys.argv[1]
   if command == "parse": parse()
   elif command == "stats": stats()
