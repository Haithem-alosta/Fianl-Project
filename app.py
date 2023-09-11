import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash.dependencies as dd

app = dash.Dash(__name__)
server = app.server

# Load the data
data_url = "https://raw.githubusercontent.com/Haithem-alosta/Assignment3/main/best-selling%20game%20consoles.csv"
data = pd.read_csv(data_url)
data3 = data[['Console Name', 'Units sold (million)', 'Released Year']]
data3 = data3.sort_values('Released Year', ascending=False)

# Define your chart creation functions
def create_bar_chart():
    fig_bar = px.bar(data3, x='Console Name', y='Units sold (million)', title='Units Sold for Different Consoles')
    return fig_bar

def create_box_plot():
    fig_box = px.box(data3, x='Console Name', y='Released Year', title='Released Years for Different Consoles')
    return fig_box

def create_pie_chart():
    data3_sorted = data3.sort_values(by='Units sold (million)', ascending=False)
    top_5_consoles = data3_sorted.head(5)
    
    fig_pie = px.pie(top_5_consoles, values='Units sold (million)', names='Console Name', title='Top 5 Best-Selling Gaming Consoles')
    
    # Customize the pie chart to look like a donut
    fig_pie.update_traces(hole=0.4, pull=[0, 0.1, 0, 0, 0])  # Adjust the hole size and pull a slice
    
    return fig_pie

# Define the app layout with custom styles
app.layout = html.Div([
    html.H1("Haithem Final Project", style={'textAlign': 'center', 'color': 'white', 'background-color': 'rgb(0, 102, 204)', 'padding': '20px'}),
    
    dcc.Dropdown(
        id='console-selector',
        options=[
            {'label': console, 'value': console} for console in data['Console Name'].unique()
        ],
        value=data['Console Name'].iloc[0],  # Default selected console
        style={'width': '50%', 'margin': '20px auto', 'textAlign': 'center'}
    ),
    
    html.Div(id='console-details', style={'padding': '20px'}),
    
    dcc.Tabs([
        dcc.Tab(label='Bar & Box Plot', children=[
            dcc.Graph(id='bar-chart', figure=create_bar_chart()),
            dcc.Graph(id='box-plot', figure=create_box_plot())
        ]),
        dcc.Tab(label='Pie Chart', children=[
            dcc.Graph(id='pie-chart', figure=create_pie_chart()),
            html.Div([
                html.A(
                    html.Button('Download Data', style={'margin-top': '20px', 'font-size': '16px', 'background-color': 'blue'}),
                    id='download-link',
                    download="best-selling-game-consoles.csv",
                    href=data_url,
                    target="_blank"
                )
            ], style={'textAlign': 'center'})
        ])
    ])
], style={'padding': '20px', 'background-color': 'lightgray'})

# Define callback to display console details based on user input
@app.callback(
    Output('console-details', 'children'),
    [Input('console-selector', 'value')]
)
def display_console_details(selected_console):
    console_data = data[data['Console Name'] == selected_console]
    details = html.Div([
        html.H3(f"Details for {selected_console}", style={'textAlign': 'center'}),
        html.Table([
            html.Tr([html.Th("Released Year"), html.Td(console_data['Released Year'].iloc[0])]),
            html.Tr([html.Th("Units Sold (million)"), html.Td(console_data['Units sold (million)'].iloc[0])]),
        ], style={'margin': '0 auto'}),
    ], style={'padding': '20px'})
    
    return details

if __name__ == '__main__':
    app.run_server(debug=True)
