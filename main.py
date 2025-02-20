import kagglehub
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
from sklearn.linear_model import LinearRegression

st.title("🌍 Global CO2 Emissions Dashboard")

# Download dataset
@st.cache_data
def load_data():
    try:
        # Download and locate CSV file dynamically
        path = kagglehub.dataset_download("patricklford/global-co-emissions")

        # Locate the CSV file
        csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]

        if not csv_files:
            raise FileNotFoundError("No CSV file found in dataset folder.")

        # Load the first CSV found
        csv_path = os.path.join(path, csv_files[0])

        # Read CSV with flexible delimiter and skip bad lines
        df = pd.read_csv(csv_path, sep=None, engine='python', on_bad_lines='skip')

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()

        return df

    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Load external country-level dataset
@st.cache_data
def load_country_data():
    try:
        # Check if CSV file exists, otherwise download it
        if not os.path.exists("annual-co2-emissions-per-country.csv"):
            url = "https://ourworldindata.org/grapher/annual-co2-emissions-per-country.csv"
            with open("annual-co2-emissions-per-country.csv", "wb") as f:
                f.write(requests.get(url).content)

        # Load the local CSV file
        country_df = pd.read_csv("annual-co2-emissions-per-country.csv")

        # Normalize column names
        country_df.columns = country_df.columns.str.strip().str.lower()

        return country_df

    except Exception as e:
        st.error(f"❌ Error loading country data: {e}")
        return pd.DataFrame()

country_df = load_country_data()

# Ensure data loaded successfully
if df.empty or country_df.empty:
    st.stop()

# Map potential column names
column_mapping = {
    "country": ["country", "nation"],
    "year": ["year", "date"],
    "co2": ["co2", "emissions", "co2_emissions"]
}

# Dynamically match columns
mapped_columns = {}
for key, options in column_mapping.items():
    for option in options:
        if option in df.columns:
            mapped_columns[key] = option
            break

# Validate required columns
if not all(col in mapped_columns for col in ["year", "co2"]):
    st.error("❌ Required columns ('year', 'co2') not found in dataset.")
    st.write("🔍 Available columns:", df.columns)
    st.stop()

# Ensure year column is numeric
df[mapped_columns["year"]] = pd.to_numeric(df[mapped_columns["year"]], errors='coerce')
df.dropna(subset=[mapped_columns["year"]], inplace=True)
df[mapped_columns["year"]] = df[mapped_columns["year"]].astype(int)

# Sidebar filters
st.sidebar.header("Filter Options")

year_column = df[mapped_columns["year"]]

# Ensure valid year range
year_range = st.sidebar.slider(
    "Select Year Range",
    int(year_column.min()),
    int(year_column.max()),
    (2000, 2020)
)

# Country filter (if country column exists)
selected_country = None
selected_countries = []
if "country" in mapped_columns:
    countries = df[mapped_columns["country"]].dropna().unique()
    countries.sort()

    # Single country selection
    selected_country = st.sidebar.selectbox("Select Country", options=countries, index=0)

    # Multiple countries for comparison
    selected_countries = st.sidebar.multiselect("Compare Countries", options=countries)

# Filter data
filtered_df = df[(df[mapped_columns["year"]] >= int(year_range[0])) & (df[mapped_columns["year"]] <= int(year_range[1]))]

if selected_country:
    filtered_df = filtered_df[filtered_df[mapped_columns["country"]] == selected_country]

# Line Chart: CO2 Emissions Over Time
st.subheader("📊 CO2 Emissions Over Time")
fig = px.line(filtered_df, x=mapped_columns["year"], y=mapped_columns["co2"],
              title=f"CO2 Emissions Over Time ({selected_country if selected_country else 'Global'})")
st.plotly_chart(fig)

# Bar Chart: CO2 Emissions by Year (Latest Year)
st.subheader("📊 CO2 Emissions (Latest Year Selected)")
if not filtered_df.empty:
    latest_year = year_column.max()
    latest_data = filtered_df[filtered_df[mapped_columns["year"]] == latest_year]
    fig_bar = px.bar(latest_data, x=mapped_columns["year"], y=mapped_columns["co2"],
                     title=f"CO2 Emissions in {latest_year}")
    st.plotly_chart(fig_bar)
    
     # Forecasting CO2 Emissions
def forecast_emissions(df, years=10):
    year_column = df[mapped_columns["year"]]
    co2_column = df[mapped_columns["co2"]]

    X = year_column.values.reshape(-1, 1)
    y = co2_column.values

    model = LinearRegression()
    model.fit(X, y)

    future_years = np.arange(year_column.max() + 1, year_column.max() + years + 1).reshape(-1, 1)
    future_predictions = model.predict(future_years)

    forecast_df = pd.DataFrame({
        mapped_columns["year"]: future_years.flatten(),
        "predicted_co2": future_predictions
    })
    return forecast_df

forecast_df = forecast_emissions(filtered_df)

st.subheader("🔮 CO2 Emissions Forecast")
fig_forecast = px.line(forecast_df, x=mapped_columns["year"], y="predicted_co2",
                       title="Forecasted CO2 Emissions for Next 10 Years")
st.plotly_chart(fig_forecast)


# Display Unique Country-level Data
st.subheader("🌎 Country-Level CO2 Emissions Data")
st.dataframe(country_df.drop_duplicates(subset='entity').head(10))

# Country Comparison Chart
if selected_countries:
    comparison_df = df[(df[mapped_columns["country"]].isin(selected_countries)) &
                       (df[mapped_columns["year"]] >= int(year_range[0])) & (df[mapped_columns["year"]] <= int(year_range[1]))]
    st.subheader("🌍 CO2 Emissions Comparison")
    fig_compare = px.line(comparison_df, x=mapped_columns["year"], y=mapped_columns["co2"],
                          color=mapped_columns["country"],
                          title="CO2 Emissions Comparison by Country")
    st.plotly_chart(fig_compare)
    
   

# Data Table
st.subheader("🗋 Raw Data")
st.dataframe(filtered_df)

# Information on CO2 impact
st.sidebar.header("🌡️ Global Warming Impact")
st.sidebar.info("CO₂ emissions trap heat in the atmosphere, causing global temperatures to rise. This leads to severe weather, rising sea levels, and biodiversity loss.")

# Solutions to reduce CO2
st.sidebar.header("💡 How to Reduce CO₂ Emissions")
st.sidebar.write("- Use renewable energy sources\n- Promote energy efficiency\n- Support carbon capture technologies\n- Encourage sustainable transportation\n- Plant trees and protect forests")

st.success("✅ Dashboard Loaded Successfully!")
