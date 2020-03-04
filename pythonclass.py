# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:43:41 2020

@author: bolom
"""

import dash 
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc # import the library
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import pandas as pd 

df = pd.read_csv('https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv')

df_vore = df['vore'].dropna().sort_values().unique()
opt_vore = [{'label': x + 'vore', 'value': x} for x in df_vore]



markdown_text = '''
#### Some references
[Dash Core Components](https://dash.plot.ly/dash-core-components)  
[Dash HTML Components](https://dash.plot.ly/dash-html-components)  
[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/l/components)  
'''

def generate_table(data, max_rows=5):
    return html.Table([
            html.Thead(
                    html.Tr(
                            [html.Th(i) for i in data.columns]
                            )
                    ),
            html.Tbody(
                    [html.Tr([
                            html.Td(col) for col in row.values
                            ]) for index, row in data.head(max_rows).iterrows()]
                    )
            ])

#external_stylesheets = [dbc.themes.BOOTSTRAP]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app =dash.Dash() #create blank app
app = dash.Dash(external_stylesheets=external_stylesheets)
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])  
app.title= "My app" 

color= {"font-color":"blue"}

app.layout = html.Div([
    html.H1("My Fifth Dash App", 
            style={"color": "orange"
                   }), #title <h1>
    dcc.Markdown(markdown_text),
    html.Div(id='my-div',
             style={
                     'background' : 'yellow',
                     'color' : 'blue'}),
    dcc.Graph(id='my-graph'
        ), 
    generate_table(df), 
    dash_table.DataTable(id="table",
            columns=[{"name": i, "id":i} for i in df.columns], 
            data=df.head(5).to_dict('records')), 
            html.Div([
                html.Label('Dropdown'),
                dcc.Dropdown(id='my-dropdown', 
                    options=opt_vore,
                    value=df_vore[0]
                ),

                html.Label('Multi-Select Dropdown'),
                dcc.Dropdown(id='my-multi-dropdown',
                    options=opt_vore,
                    value=df_vore[0:2],
                    multi=True
                ),

                html.Label('Radio Items'),
                dcc.RadioItems(
                    options=opt_vore,
                    value=df_vore[0]
                ),

                html.Label('Checkboxes'),
                dcc.Checklist(
                    options=opt_vore,
                    value=df_vore[0:2]
                ),

                html.Label('Text Input'),
                dcc.Input(value=df_vore[0], type='text'),

                html.Label('Slider'),
                dcc.Slider(
                    min=0,
                    max=9,
                    marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                    value=5,
                ),
            ], style={'columnCount': 2})
    ])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-dropdown', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

@app.callback(
    Output('my-graph', 'figure'),
    [Input('my-multi-dropdown', 'value')]
)
def update_output_graph(input_value):
    return  {
                'data': [
                    go.Scatter(
                        x=df[df['vore'] == i]['bodywt'] if i in input_value else [],
                        y=df[df['vore'] == i]['sleep_total'] if i in input_value else [],
                        text=df[df['vore'] == i]['name'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df_vore
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'Body weight (kg)'},
                    yaxis={'title': 'Total daily sleep time (hr)'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }


if __name__ == '__main__':
    app.run_server(debug=True)#run the app
    print("hello")
    