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

---

## Data dictionary

Definitions, types, and provenance for variables used by `app.py`. Types describe how the CSV is read in Python/Pandas unless noted.

**Authoritative NSW recorded-crime statistics portal:** [NSW Bureau of Crime Statistics and Research (BOCSAR)](https://bocsar.nsw.gov.au/) — incident-level downloads used in this project come from BOCSAR **Open datasets** ([statistics dashboards → Open datasets](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html)).

### `final_csvs/nsw_lga_crime_tableau_clean.csv`

_Source bundle (examples): monthly criminal incidents by LGA (`RCI_offencebymonth.xlsm` class of extract)._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `LGA` | NSW Local Government Area name (aligned across merges). | string | BOCSAR recorded crime open data; cleaned to long format. Portal: [BOCSAR](https://bocsar.nsw.gov.au/), datasets: [Open datasets](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html). |
| `Offence category` | Broad offence classification (aggregated subcategories in cleaning pipeline). | string | BOCSAR offence taxonomy ([BOCSAR](https://bocsar.nsw.gov.au/)). |
| `Month` | First day of calendar month for the observation. | datetime (parsed on load) | Derived from BOCSAR monthly workbook columns. |
| `Incident_Count` | Count of recorded incidents for that LGA × offence × month. | float/int | BOCSAR incident counts; zeros retained where present in source ([BOCSAR](https://bocsar.nsw.gov.au/)). |
| `Month_Label` | Human-readable month label (e.g. Jan-21). | string | Derived during cleaning for charts/labels. |
| `Year` | Calendar year extracted from `Month`. | integer | Derived. |
| `Month_Num` | Month number 1–12. | integer | Derived. |

### `final_csvs/nsw_daily_crime_grouped_clean.csv`

_Source bundle (examples): statewide daily incidents workbook (`NSW_criminal_incidents_daily.xlsx` class of extract)._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `Date` | Calendar date (daily NSW totals). | datetime (parsed on load) | BOCSAR statewide daily incident extract ([BOCSAR Open datasets](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html)); offences grouped to broad categories in cleaning. |
| `Offence category` | Broad offence classification consistent with LGA file. | string | Mapped from BOCSAR detailed labels ([BOCSAR](https://bocsar.nsw.gov.au/)). |
| `Incident_Count` | Incidents on that date for that offence category (statewide). | float | BOCSAR daily counts after grouping ([BOCSAR](https://bocsar.nsw.gov.au/)). |
| `Year` | Calendar year. | integer | Derived from `Date`. |
| `Month_Num` | Month number 1–12. | integer | Derived. |
| `Month_Label` | Short label for month (e.g. Jan-21). | string | Derived. |

*Note: This file is loaded in `load_all()` for pipeline parity; the current narrative Acts primarily use the monthly LGA dataset (`crime_df`).*

### `final_csvs/nsw_lga_avg_population_2021_2025_clean.csv`

_Not published by BOCSAR; used only as a **denominator** for rates. Incident **numerators** are BOCSAR ([BOCSAR](https://bocsar.nsw.gov.au/))._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `LGA` | Local Government Area name (matched to BOCSAR crime file naming). | string | ERP-style population projections by LGA from NSW open demographic/planning data; labels reconciled to BOCSAR LGAs for joins. Crime statistics authority: [BOCSAR](https://bocsar.nsw.gov.au/). |
| `ERP_2021` … `ERP_2025` | Estimated Resident Population (or projection) for that year by LGA. | float | Same NSW open-data ERP pipeline as above; see Credits. |
| `Avg_Population_2021_2025` | Mean of annual ERP columns over 2021–2025 (rounded in cleaning). | integer | Derived for rate denominators; incident counts remain BOCSAR. |
| `Population_2025` | Population figure for 2025 used as reference year where applicable. | integer | From ERP source column in pipeline above. |

### `final_csvs/nsw_police_station_count_by_lga_clean.csv`

_Not published by BOCSAR; **context layer** only. Incident counts remain BOCSAR ([BOCSAR](https://bocsar.nsw.gov.au/))._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `LGA` | Local Government Area. | string | Station points spatially assigned to LGA polygons; LGA labels aligned with BOCSAR crime tables. |
| `Police_Station_Count` | Number of stations attributed to that LGA after spatial matching and name cleaning. | integer | Derived from NSW spatial / policing facility point data + boundary layers (see Credits). |

### `final_csvs/nsw_police_stations_with_lga_clean.csv`

_Not published by BOCSAR; map overlay only. Crime narrative statistics: [BOCSAR](https://bocsar.nsw.gov.au/)._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `Station_Name` | Facility / station label from source layer. | string | NSW spatial / policing open GIS layer used for coordinates (see Credits). |
| `Longitude`, `Latitude` | WGS84 coordinates for map overlays. | float | Same layer as `Station_Name`. |
| `LGA` | LGA attributed by spatial join; may be empty where outside NSW LGA match. | string | Derived join to LGA boundaries; rows with missing coords omitted from maps in `app.py`. |

### `nsw_lga.geojson` (repository root)

_Not BOCSAR incident data; boundary geometry for choropleth joins to BOCSAR `LGA` labels._

| Element | Definition | Type | Provenance |
|---------|------------|------|------------|
| Feature geometry | Polygon boundaries for LGAs. | GeoJSON geometry | NSW administrative LGA boundaries (open spatial data); simplified for repo size where applicable. Join key aligned with BOCSAR crime CSV `LGA`. Official crime counts: [BOCSAR](https://bocsar.nsw.gov.au/). |
| `properties.LGA` | Attribute used as join key to tabular `LGA`. | string | Must match cleaned BOCSAR CSV `LGA` strings after `strip()` in `app.py`. |

### Derived fields (computed in code, not stored in raw CSVs)

These are built in `compute_lga_summary()` and downstream charts after filtering:

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `Total_Crime` | Sum of `Incident_Count` per LGA within current filters. | float | Aggregated from BOCSAR-based `crime_df` ([BOCSAR](https://bocsar.nsw.gov.au/)). |
| `Crime_Rate_Per_1000` | `Total_Crime / Avg_Population_2021_2025 × 1000`. | float | Numerator BOCSAR incidents; denominator ERP-by-LGA table above — crude narrative rate only. |
| `Crimes_Per_Station` | `Total_Crime / Police_Station_Count`; zero stations → NaN in pipeline. | float | Numerator BOCSAR; denominator contextual station counts — not a performance metric. |
| LGA centroid lat/lon | Mean of station coordinates per LGA from `police_geo_df` for bubble/map positioning. | float | Derived approximation from facility layer — not ABS official centroids. |

---

## Credits

### Data

- **Recorded crime statistics (primary)** — NSW Bureau of Crime Statistics and Research (**BOCSAR**): [https://bocsar.nsw.gov.au/](https://bocsar.nsw.gov.au/). Incident downloads for this project were taken from BOCSAR **Open datasets**: [https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html) (e.g. monthly incidents by LGA, statewide daily incidents — exact workbook names match those published on that page).

- **Population denominators (ERP by LGA)** — Not BOCSAR outputs; NSW **Estimated Resident Population** / projection tables obtained from NSW open data and harmonised to BOCSAR **LGA** labels so rates use consistent geography with BOCSAR counts. Crime statistics authority remains [BOCSAR](https://bocsar.nsw.gov.au/).

- **Police facility locations & LGA boundary geometry** — NSW open spatial / GIS layers; processed (spatial join, name cleaning) to align with BOCSAR **LGA** naming for overlays and contextual charts only. Official incident statistics: [BOCSAR](https://bocsar.nsw.gov.au/).

### Software

Python · Streamlit · Pandas · NumPy · Plotly · GeoPandas.

### Team

| Name | MDSI role |
|------|-----------|
| Dhruv Sharma | Architect |
| Kanishk Duggal | Analyst |
| Shreyas Rajesh | Artist |
| Kunal Mistry | Analyst |
| Krishna Kumar | Analyst |
| Dharani Saravanan | Artist |
| Brian Shimmer | Orator |

**Dashboard build (Streamlit / visuals):** Krishna Kumar, Brian Shimmer, Dharani Saravanan.

---

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
