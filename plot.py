import plotly.graph_objects as go

# Data
years = list(range(2020, 2031))
market_sizes = [221.4, 288.7, 376.6, 489.1, 635.8, 826.5, 1074.3, 1396.2, 1812.9, 2353.0, 3055.1]

# Create bar chart
fig = go.Figure(data=[go.Bar(
    x=years,
    y=market_sizes,
    marker=dict(color='blue'),
    hoverinfo='x+y',
    hovertemplate='%{x}: %{y}M'
)])

# Update layout
fig.update_layout(
    title='U.S. 5G Optical Transceiver Market Size (2020-2030)',
    xaxis_title='Year',
    yaxis_title='Market Size (USD Million)',
    hovermode='closest'
)

# Add hover effect
fig.update_traces(marker=dict(color='lightblue', line=dict(color='blue', width=1)),
                  hovertemplate='%{x}: %{y}M',
                  hoverinfo='text',
                  marker_line_color='darkblue',
                  selector=dict(type='bar'))

# Adding hover effect for changing color
fig.update_traces(
    marker=dict(color='blue'),
    selector=dict(type='bar'),
    hoverlabel=dict(bgcolor='lightblue')
)

fig.show()