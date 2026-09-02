# 🌲 Wood-Site AI Agent

## Bachelor Thesis Research Prototype

### Thesis Title

**Exploring the Potential of Artificial Intelligence for the Identification and Monitoring of Wood Storage Sites through Openly Available Satellite Imagery as a Tool for Market Potential Analysis: A Case Study of Finland and Sweden**

---

## 1. Project Overview

The **Wood-Site AI Agent** is a research prototype developed as part of a bachelor's thesis.

The project investigates how artificial intelligence and openly available geospatial imagery can support the **identification and monitoring of wood-storage and wood-processing sites**.

The prototype combines:

- Geographic coordinates
- Geospatial imagery
- Google Earth Engine
- High-resolution orthophotos
- OpenAI vision models
- AI-agent workflows
- Historical-image comparison
- An interactive Streamlit dashboard

The purpose is to explore whether visible characteristics of wood-industry sites can provide useful **decision-support indicators for preliminary market-potential analysis**.

The system is not intended to directly predict sales, revenue, purchasing intention, production volume, or commercial demand.

---

## 2. Research Concept

### Automated Coordinate-Based Workflow

```text
User Coordinates
        ↓
Google Earth Engine
        ↓
Available Geospatial Imagery
        ↓
High-Resolution Orthophoto
        ↓
OpenAI Vision Analysis
        ↓
Wood-Site Assessment
        ↓
Streamlit Dashboard
        ↓
Follow-Up Questions
```

### Historical-Monitoring Pilot

```text
Historical Site Images
        ↓
Individual AI Image Assessments
        ↓
Temporal Comparison
        ↓
Visible Changes Over Time
        ↓
Uncertainty Assessment
```

---

## 3. Current Prototype Capabilities

### Coordinate-Based Site Analysis

The user can enter a latitude and longitude in the dashboard.

The system then:

1. Connects to Google Earth Engine.
2. Searches for available high-resolution imagery.
3. Identifies valid orthophoto coverage for the location.
4. Automatically selects the latest valid orthophoto year.
5. Retrieves the image into memory.
6. Sends the image for AI-assisted visual analysis.
7. Displays the assessment in the dashboard.

The image is processed in memory and is not permanently stored locally by the automated coordinate-analysis workflow.

### AI-Based Visual Assessment

The vision model examines visible site characteristics such as:

- Log-storage areas
- Timber or processed-wood stacks
- Possible woodchip or sawdust piles
- Open industrial yards
- Industrial buildings
- Material-handling areas
- Road access
- Rail infrastructure
- Surrounding forest context
- Other visible characteristics relevant to wood-storage or wood-processing activity

The system communicates uncertainty when the available visual evidence is insufficient.

### Follow-Up Questions

After a site has been analysed, the user can ask questions such as:

```text
Does this site have rail access?
```

```text
Are there visible wood-storage areas?
```

```text
What infrastructure is visible?
```

The follow-up system reuses the existing site assessment rather than retrieving and analysing the orthophoto again.

---

## 4. Historical Monitoring Pilot

A historical-monitoring workflow has been implemented for the pilot site **FIN001**.

Currently available reference years are:

- 2021
- 2022
- 2025

The system compares visible changes relating to:

- Wood-storage extent
- Use of open yard space
- Material piles
- Visible infrastructure
- Apparent activity
- Other observable site-level characteristics

Example question:

```text
What changed over time at this site?
```

The system produces a temporal assessment while explicitly reporting uncertainty.

### Important Limitation

Historical monitoring is currently implemented as a **pilot for FIN001 using prepared historical reference images**.

It is not yet an automated historical-imagery retrieval system for arbitrary coordinates.

---

## 5. Imagery and Data Sources

### Finland

The automated high-resolution workflow currently uses the Finnish orthophoto collection available through Google Earth Engine:

```text
Finland/SMK/V/50cm
```

The system checks which orthophoto years contain valid imagery around the requested coordinates and automatically selects the latest valid year.

Imagery availability varies by geographic location.

### Sentinel-2

The project also experimentally tested:

```text
COPERNICUS/S2_SR_HARMONIZED
```

Sentinel-2 provides useful regional satellite coverage, but its spatial resolution is substantially lower than the Finnish high-resolution orthophotos for detailed wood-site identification.

This comparison forms part of the methodological evaluation of imagery suitability.

### Sweden

The intended Swedish workflow is based on high-resolution orthophoto data from **Lantmäteriet**, the Swedish mapping authority.

Integration of the Swedish imagery source is planned as an extension of the current prototype.

The intended architecture is:

```text
Finland → Finnish Orthophoto Source
                     ↓
                  AI Agent
                     ↑
Sweden  → Swedish Orthophoto Source
```

The objective is to use the same AI-analysis framework while selecting an appropriate national imagery source for each country.

---

## 6. AI Agent

The project contains an AI agent capable of selecting different tools according to the user's request.

Current agent functions include:

- Retrieving known site metadata
- Identifying available historical images
- Analysing historical site images
- Analysing Finnish locations from coordinates
- Producing evidence-based responses

The agent is instructed to distinguish between **visible evidence**, **interpretation**, and **uncertainty**.

The agent is also instructed not to infer unsupported commercial information such as:

- Exact timber volume
- Production levels
- Sales
- Revenue
- Market demand
- Purchasing intention
- Company performance

---

## 7. Decision-Support Perspective

The research investigates whether remotely observable site characteristics can contribute to preliminary site screening and prioritization.

Potential indicators include:

- Presence of significant wood-storage areas
- Industrial-yard configuration
- Material-handling infrastructure
- Road accessibility
- Rail connectivity
- Visible processing-related infrastructure
- Changes in site utilization over time

These indicators may support the **prioritization of locations for further investigation**.

They should not be interpreted as direct evidence of:

- Exact timber volume
- Production output
- Company sales
- Revenue
- Market demand
- Purchasing intention
- Company performance

Additional commercial, operational, and company-level information would be required for a complete market-potential assessment.

---

## 8. User Interface

The prototype includes an interactive dashboard developed with **Streamlit**.

Main dashboard functions include:

- Coordinate input
- Location map
- Automated location analysis
- Imagery information
- AI site assessment
- Historical monitoring for the pilot site
- Conversational follow-up questions

---

## 9. Demo Workflow

A typical demonstration can be performed as follows:

1. Launch the Wood-Site AI dashboard.
2. Enter latitude and longitude.
3. Click **Analyse Location**.
4. Review the selected imagery information.
5. Review the **AI Site Assessment**.
6. For FIN001, click **Compare Historical Changes**.
7. Review the historical comparison.
8. Ask follow-up questions in the chat interface.

Example FIN001 coordinates:

```text
Latitude: 60.868673
Longitude: 26.7346685
```

---

## 10. Project Structure

```text
wood-site-ai-agent/
│
├── data/
│   ├── screenshots/
│   ├── results/
│   └── site_metadata.csv
│
├── src/
│   ├── agent.py
│   ├── dashboard.py
│   ├── earth_engine_tools.py
│   ├── orthophoto_vision.py
│   ├── vision.py
│   └── site_tools.py
│
├── launch_dashboard.bat
├── requirements-agent.txt
├── .gitignore
└── README.md
```

### Important Components

**`agent.py`**  
Defines the Wood-Site AI Agent and its available tools.

**`dashboard.py`**  
Provides the Streamlit user interface.

**`earth_engine_tools.py`**  
Handles Google Earth Engine initialization, satellite imagery retrieval, orthophoto coverage checks, and automatic valid-year selection.

**`orthophoto_vision.py`**  
Connects high-resolution Finnish orthophotos with AI vision analysis.

**`vision.py`**  
Handles historical image analysis and temporal comparison.

**`site_tools.py`**  
Handles site metadata, local historical imagery, and saved analysis results.

**`launch_dashboard.bat`**  
Provides a simple Windows launcher for the Streamlit dashboard.

---

## 11. Installation

### Requirements

- Python 3.11
- Google Earth Engine access
- OpenAI API access
- Git
- Internet connection

Clone the repository:

```bash
git clone https://github.com/Nayeemrin/wood-site-ai-agent.git
cd wood-site-ai-agent
```

Create a Python virtual environment:

```bash
python -m venv .venv-agent
```

Activate it on Windows PowerShell:

```powershell
.\.venv-agent\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements-agent.txt
```

---

## 12. Environment Variables

Create a `.env` file in the project root directory.

Example:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

### Security

The `.env` file and API credentials must **never be committed to GitHub**.

The repository's `.gitignore` is used to prevent sensitive local files from being uploaded.

---

## 13. Google Earth Engine

The prototype requires an authenticated Google Earth Engine environment.

The current thesis implementation uses the Earth Engine project:

```text
wood-site-thesis
```

Users running their own copy of the software may need to authenticate Earth Engine and configure their own Google Cloud / Earth Engine project.

---

## 14. Running the Dashboard

### Windows Launcher

The easiest method on Windows is to double-click:

```text
launch_dashboard.bat
```

The launcher starts the Streamlit server and opens the dashboard in the default browser.

### Terminal Method

Alternatively, from the project root:

```powershell
& ".\.venv-agent\Scripts\python.exe" -m streamlit run ".\src\dashboard.py"
```

The local dashboard is normally available at:

```text
http://localhost:8501
```

---

## 15. Current Research Status

### Implemented

- [x] Python project architecture
- [x] Google Earth Engine integration
- [x] Sentinel-2 experimental retrieval
- [x] Finnish high-resolution orthophoto retrieval
- [x] Automatic valid-orthophoto-year selection
- [x] In-memory imagery processing
- [x] OpenAI vision assessment
- [x] Coordinate-based location analysis
- [x] AI-agent tool workflow
- [x] Streamlit dashboard
- [x] Follow-up conversational analysis
- [x] FIN001 historical-monitoring pilot
- [x] Historical change assessment
- [x] Windows dashboard launcher

### Planned / Future Extensions

- [ ] Swedish Lantmäteriet imagery integration
- [ ] Automated historical imagery retrieval for arbitrary coordinates
- [ ] Direct multi-image temporal comparison
- [ ] Larger-scale validation across Finnish and Swedish sites
- [ ] Additional decision-support indicators
- [ ] Broader evaluation of AI assessment accuracy

---

## 16. Research Limitations

The current prototype has several important limitations:

1. High-resolution orthophoto availability varies by location and year.
2. A single image represents conditions only at the time of capture.
3. Seasonal and temporal conditions can influence visible site characteristics.
4. AI interpretation can contain uncertainty.
5. Historical comparisons currently rely on prepared pilot imagery for FIN001.
6. Historical comparison currently uses individual image assessments before temporal comparison.
7. Differences between descriptions may sometimes reflect model interpretation rather than actual physical change.
8. Visible site activity cannot directly establish commercial performance or market demand.
9. Swedish high-resolution imagery integration is not yet implemented in the current prototype.

These limitations are treated as part of the research evaluation rather than being hidden from the user.

---

## 17. Research Prototype Disclaimer

This repository contains an **academic research prototype** developed for a bachelor's thesis.

Results produced by the system should be interpreted as **AI-assisted visual observations and decision-support information**.

They are not intended to provide:

- Verified commercial intelligence
- Exact inventory measurements
- Exact production measurements
- Company performance assessments
- Market-demand predictions
- Investment recommendations

---

## Author

**Md Rafiqul Islam Nayeem**  
Bachelor Thesis Project  
International Business  
OTH Amberg-Weiden  
Germany

---

## Project Status

**Research prototype — under active thesis development, 2026**