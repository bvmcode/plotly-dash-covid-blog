import os
from datetime import datetime, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd

################### SET UP #########################
os.environ['TZ']= 'America/Chicago'

def get_data():
    '''
    Get data from the backend service
    '''
    df = pd.read_csv('./files/covid.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

def get_last_date():
    '''
    Get the max date from the dataset
    '''
    return data['date'].max()


app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG]) # create app with bootstrap themse
data = get_data() # pull in data
last_date = get_last_date() # set the max date

# colors to be used for the plot
colors = {
    "plot_background": "#111111",
    "plot_text": "#7FDBFF",
    "line":"#ff7f0e",
}

################### COMPONENTS ########################

# title of the dash
title = html.H3('NJ COVID-19 Dashboard', style={'color':'white'})

# dropdown menu
dropdown = html.Div([html.H5('Category'),
           dcc.Dropdown(
        id='covid-dropdown',
        options=[
            {'label': 'Confirmed', 'value': 'Confirmed'},
            {'label': 'Deaths', 'value': 'Deaths'},
            {'label': 'Recovered', 'value': 'Recovered'},
            {'label': 'Active', 'value': 'Active'},
        ],
        value='Active',
        style={'color':'black', 'backgroundColor':colors['line'], 'fontSize':'110%', 'width':'400px'}
    )])


# header using bootrap, contains title and the dropdown menue
header = dbc.Card([
    html.Div(id="header",children=
    [
        dbc.Row(
            [
                dbc.Col(title),
                dbc.Col(dropdown),
            ]
        )
    ]
)],body=True)

# info about where the data came from
info = html.Div(id='info', children=[
    html.H5(['Data from ', 
            html.A('John Hopkins University COVID-19 Repo', 
            href='https://github.com/CSSEGISandData/COVID-19')], 
            style={'textAlign':'Center', 'padding':'10px'})
])

# where the plot will land
plot = html.Div(id='plot')


################### UI LAYOUT ########################
# combine the components into our layout
app.layout = html.Div(children=[
    header,
    info,
    plot
])

################### CALLBACK ########################
@app.callback(
    dash.dependencies.Output('plot', 'children'),
    [dash.dependencies.Input('covid-dropdown', 'value')])
def update_output(value):
    '''
    callback function takes in a change in dropdown value and produces a corresponding plot 
    based on what's selected. It returns this plot to the placehold (id=plot) in the layout
    '''

    # global variables for data and last date as these could change based on the timing of new data
    # if last_date is 2 or more days ago and its after 3 am then bring in the updated data
    # then update last_date
    global data
    global last_date
    if last_date.date() < (datetime.now() + timedelta(days=-1)).date() and datetime.now().hour > 3:
        data = get_data()
        last_date = get_last_date()

    # our plot - The value input selects the corresponding column in the dataframe. The title is also dymanic
    fig = dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["date"],
                        "y": data[value],
                        "type": "line",
                        "line": {"color":colors['line']},
                    },
                ],
                "layout": {
                    "title": f'Total {value} by Day',
                    "plot_bgcolor": colors["plot_background"],
                    "paper_bgcolor": colors["plot_background"],
                    "font": {"color": colors["plot_text"]},
                    "yaxis": {"title": "Cases"},
                    "legend": {"orientation": "h", "y": -0.15},
                    "margin": {"t":-10}
                },
            },
        )
    return fig

################### RUN APP ########################
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')