import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

## Functions

def get_icon_size(funding_amount_str):
    
    try:
        # Convert the funding amount string to an integer
        funding_amount = int(funding_amount_str.replace(',', ''))
        
        # Determine the icon size based on the funding amount
        if funding_amount < 50000000:
            icon_size = 40
        elif 50000000 <= funding_amount < 100000000:
            icon_size = 50
        elif 100000000 <= funding_amount:
            icon_size = 60
        
        return icon_size
    
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        return 30  # Default size in case of an error
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return 30

def get_funding_color(funding_series, funding_amount_str):
    
    try:
        # Convert the funding amount string to an integer
        funding_amount = int(funding_amount_str.replace(',', ''))
        
        # Convert the series to integers
        funding_series_int = funding_series.dropna().str.replace(',', '').astype(int)

        print(funding_series_int)
        
        # Get the minimum and maximum values
        min_amount = funding_series_int.min()
        max_amount = funding_series_int.max()
        
        # Ensure the funding amount is within the range
        if funding_amount < min_amount or funding_amount > max_amount:
            raise ValueError(f"Funding amount {funding_amount} is out of range ({min_amount} to {max_amount})")
        
        # Normalize the data to the range [0, 1]
        norm = plt.Normalize(min_amount, max_amount)
        
        # Create a colormap
        # cmap = plt.get_cmap('jet')

        # Define a custom colormap that interpolates between black and red
        colors = [(0, "black"), (1, "red")]  # Define the colors at the min and max values
        cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)
        
        # Get the normalized value for the funding amount
        normalized_amount = norm(funding_amount)
        
        # Get the color from the colormap
        rgba_color = cmap(normalized_amount)
        
        # Convert RGBA color to hex format
        hex_color = mcolors.rgb2hex(rgba_color)
        
        return hex_color
    
    except (ValueError, KeyError) as e:
        print(e)
        return "#000000"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "#000000"

def round_to_100K(number_str):
    try:
        # Ensure the input is a string
        if not isinstance(number_str, str):
            return ""
        
        # Convert the string to an integer
        number = int(number_str.replace(',', ''))
        
        # Round to the nearest hundred thousand
        rounded_number = round(number / 100000) * 100000
        
        # Convert to millions and format as string
        rounded_millions = rounded_number / 1000000
        result_str = f"{rounded_millions:.1f}M"
        
        return result_str
    
    except:
        return ""

# Load the CSV file
startup_df = pd.read_csv('startups.csv')
round_df = pd.read_csv('rounds.csv')

funding_amount_df = round_df['Funding Amount']

companies = startup_df.to_dict('records')
funding_events = round_df.to_dict('records') 

print("TEST: ")
print(funding_amount_df)
print(get_funding_color(funding_amount_df, '10,000,000'))


# Data for companies
"""
companies = [
    {"name": "Company A", "start": 2013, "end": 2021},
    {"name": "Company B", "start": 2016, "end": 2024},
    {"name": "Company C", "start": 2015, "end": 2020},
]

funding_events = [
    {"year": 2016, "company": "Company B", "amount": "2M", "round": "Seed", "size": 30},
    {"year": 2017, "company": "Company B", "amount": "20M", "round": "Series A", "size": 40},
    {"year": 2018, "company": "Company B", "amount": "200M", "round": "Series B", "size": 50}
]
"""

# Prepare data for the plot
company_names = [company["Name"] for company in companies]
start_years = [int(company["Founding Year"]) for company in companies]
end_years = [2024 for company in companies]
durations = [end - start for start, end in zip(start_years, end_years)]


# Create the horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    y=company_names,
    x=durations,
    base=start_years,
    orientation='h',
    marker=dict(
        color='black'  # Set bar color to black
    ),
    showlegend=False
))

# Add round scatter dots at the start and end of each bar
for i, company in enumerate(companies):
    fig.add_trace(go.Scatter(
        x=[company["Founding Year"], 2024],
        y=[company["Name"], company["Name"]],
        mode='markers',
        marker=dict(
            symbol='circle',
            color='black',
            size=15
        ),
        showlegend=False,
        hoverinfo='skip'  # No hover info for these dots
    ))

# Add a scatter plot for the funding events

for event in funding_events:
    fig.add_trace(go.Scatter(
        x=[event["Year"]],
        y=[event["Name"]],
        mode='markers+text',
        marker=dict(
            symbol='circle',
            color=get_funding_color(funding_amount_df, event["Funding Amount"]),
            size=get_icon_size(event["Funding Amount"]),
        ),
        text=[round_to_100K(event["Funding Amount"])],
        textposition="middle center",
        textfont=dict(
            color='white'
        ),
        hoverinfo='text',
        hovertext=f"{event['Round']}",
        hoverlabel=dict(
            bgcolor='red',
            font_size=12,
            font_color='white',
            align='right'
        ),
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title="Company Duration from Founding to Exit",
    xaxis_title="Year",
    yaxis_title="Company",
    xaxis=dict(
        tickmode='linear',
        tick0=2013,
        dtick=1
    ),
    yaxis=dict(
        autorange='reversed'  # Reverse the y-axis to have the first company at the top
    ),
    plot_bgcolor='white',  # Set the background color to white
    paper_bgcolor='white',  # Set the paper background color to white
    bargap=0.9,  # Adjust the gap between bars to make them smaller
    height=150*len(companies),
)


fig.show()
