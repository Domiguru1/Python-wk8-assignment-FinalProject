import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


df = pd.read_csv('owid-covid-data.csv')

#Checking if I have the right columns
print(df.columns)

print(df.head())

# Define key columns
key_columns = ["date", "location", "total_cases", "total_deaths", "new_cases", "new_deaths", "total_vaccinations"]

# Check for missing columns
missing_cols = [col for col in key_columns if col not in df.columns]

if missing_cols:
    print(f"Warning: These columns are missing: {missing_cols}")
else:
    print("All key columns are present!")

# Filter for Kenya and making a copy
kenya_df = df[df["location"] == "Kenya"].copy()

# Drop rows with missing dates or critical values
critical_columns = ["date", "total_cases", "total_deaths", "new_cases", "new_deaths", "total_vaccinations"]
kenya_df.dropna(subset=critical_columns, inplace=True)

# Display cleaned data
print(kenya_df.head())


# Filter the DataFrame for the three East African countries
ea_countries = ['Kenya', 'Uganda', 'Tanzania']
df_ea = df[df['location'].isin(ea_countries)]

# Generate the statistical summary
summary = df_ea[['location', 'total_cases', 'total_deaths']].groupby('location').describe()

# Display the summary
print(summary)

# Define key columns to check for missing values
critical_columns = ["date", "total_cases", "total_deaths", "new_cases", "new_deaths", "total_vaccinations"]

# Drop rows with missing values in any of these columns
kenya_df.dropna(subset=critical_columns, inplace=True)

# Display cleaned dataset
print(kenya_df.head())

# Convert the 'date' column to datetime format
kenya_df["date"] = pd.to_datetime(kenya_df["date"])

# Display first few rows to confirm changes
print(kenya_df.head())
print(kenya_df.dtypes)  # Verify 'date' is now datetime
kenya_df.interpolate(method="linear", inplace=True)

# Filter for Kenya, Uganda, and Tanzania
import matplotlib.pyplot as plt

countries = ["Kenya", "Uganda", "Tanzania"]
df_filtered = df[df["location"].isin(countries)]

# Plot total cases over time
plt.figure(figsize=(12, 6))
for country in countries:
    country_df = df_filtered[df_filtered["location"] == country]
    plt.plot(country_df["date"], country_df["total_cases"], label=country)

# Customize the plot
plt.title("Total COVID-19 Cases Over Time (Kenya, Uganda, Tanzania)")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend(title="Country")
plt.grid(True)

# Show the plot
plt.show()

#plot total deaths over time
plt.figure(figsize = (12,6))
for country in countries:
    country_df = df_filtered[df_filtered['location'] == country]
    plt.plot(country_df["date"], country_df["total_deaths"], label=country)

# Customize the plot
plt.title("Total COVID-19 Deaths Over Time (Kenya, Uganda, Tanzania)")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.legend(title="Country")
plt.grid(True)

# Show the plot
plt.show()

# Daily Cases
plt.figure(figsize=(12, 6))
for country in countries:
    country_df = df_filtered[df_filtered["location"] == country]
    plt.plot(country_df["date"], country_df["new_cases"], label=country)

# Customize the plot
plt.title("Daily New COVID-19 Cases Comparison (Kenya, Uganda, Tanzania)")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.legend(title="Country")
plt.grid(True)

# Show the plot
plt.show()

#Analysing world wide and East Africa
countries = ["Kenya", "Uganda", "Tanzania"]
df_filtered = df[df["location"].isin(countries)].copy()  # This ensures df_filtered is defined

# Calculate death rate
df_filtered["death_rate"] = df_filtered["total_deaths"] / df_filtered["total_cases"]
print(df_filtered.pivot_table(index="date", columns="location", values="death_rate"))

# Get all unique location names
unique_locations = df["location"].unique()
print(unique_locations)  # Displays ALL entries

# Exclude non-country entities
regions_to_exclude = ["World", "European Union", "Asia", "Europe", "Africa", "North America", "South America",'High income','Upper middle income','Lower middle income']
df_filtered = df[~df["location"].isin(regions_to_exclude)]

# Get top 10 countries by total cases
top_countries = df_filtered.groupby("location")["total_cases"].max().nlargest(10)

# Plot bar chart
plt.figure(figsize=(12, 6))
top_countries.plot(kind="bar", color="red")

# Customize plot
plt.title("Top 10 Countries by Total COVID-19 Cases (Excluding Regions and Income rates)")
plt.xlabel("Country")
plt.ylabel("Total Cases")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Show plot
plt.show()

#Top 10 countries
# Filter for Kenya, Uganda, and Tanzania
countries = ["Kenya", "Uganda", "Tanzania"]
df_filtered = df[df["location"].isin(countries)].copy()

# Select latest available data
df_latest = df_filtered.sort_values("date").groupby("location").last()

# Extract total cases
total_cases = df_latest["total_cases"]
# Plot bar chart
plt.figure(figsize=(8, 6))
total_cases.plot(kind="bar", color=["red"])
# Customize plot
plt.title("Total COVID-19 Cases (Kenya, Uganda, Tanzania)")
plt.xlabel("Country")
plt.ylabel("Total Cases")
plt.xticks(rotation=0)
plt.grid(axis="y")

# Show plot
plt.show()

# Ensure 'date' column is in datetime format
df["date"] = pd.to_datetime(df["date"], errors="coerce")  

# Drop invalid dates
df = df.dropna(subset=["date"])

# Extract year-month for grouping
df["month"] = df["date"].dt.to_period("M")

# Filter for Kenya, Uganda, and Tanzania
countries = ["Kenya", "Uganda", "Tanzania"]
df_filtered = df[df["location"].isin(countries)].copy()
# Group by month and country, taking the max vaccinations per month
df_grouped = df_filtered.groupby(["month", "location"])["total_vaccinations"].max().reset_index()

# Convert period to string for easy plotting
df_grouped["month"] = df_grouped["month"].astype(str)

# Plot cumulative vaccinations over months
plt.figure(figsize=(12, 6))
for country in countries:
    country_df = df_grouped[df_grouped["location"] == country]
    plt.plot(country_df["month"], country_df["total_vaccinations"], marker="o", linestyle="-", label=country)

# Customize plot
plt.title("Cumulative COVID-19 Vaccinations Over Time (Monthly) - Kenya, Uganda, Tanzania")
plt.xlabel("Month")
plt.ylabel("Total Vaccinations")
plt.xticks(rotation=45)
plt.legend(title="Country")
plt.grid(True)

# Show plot
plt.show()

# Filter for Kenya, Uganda, and Tanzania
countries = ['Kenya', 'Uganda', 'Tanzania']
df_ea = df[df['location'].isin(countries)]

# Drop rows with missing vaccination or population data
df_ea = df_ea.dropna(subset=['people_vaccinated', 'population'])

# Get the latest data per country (assuming 'date' column is in datetime format)
df_ea['date'] = pd.to_datetime(df_ea['date'])
latest_vax = df_ea.sort_values('date').groupby('location').last()

# Compute vaccinated individuals per population (as a percentage)
latest_vax['vaccinated_per_population'] = (latest_vax['people_vaccinated'] / latest_vax['population']) * 100

# Select relevant columns for summary
result = latest_vax[['people_vaccinated', 'population', 'vaccinated_per_population']]
print(result)

# Filter for the three countries
countries = ['Kenya', 'Uganda', 'Tanzania']
df_ea = df[df['location'].isin(countries)].dropna(subset=['people_vaccinated', 'population'])

# Ensure date column is datetime
df_ea['date'] = pd.to_datetime(df_ea['date'])

# Get the latest data per country
latest = df_ea.sort_values('date').groupby('location').last()

# Setup subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # 1 row, 3 columns

colors = ['#2ecc71', '#e74c3c']  # Green for vaccinated, red for unvaccinated
for i, country in enumerate(countries):
    vaccinated = latest.loc[country, 'people_vaccinated']
    population = latest.loc[country, 'population']
    unvaccinated = population - vaccinated

    sizes = [vaccinated, unvaccinated]
    labels = ['Vaccinated', 'Unvaccinated']

    axes[i].pie(sizes, labels=labels, colors=colors, autopct='%.1f%%', startangle=140)
    axes[i].set_title(f'{country}')
    axes[i].axis('equal')  # Equal aspect ratio ensures pie is a circle

plt.suptitle('COVID-19 Vaccination Status in East Africa')
plt.tight_layout()
plt.show()

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# This entries are not countries
regions_to_exclude = [
    "World", "European Union", "Asia", "Europe", "Africa",
    "North America", "South America", "High income",
    "Upper middle income", "Lower middle income"
]

# Get latest data per location
latest_df = df.sort_values('date').groupby('location', as_index=False).last()
choropleth_data = latest_df[~latest_df['location'].isin(regions_to_exclude)]

# Keeping required columns and drop missing values
choropleth_data = choropleth_data[['iso_code', 'location', 'total_cases']].dropna(subset=['iso_code', 'total_cases'])


fig = px.choropleth(
    choropleth_data,
    locations="iso_code",
    color="total_cases",
    hover_name="location",
    color_continuous_scale="Reds",
    range_color=[0, choropleth_data['total_cases'].max()],
    title="Total COVID-19 Cases by Country"
)

fig.update_layout(
    coloraxis_colorbar=dict(
        title="Total Cases",
        ticks="outside"
    )
)
fig.show()

