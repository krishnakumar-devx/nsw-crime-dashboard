# NSW Crime Intelligence Dashboard

An interactive Streamlit dashboard that explores crime patterns across New South Wales using cleaned BOCSAR crime data, population context, police station coverage, and LGA boundary data.

## Project Overview

This project was created for a data visualisation assignment focused on building a data narrative, not just a static dashboard. The dashboard is designed to show:

- how crime changes over time across NSW
- which offence categories are most significant
- which LGAs carry the highest crime burden
- how crime patterns compare with population and police station coverage

The storytelling angle is community safety: moving from broad statewide patterns to local LGA-level pressure and context.

## Features

- KPI cards for high-level crime indicators
- LGA-level choropleth map using NSW boundary data
- monthly and yearly trend views
- offence category breakdowns
- crime rate comparisons using population data
- police station coverage context
- cleaned multi-source data integrated into one dashboard

## Dataset Files

The app uses the following cleaned CSV files from `final_csvs/`:

- `nsw_lga_crime_tableau_clean.csv`
- `nsw_daily_crime_grouped_clean.csv`
- `nsw_lga_avg_population_2021_2025_clean.csv`
- `nsw_police_station_count_by_lga_clean.csv`
- `nsw_police_stations_with_lga_clean.csv`

It also uses:

- `nsw_lga.geojson` for the NSW LGA boundary map

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- GeoPandas

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- README.md
|-- nsw_lga.geojson
|-- final_csvs/
|   |-- nsw_daily_crime_grouped_clean.csv
|   |-- nsw_lga_avg_population_2021_2025_clean.csv
|   |-- nsw_lga_crime_tableau_clean.csv
|   |-- nsw_police_station_count_by_lga_clean.csv
|   `-- nsw_police_stations_with_lga_clean.csv
`-- .streamlit/
```

## How To Run

1. Create and activate a Python environment if you want to keep dependencies isolated.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python -m streamlit run "app.py"
```

4. Open the local Streamlit URL shown in the terminal, usually:

`http://localhost:8501`

## Notes

- The boundary GeoJSON file can be large, so a lighter version may be preferable for publishing or deployment.
- The dashboard depends on local data files being present in the paths shown above.

## Author

Project prepared as part of a data visualisation coursework submission on NSW crime trends and community safety.
