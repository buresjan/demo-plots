import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Define survey data
survey_data = {
    "Country": ["Total", "Australia", "Belgium", "Brazil", "Canada", "China", "France", "Germany"],
    "Total": [20122, 1001, 1004, 1008, 1006, 1006, 1009, 1005],
    "Strongly oppose": [12, 17, 11, 22, 13, 3, 7, 14],
    "Tend to oppose": [16, 19, 16, 18, 18, 11, 18, 14],
    "Strongly support": [21, 21, 23, 12, 17, 22, 18, 21],
    "Tend to support": [25, 20, 22, 15, 25, 39, 32, 21],
    "Neither support nor oppose": [21, 17, 23, 27, 18, 24, 21, 23],
    "Don't know": [5, 7, 5, 6, 9, 1, 4, 6],
    "Net: Oppose": [28, 36, 27, 40, 31, 15, 25, 29],
    "Net: Support": [46, 40, 44, 27, 42, 61, 50, 42]
}

# Create DataFrame
df = pd.DataFrame(survey_data)

# Define color mapping
negative_colors = ["#b0b0b0", "#d3d3d3"]  # Shades of grey for opposition
positive_colors = ["#ffd700", "#ffecb3"]  # Shades of gold for support

# Initialize figure
fig = go.Figure()

# Add traces for opposition (negative values for left side)
for i, col in enumerate(df.columns[2:4]):
    fig.add_trace(go.Bar(
        x=-df[col].values,
        y=df['Country'],
        orientation='h',
        name=col,
        marker_color=negative_colors[i],
        customdata=np.stack((df['Country'], df[col], np.full(len(df), col)), axis=-1),
        hovertemplate="%{customdata[2]}<br>%{customdata[0]}: %{customdata[1]}%"
    ))

# Add traces for support (positive values for right side)
for i, col in enumerate(df.columns[4:6]):
    fig.add_trace(go.Bar(
        x=df[col].values,
        y=df['Country'],
        orientation='h',
        name=col,
        marker_color=positive_colors[i],
        customdata=np.stack((df['Country'], df[col], np.full(len(df), col)), axis=-1),
        hovertemplate="%{customdata[2]}<br>%{customdata[0]}: %{customdata[1]}%"
    ))

# Update layout for the desired aesthetics
fig.update_layout(
    barmode='relative',
    height=500,
    width=800,
    yaxis_autorange='reversed',
    bargap=0.1,
    legend_orientation='h',
    legend_x=-0.05, legend_y=1.15,  # Position legend higher
    margin=dict(l=180, r=30, t=20, b=20),  # Add left margin for country names
    plot_bgcolor='white',  # Set background to white
)

# Customize axes and remove gridlines, ticks
fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
fig.update_yaxes(showgrid=False, tickfont=dict(size=12), tickangle=0)

# Calculate and display percentage sums on each side
for idx, row in df.iterrows():
    oppose_sum = row["Strongly oppose"] + row["Tend to oppose"]
    support_sum = row["Strongly support"] + row["Tend to support"]
    fig.add_annotation(
        x=-oppose_sum - 5,  # Position to the left
        y=row["Country"],
        text=f"{oppose_sum}%",
        showarrow=False,
        font=dict(color="black")
    )
    fig.add_annotation(
        x=support_sum + 5,  # Position to the right
        y=row["Country"],
        text=f"{support_sum}%",
        showarrow=False,
        font=dict(color="black")
    )

# fig.show()
fig.write_html("plot-legend.html")