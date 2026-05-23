# NSW Crime Intelligence Dashboard

**Group 24**

**In-app title (hero header):** **NSW Crime Intelligence.** The same build deploys publicly on **Streamlit Community Cloud** from this repository.

## Project Overview

**NSW Crime Intelligence** uses Streamlit as an exploratory interface over cleaned NSW crime aggregates. Inputs include monthly LGA offences (BOCSAR class), statewide daily extracts where applied, ERP-style population denominators joined for crude rates per 1,000 residents, police station inventories for density narratives, and LGA geometries for choropleths. The design targets a coursework portfolio centred on storytelling rather than KPI-only dashboards; key affordances span:


- how crime shifts over time across NSW  
- dominant offence categories and LGA hotspots  
- crude rates against population plus police-station density as narrative context  

## Requirements

**Runtime**

| Item | Requirement |
|------|-------------|
| Python | **3.10 +** recommended (aligned with Streamlit wheels on Cloud) |
| Packages | Versions pinned in **`requirements.txt`** (`streamlit`, `pandas`, `plotly`, `numpy`, `geopandas`) |
| Data layout | Repo root **`app.py`**, **`final_csvs/`** CSVs, **`nsw_lga.geojson`**, **`/.streamlit/config.toml`** as below |
| Local run | `pip install -r requirements.txt` then `python -m streamlit run "app.py"` |

**Portfolio / polish (technical delivery)**

| Item | How this repo satisfies it |
|------|-----------------------------|
| Public dashboard | Hosted on **Streamlit Community Cloud** from this GitHub repository |
| Design system | **`.streamlit/config.toml`** (Streamlit theme: colours, typography) |
| Data dictionary | **Below** — every field: definition · type · provenance |
| Credits | **Below** — data sources · software · team · dashboard authors |
| Annotated Streamlit code | **`app.py`** includes module notes, `@st.cache_data` loader docs, helpers, Act sections |

## Features

- KPI narrative cards and storyline copy  
- LGA choropleth + supplementary map visualisations  
- Time patterns (annual, seasonal-style views)  
- Offence-category breakdown and LGA deep dive  
- Population- and policing-context metrics  

## Dataset Files

`final_csvs/`:

- `nsw_lga_crime_tableau_clean.csv`
- `nsw_daily_crime_grouped_clean.csv`
- `nsw_lga_avg_population_2021_2025_clean.csv`
- `nsw_police_station_count_by_lga_clean.csv`
- `nsw_police_stations_with_lga_clean.csv`

Repository root boundary file:

- `nsw_lga.geojson`

---

## Data dictionary

Tabular dictionary: **variable**, **definition**, **data type**, **provenance** for each input file and derived metrics used by `app.py`.

**Recorded crime portal:** NSW Bureau of Crime Statistics and Research — BOCSAR [https://bocsar.nsw.gov.au/](https://bocsar.nsw.gov.au/) · Open datasets [https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html)

### `final_csvs/nsw_lga_crime_tableau_clean.csv`

_Source type: monthly recorded incidents by LGA (same information class as `RCI_offencebymonth.xlsm`)._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `LGA` | NSW Local Government Area name (aligned across merges). | string | BOCSAR open data · cleaned to long format · [portal](https://bocsar.nsw.gov.au/) · [datasets](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html) |
| `Offence category` | Broad offence grouping after project-side aggregation from subcategories. | string | BOCSAR taxonomy |
| `Month` | First calendar day of observation month. | datetime (parsed on load) | BOCSAR workbook month columns |
| `Incident_Count` | Count of incidents for LGA × offence × month. | float / int | BOCSAR counts |
| `Month_Label` | Display label (`Jan-21`). | string | Derived in cleaning |
| `Year` | Calendar year from `Month`. | integer | Derived |
| `Month_Num` | Month index 1–12. | integer | Derived |

### `final_csvs/nsw_daily_crime_grouped_clean.csv`

_Source type: statewide daily incident workbook (`NSW_criminal_incidents_daily.xlsx` class)._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `Date` | Calendar date for statewide daily tally. | datetime (parsed on load) | BOCSAR daily extract · grouped to broad offences in cleaning · [datasets](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html) |
| `Offence category` | Broad category aligned with LGA monthly file. | string | Mapped from BOCSAR detail labels |
| `Incident_Count` | Incidents per date per category (NSW-wide). | float | BOCSAR |
| `Year` | From `Date`. | integer | Derived |
| `Month_Num` | 1–12. | integer | Derived |
| `Month_Label` | Month short label. | string | Derived |

Loaded in code for pipeline completeness; dominant narrative path uses **`crime_df`** monthly LGA rows.

### `final_csvs/nsw_lga_avg_population_2021_2025_clean.csv`

_Denominator only — ERP-style counts are **not** from BOCSAR._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `LGA` | LGA keyed to crime tables after name harmonisation. | string | NSW open demographic / ERP-style projection table by LGA · joined to BOCSAR `LGA` list |
| `ERP_2021` … `ERP_2025` | Annual ERP projection values. | float | Same ERP pipeline |
| `Avg_Population_2021_2025` | Mean ERP 2021–2025 rounded. | integer | Project derived |
| `Population_2025` | ERP reference column for merges. | integer | ERP source |

### `final_csvs/nsw_police_station_count_by_lga_clean.csv`

_Context layer — incidents remain BOCSAR._

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `LGA` | LGA attributed after spatial joins. | string | Station points ∩ boundary polygons aligned to crime `LGA` |
| `Police_Station_Count` | Stations per LGA after cleaning duplicates. | integer | NSW GIS facility layer ∩ boundaries |

### `final_csvs/nsw_police_stations_with_lga_clean.csv`

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `Station_Name` | Label from GIS layer. | string | NSW open policing / spatial facility inventory |
| `Longitude`, `Latitude` | WGS84 for markers. | float | Same GIS layer |
| `LGA` | Spatial join result; blank if unmatched. | string | Derived · invalid coords stripped in plotting |

### `nsw_lga.geojson` (repository root)

| Element | Definition | Type | Provenance |
|---------|------------|------|------------|
| geometry | Polygon for each NSW LGA. | GeoJSON | NSW administrative LGA polygons · simplified footprint for repo size |
| `properties.LGA` | Join key ↔ CSV `LGA` after whitespace strip in **`app.py`**. | string | Boundary attribution |

### Derived fields (within `compute_lga_summary()` and charts)

| Variable | Definition | Type | Provenance |
|----------|------------|------|------------|
| `Total_Crime` | Sum `Incident_Count` per LGA in filter scope. | float | Aggregation of BOCSAR `crime_df` |
| `Crime_Rate_Per_1000` | `Total_Crime ÷ Avg_Population_2021_2025 × 1000`. | float | BOCSAR numerator · ERP denominator |
| `Crimes_Per_Station` | `Total_Crime ÷ Police_Station_Count` (no station → NaN handled). | float | BOCSAR numerator · GIS denominator |
| LGA centroid mean lat/lon | Mean station coordinates per LGA for bubble overlays. | float | Facility CSV · exploratory geometry only |

---

## Credits

### Data

- **Recorded crime** — NSW BOCSAR: [website](https://bocsar.nsw.gov.au/) · [Open datasets](https://bocsar.nsw.gov.au/statistics-dashboards/open-datasets.html)  
- **ERP population denominators** — NSW open-government demographic / ERP extract · LGA keyed to BOCSAR labels  
- **Police facilities · LGA boundaries** — NSW open spatial GIS resources · joins harmonised with BOCSAR `LGA`  

### Software

Python · Streamlit · Pandas · NumPy · Plotly · GeoPandas.

### Team (MDSI roles)

| Name | Role |
|------|------|
| Dhruv Sharma | Architect |
| Kanishk Duggal | Analyst |
| Shreyas Rajesh | Artist |
| Kunal Mistry | Analyst |
| Krishna Kumar | Analyst |
| Dharani Saravanan | Artist |
| Brian Shimmer | Orator |

**Dashboard implementation (Streamlit / Plotly visuals):** Krishna Kumar, Brian Shimmer, Dharani Saravanan.

---

## Tech Stack

Python · Streamlit · Pandas · Plotly · GeoPandas · NumPy  

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
    `-- config.toml
```

## How to run locally

1. **Open a terminal** (Windows: **PowerShell** or **Command Prompt**; Mac/Linux: **Terminal**). You can also use the **integrated terminal** in VS Code / Cursor (**Terminal → New Terminal**).
2. **Go to the project folder** — the directory that contains `app.py` and `requirements.txt` (clone or download this repo first, then `cd` into that folder).
3. **Install dependencies** (once per machine or after updating `requirements.txt`):

```bash
pip install -r requirements.txt
```

4. **Start the app:**

```bash
python -m streamlit run "app.py"
```

5. When the terminal shows a local URL, **open it in your browser** (usually **http://localhost:8501**). Keep the terminal **open** while you use the dashboard; press **Ctrl+C** there to stop the server.

## Design system

Streamlit theme and widget chrome are governed by **`/.streamlit/config.toml`** (palette, typography, backgrounds). Loaded automatically for local sessions and Streamlit Cloud builds.

## Public dashboard (NSW Crime Intelligence)

**Live deployment (Streamlit Community Cloud):** [https://nsw-crime-dashboard-ykmus7g8t7ptej4ejeunwt.streamlit.app](https://nsw-crime-dashboard-ykmus7g8t7ptej4ejeunwt.streamlit.app)

**Walkthrough video (Google Drive folder):** [https://drive.google.com/drive/folders/1Ul5EcDoY-y82Z3DgInSc8dwP1Z6IGwZK?usp=sharing](https://drive.google.com/drive/folders/1Ul5EcDoY-y82Z3DgInSc8dwP1Z6IGwZK?usp=sharing)

**Source repository:** [https://github.com/krishnakumar-devx/nsw-crime-dashboard](https://github.com/krishnakumar-devx/nsw-crime-dashboard)

## Authors

Dhruv Sharma · Kanishk Duggal · Shreyas Rajesh · Kunal Mistry · Krishna Kumar · Dharani Saravanan · Brian Shimmer  

Coursework submission — **Group 24** — Data Visualisation (Data Narrative Studio) · NSW Crime Trends & Community Safety.
