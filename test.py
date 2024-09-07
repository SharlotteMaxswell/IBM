import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown list for Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',  # Default value to 'ALL'
                 placeholder='Select a Launch Site',
                 searchable=True),
    
    html.Br(),
    
    # TASK 2: Pie chart for successful launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # TASK 3: Slider to select payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload, max=max_payload, step=1000,
                    marks={int(min_payload): f'{min_payload}', int(max_payload): f'{max_payload}'},
                    value=[min_payload, max_payload]),
    
    # TASK 4: Scatter chart to show correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Count success and failure for all sites
        success_counts = spacex_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        fig = px.pie(success_counts, values='count', 
                     names='class', 
                     title='Total Success Launches for All Sites')
    else:
        # Filter dataframe for the selected site
        filtered_site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count success and failure for the selected site
        success_counts = filtered_site_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        fig = px.pie(success_counts, values='count', 
                     names='class', 
                     title=f"Success vs Failure for {entered_site}")
    return fig

# TASK 4: Callback for Scatter Chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    # Filter dataset based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        # Scatter plot for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        # Filter by launch site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for {entered_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
