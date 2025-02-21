# Global CO₂ Emissions Dashboard

## Overview

The **Global CO₂ Emissions Dashboard** is an interactive web application developed using Streamlit. It provides users with comprehensive insights into global carbon dioxide emissions, enabling analysis of emission trends over time, country-specific data exploration, and future emission forecasting.

## Features

- 📊 **CO₂ Emissions Over Time**: Visualize historical CO₂ emission trends globally or for selected countries using interactive line charts.
- 🌍 **Country Comparison**: Compare CO₂ emissions between multiple countries within a specified timeframe to understand relative contributions.
- 🔮 **Forecasting**: Utilize linear regression models to predict CO₂ emission levels for the next decade based on historical data.
- 📑 **Data Exploration**: Access and explore raw datasets to perform custom analyses and gain deeper insights.

## Datasets

The application leverages the following datasets:

- **Global CO₂ Emissions Dataset**:  
  - Sourced from Kaggle, this dataset encompasses comprehensive data on CO₂ emissions from fossil fuel combustion and cement production across various countries.  
  - 📌 [Kaggle Dataset](https://www.kaggle.com/datasets/patricklford/global-co-emissions)  

- **Annual CO₂ Emissions per Country**:  
  - Obtained from Our World in Data, this dataset provides annual CO₂ emission figures for countries worldwide, facilitating temporal analysis and comparisons.  
  - 📌 [Our World in Data](https://ourworldindata.org/grapher/annual-co2-emissions-per-country)  

## Technologies Used

- 🖥 **Streamlit** - For developing the interactive web interface.
- 📊 **Pandas** - For efficient data manipulation and analysis.
- 📈 **Plotly Express** - For creating interactive data visualizations.
- 🤖 **Scikit-learn** - For building linear regression models to forecast future CO₂ emissions.
- 🔗 **Requests** - For downloading datasets dynamically.

## How to Use

1. **Set Up Environment**: Install the required Python libraries using pip:

   ```bash
   pip install streamlit pandas plotly scikit-learn requests

## Download Datasets: 
The application includes functions to download the necessary datasets directly from their sources. Ensure your environment has internet access.

## Run the Application: Execute the Streamlit app by running:
streamlit run main.py

## Interact with the Dashboard:

    Use the sidebar filters to select year ranges and countries.
    Explore different sections to visualize trends, compare emissions, and view forecasts.

## Key Functionalities

    Data Filtering:
        Users can filter data by year range and country using an interactive sidebar.

    CO₂ Emissions Over Time:
        Displays a line chart showing CO₂ emissions trends over selected years.

    CO₂ Emissions by Year:
        Presents a bar chart for emissions in the latest selected year.

    Forecasting CO₂ Emissions:
        Uses Linear Regression to predict emissions for the next 10 years.

    Country-Level Data:
        Shows unique CO₂ emissions data for different countries.

    Comparative Analysis:
        Enables users to compare emissions of multiple selected countries.

## Notes

    🛠 Caching Mechanism: The app uses Streamlit’s caching system to enhance performance.
    ⚠ First Run May Take Time: Since datasets are downloaded dynamically, the initial run may take a few extra seconds.
    🌡 Environmental Awareness: The app also provides insights into global warming impact and suggests solutions to reduce CO₂ emissions.

## Contributing

If you would like to contribute to improving this dashboard, feel free to fork the repository and submit a pull request.


