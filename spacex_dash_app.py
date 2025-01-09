# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Set min and max payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                # Dropdown to select Launch Site
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown', 
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, 
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                             ],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True),
                                # Pie chart to display launch success/failure
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # Payload range slider
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 10000: '10000'},
                                                value=[min_payload, max_payload]),
                                # Scatter chart to display payload vs launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2: Pie chart callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def get_pie_chart(entered_site):
    # Filter dataframe based on selected site
    filtered_df = spacex_df
    if entered_site != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
    # Create a pie chart showing success vs failure
    fig = px.pie(filtered_df, 
                 names='class',  # Success (1) vs Failure (0)
                 title=f"Success vs Failure Launches at {entered_site}" if entered_site != 'ALL' else "Success vs Failure for All Launch Sites",
                 color='class', 
                 color_discrete_map={0: 'red', 1: 'green'})
    
    return fig

# TASK 4: Scatter plot callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_scatter_plot(entered_site, payload_range):
    # Filter dataframe based on site and payload range
    filtered_df = spacex_df
    if entered_site != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
    # Filter by payload range
    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    # Create scatter plot showing payload vs launch success
    fig = px.scatter(filtered_df, 
                     x='Payload Mass (kg)', 
                     y='class',  # Success (1) vs Failure (0)
                     color='Booster Version Category', 
                     title=f"Payload vs Success for {entered_site}" if entered_site != 'ALL' else "Payload vs Success for All Launch Sites",
                     labels={'class': 'Launch Outcome'},
                     color_discrete_map={'FT': 'blue', 'Block 5': 'orange'})
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
