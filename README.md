# UN Population Data Parser

## Overview

This project provides a minimalist Python-based solution for parsing and analyzing population data from Wikipedia's "List of countries by population (United Nations)" page. The system extracts the data, stores it in a PostgreSQL database, and generates statistical insights about population by continental regions.

## Components

The project contains Python scripts that perform two main functions:

1. **Data Parsing**: Extracts the population table from Wikipedia and stores it in PostgreSQL
2. **Statistical Analysis**: Calculates regional population statistics including:
   - Total population by continent
   - Largest country in each region (by population)
   - Smallest country in each region (by population)

## Requirements

- Python 3.x
- pandas
- SQLAlchemy
- PostgreSQL database

## Configuration

The scripts use the following default configuration:

- Wikipedia URL: `https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)`
- Database connection: `postgresql://user:password@db:5432/population_db`

## Usage

The system is designed to be run via command line with specific commands:

### Parsing the data

```bash
python script.py parse
```

This command will:
- Fetch the Wikipedia page
- Extract the population data table
- Store it in the PostgreSQL database under table name "population"

### Generating statistics

```bash
python script.py stats
```

This command will:
- Connect to the database
- Ensure the population table exists
- Group data by UN continental regions
- Calculate and display statistics for each region in Ukrainian

## Versions

There are three script versions included in the project:

1. **Basic Version**: Uses pandas for both parsing and statistics generation
2. **Duplicate Version**: Identical to the basic version (maintained for reference)
3. **SQL-Optimized Version**: Uses a SQL query to perform regional statistics calculations directly in the database for better performance

## Output Example

The statistics output follows this format for each continental region:

```
Назва регіону: [Region Name]
Загальне населення регіону: [Total Population]
Назва найбільшої країни в регіоні: [Largest Country Name]
Населення найбільшої країни в регіоні: [Largest Country Population]
Назва найменшої країни в регіоні: [Smallest Country Name]
Населення найменшої країни в регіоні: [Smallest Country Population]
```

## Notes

- The system includes retry logic to handle the case where the parsing process is still in progress when statistics are requested
- The SQL-optimized version demonstrates a more efficient approach for larger datasets
