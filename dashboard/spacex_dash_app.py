# Import required libraries
import pandas as pd
import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px

# Read the airline data into pandas dataframe
try:
    spacex_df = pd.read_csv("../data/spacex_launch_dash.csv")
except:
    spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
    spacex_df.to_csv("../data/spacex_launch_dash.csv", index = False)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
    'SpaceX Launch Records Dashboard',
    style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
    ),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id = 'site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            ],
        value = 'ALL',
        placeholder = 'Select a Launch Site here',
        searchable = True
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks = {i:str(i) for i in range(0,10000, 1000)},
        value=[min_payload, max_payload]
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(data, values='class',
        names='Launch Site',
        title='Successful Launches for all sites')
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(data, values='Flight Number',
        names='class',
        title= f'Successful Launches for {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")]
)

def get_scatterchart(entered_site, entered_payload):
    min, max = entered_payload
    data = spacex_df[spacex_df['Payload Mass (kg)'].between(min, max)]
    if entered_site == 'ALL':
        fig = px.scatter(data, x='Payload Mass (kg)',
        y='class',
        color = 'Booster Version',
        title='Payload vs Launch Success for all')
    else:
        data = data[data['Launch Site'] == entered_site]
        fig = px.scatter(data, x='Payload Mass (kg)',
        y='class',
        color = 'Booster Version',
        title= f'Successful Launches for {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
