# 🌲 Wood-Site AI Agent

## Bachelor Thesis Research Prototype

**Thesis Title**

**Exploring the Potential of Artificial Intelligence for the Identification and Monitoring of Wood Storage Sites through Openly Available Satellite Imagery as a Tool for Market Potential Analysis: A Case Study of Finland and Sweden**

---

## 1. Project Overview

The **Wood-Site AI Agent** is a research prototype developed as part of a bachelor's thesis.

The project investigates how artificial intelligence and openly available geospatial imagery can support the **identification and monitoring of wood-storage and wood-processing sites**.

The prototype combines:

- geographic coordinates,
- geospatial imagery,
- Google Earth Engine,
- high-resolution orthophotos,
- OpenAI vision models,
- an AI-agent workflow,
- historical-image comparison,
- and an interactive Streamlit dashboard.

The purpose is to explore whether visible characteristics of wood-industry sites can provide useful **decision-support indicators for preliminary market-potential analysis**.

The system is not intended to directly predict sales, revenue, purchasing intention, production volume, or commercial demand.

---

## 2. Research Concept

The basic automated workflow is:

```text
User coordinates
      ↓
Google Earth Engine
      ↓
Available geospatial imagery
      ↓
High-resolution orthophoto
      ↓
OpenAI Vision Analysis
      ↓
Wood-site assessment
      ↓
Streamlit Dashboard
      ↓
Follow-up questions
For the historical-monitoring pilot:

Historical site images
      ↓
Individual AI image assessments
      ↓
Temporal comparison
      ↓
Visible changes over time
      ↓
Uncertainty assessment
3. Current Prototype Capabilities
Coordinate-Based Site Analysis

The user can enter a latitude and longitude in the dashboard.

The system then:

connects to Google Earth Engine,
searches for available high-resolution imagery,
automatically selects an available orthophoto,
retrieves the image into memory,
sends the image for AI-assisted visual analysis,
displays the assessment in the dashboard.

The image is processed in memory and is not permanently stored locally by the automated coordinate-analysis workflow.

AI-Based Visual Assessment

The vision model examines visible site characteristics such as:

log-storage areas,
timber or processed-wood stacks,
possible woodchip or sawdust piles,
open industrial yards,
industrial buildings,
material-handling areas,
road access,
rail infrastructure,
surrounding forest context,
and other visible features relevant to wood-storage or wood-processing activity.

The system also communicates uncertainty when the available visual evidence is insufficient.

Follow-Up Questions

After a site has been analysed, the user can ask questions such as:

Does this site have rail access?
Are there visible wood-storage areas?
What infrastructure is visible?

The follow-up system reuses the existing site assessment rather than retrieving and analysing the orthophoto again.

4. Historical Monitoring Pilot

A historical-monitoring workflow has been implemented for the pilot site FIN001.

Currently available reference years:

2021
2022
2025

The system compares visible changes relating to:

wood-storage extent,
use of open yard space,
material piles,
visible infrastructure,
apparent activity,
and other observable site-level characteristics.

Example question:

What changed over time at this site?

The system generates a temporal assessment while explicitly reporting uncertainty.

Important Limitation

Historical monitoring is currently implemented as a pilot for FIN001 using prepared historical reference images.

It is not yet an automated historical-imagery retrieval system for arbitrary coordinates.

5. Imagery and Data Sources
Finland

The automated high-resolution workflow currently uses the Finnish orthophoto collection available through Google Earth Engine:

Finland/SMK/V/50cm

The system checks which orthophoto years contain valid imagery around the requested coordinates and automatically selects the latest valid year.

Imagery availability can differ by geographic location.

Sentinel-2

The project also experimentally tested:

COPERNICUS/S2_SR_HARMONIZED

Sentinel-2 provides useful regional satellite coverage but its spatial resolution is substantially lower than the Finnish high-resolution orthophotos for detailed wood-site identification.

This comparison forms part of the methodological evaluation of imagery suitability.

Sweden

The intended Swedish workflow is based on high-resolution orthophoto data from Lantmäteriet, the Swedish mapping authority.

Integration of the Swedish imagery source is planned as an extension of the current prototype.

The intended architecture is:

Finland → Finnish orthophoto source
                     ↓
                 AI Agent
                     ↑
Sweden  → Swedish orthophoto source

The objective is to use the same AI-analysis framework while selecting an appropriate national imagery source for each country.

6. AI Agent

The project contains an AI agent capable of selecting different tools depending on the user's request.

Current agent functions include:

retrieving known site metadata,
identifying available historical images,
analysing historical site images,
analysing Finnish locations from coordinates,
and producing evidence-based responses.

The agent is instructed to distinguish between visible evidence and interpretation.

7. Decision-Support Perspective

The research investigates whether remotely observable characteristics can contribute to preliminary site screening.

Potential indicators include:

presence of significant wood-storage areas,
industrial-yard configuration,
material-handling infrastructure,
road accessibility,
rail connectivity,
visible processing-related infrastructure,
and changes in site utilization over time.

These indicators may support the prioritization of locations for further investigation.

They should not be interpreted as direct evidence of:

exact timber volume,
production output,
company sales,
revenue,
market demand,
purchasing intention,
or company performance.

Additional commercial and company-level information would be required for a complete market-potential assessment.

8. User Interface

The prototype includes an interactive dashboard developed with Streamlit.

Main dashboard functions include:

coordinate input,
location map,
automated location analysis,
imagery information,
AI site assessment,
historical monitoring for the pilot site,
and conversational follow-up questions.
9. Demo Workflow

A typical demonstration can be performed as follows:

Launch the Wood-Site AI dashboard.
Enter latitude and longitude.
Click Analyse Location.
Review the selected imagery information.
Review the AI Site Assessment.
For FIN001, click Compare Historical Changes.
Review the historical comparison.
Ask follow-up questions in the chat interface.

Example FIN001 coordinates:

Latitude: 60.868673
Longitude: 26.7346685
10. Project Structure
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
Important Components

agent.py
Defines the Wood-Site AI Agent and its available tools.

dashboard.py
Provides the Streamlit user interface.

earth_engine_tools.py
Handles Google Earth Engine initialization and imagery retrieval.

orthophoto_vision.py
Connects high-resolution Finnish orthophotos with AI vision analysis.

vision.py
Handles historical image analysis and comparison.

site_tools.py
Handles site metadata, local historical imagery, and analysis results.

launch_dashboard.bat
Provides a simple Windows launcher for the Streamlit dashboard.

11. Installation
Requirements
Python 3.11
Google Earth Engine account/access
OpenAI API access
Git
Internet connection

Clone the repository:

git clone https://github.com/Nayeemrin/wood-site-ai-agent.git
cd wood-site-ai-agent

Create a Python environment:

python -m venv .venv-agent

Install the dependencies:

pip install -r requirements-agent.txt
12. Environment Variables

Create a .env file in the root directory.

Example:

OPENAI_API_KEY=your_openai_api_key_here
Security

The .env file and API credentials must never be committed to GitHub.

The repository's .gitignore is used to prevent sensitive local files from being uploaded.

13. Google Earth Engine

The prototype requires an authenticated Google Earth Engine environment.

The current research project uses an Earth Engine project configuration for the thesis prototype.

Users running their own copy of the software may need to authenticate Earth Engine and configure their own Earth Engine project.

14. Running the Dashboard
Windows Launcher

The easiest method on Windows is to double-click:

launch_dashboard.bat

This starts the Streamlit server and opens the dashboard in the default browser.

Terminal Method

Alternatively:

python -m streamlit run src/dashboard.py

The local dashboard is normally available at:

http://localhost:8501
15. Current Research Status
Implemented
 Python project architecture
 Google Earth Engine integration
 Sentinel-2 experimental retrieval
 Finnish high-resolution orthophoto retrieval
 Automatic valid-orthophoto-year selection
 In-memory imagery processing
 OpenAI vision assessment
 Coordinate-based analysis
 AI-agent tool workflow
 Streamlit dashboard
 Follow-up conversational analysis
 FIN001 historical-monitoring pilot
 Historical change assessment
 Windows dashboard launcher
Planned / Future Extensions
 Swedish Lantmäteriet imagery integration
 Automated historical imagery retrieval for arbitrary coordinates
 Direct multi-image temporal comparison
 Larger-scale validation across Finnish and Swedish sites
 Additional decision-support indicators
 Broader evaluation of AI assessment accuracy
16. Research Limitations

The current prototype has several important limitations:

High-resolution orthophoto availability varies by location and year.
A single image represents conditions only at the time of capture.
Seasonal conditions can influence visible site characteristics.
AI interpretation can contain uncertainty.
Historical comparisons currently rely on prepared pilot imagery.
Differences between image descriptions may sometimes reflect model interpretation rather than actual physical change.
Visible site activity cannot directly establish commercial performance or market demand.
Swedish high-resolution imagery integration is not yet implemented in the prototype.

These limitations are treated as part of the research evaluation rather than hidden from the user.

17. Research Prototype Disclaimer

This repository contains an academic research prototype developed for a bachelor's thesis.

The results produced by the system should be interpreted as AI-assisted visual observations and decision-support information.

They are not intended to provide verified commercial intelligence, exact inventory measurements, company performance assessments, or investment recommendations.

Author
MD Rafiqul Islam Nayeem
Bachelor Thesis Project
International Business
OTH Amberg-Weiden
Germany

Project Status

Research prototype — under active thesis development, 2026