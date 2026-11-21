import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the CSV file
file_path = 'data.csv'
data = pd.read_csv(file_path)

# Set the number of items to display
top_n = 5


# Count unique tech tags, countries, and cities
unique_tech_tags = data['Tech Tags'].nunique()
unique_countries = data['Country'].nunique()
unique_cities = data['City'].nunique()

print(f"Unique tech tags: {unique_tech_tags}")
print(f"Unique countries: {unique_countries}")
print(f"Unique cities: {unique_cities}")

sns.set(style="white")

def set_integer_ticks(axis):
    max_value = int(axis.get_yticks()[-1])
    axis.set_yticks(np.arange(0, max_value + 1, 1)[::4])

# Number of startups per country
top_countries = data['Country'].value_counts().head(top_n)
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=top_countries.index, y=top_countries.values, palette="viridis")
plt.xlabel('')  # Suppress x-axis label
plt.ylabel('Number of Startups', fontsize=28, labelpad=15)  # Increase label padding
plt.xticks(rotation=45, fontsize=24)  # Increase tick font size
plt.yticks(fontsize=24)  # Increase tick font size
set_integer_ticks(ax)
plt.tight_layout()  # Adjust layout to fit everything nicely
plt.show()

# Number of startups per tech tag
tech_tags_expanded = data['Tech Tags'].str.split(',', expand=True).stack().str.strip()
top_tech_tags = tech_tags_expanded.value_counts().head(top_n)
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=top_tech_tags.index, y=top_tech_tags.values, palette="magma")
plt.xlabel('')  # Suppress x-axis label
plt.ylabel('Number of Startups', fontsize=28, labelpad=15)  # Increase label padding
plt.xticks(rotation=45, fontsize=24)  # Increase tick font size
plt.yticks(fontsize=24)  # Increase tick font size
set_integer_ticks(ax)
plt.tight_layout()  # Adjust layout to fit everything nicely
plt.show()

# Number of startups per initial letter
initial_letters = data['Name'].str[0].str.upper()
top_initial_letters = initial_letters.value_counts().head(top_n)
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=top_initial_letters.index, y=top_initial_letters.values, palette="cubehelix")
plt.xlabel('')  # Suppress x-axis label
plt.ylabel('Number of Startups', fontsize=28, labelpad=15)  # Increase label padding
plt.xticks(rotation=45, fontsize=24)  # Increase tick font size
plt.yticks(fontsize=24)  # Increase tick font size
set_integer_ticks(ax)
plt.tight_layout()  # Adjust layout to fit everything nicely
plt.show()