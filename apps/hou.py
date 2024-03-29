import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import datetime
import numpy as np
from dash.dependencies import Input, Output
from apps import common
from app import app
import dash_table
import base64
import dash_bootstrap_components as dbc


df = pd.read_csv('data/hou.csv', dtype={'b_count': 'category', 's_count' : 'category', 'pitcher_id' : 'category', 'pitch_type' : 'category', 'stand': 'category' })

teamColor = [[0, "#fff"],
                [0.25, "#fbe2d2"],
                [0.45, "#f7c5a5"],
                [0.65, "#f3a878"],
                [0.85, "#ef8b4b"],
                [1, "#eb6e1f"]]

darker = '#002d62'
lighter = '#eb6e1f'
bright = '#f4911e'

features = df.pitcher_id.unique()
pitches = df.pitch_type.unique()
opts = [{'label' : i, 'value' : i} for i in features]
tops = [{'label' : j, 'value' : j} for j in pitches]
balls6 = [{'label' : '0', 'value' : '0.0'},             #increase num
         {'label' : '1', 'value' : '1.0'},
         {'label' : '2', 'value' : '2.0'},
         {'label' : '3', 'value' : '3.0'}]

strike6 = [{'label' : '0', 'value' : '0.0'},            #increase num
         {'label' : '1', 'value' : '1.0'},
         {'label' : '2', 'value' : '2.0'}]

batter6 = [{'label' : 'Right', 'value' : 'R'},          #increase num
         {'label' : 'Left', 'value' : 'L'}]

trace_1 = go.Histogram2d()

layouts = go.Layout(height = 600,
                   width = 600)
fig5 = go.Figure(data = [trace_1], layout = layouts)    #increase num
value = opts[0]['value']
def counts(s,b,hand,pitcher):
    pitches = df.query('pitcher_id == @pitcher').pitch_type.unique()
    j= 0
    i= 0
    bc = ['0','1','2','3']
    sc = ['0','1','2']
    final = pd.DataFrame(data = pitches, columns = ['Pitch Type'])
    for st in s:
        
        j = 0
        for ba in b:
            res = []
            total = df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and stand == @hand').shape[0]
            for value in pitches:
                res.append(df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and pitch_type == @value and stand == @hand').shape[0]
                       /total)
            colname = (bc[j] + '-'+ sc[i])
            #df1 = pd.DataFrame(data = res, columns = [colname])  
            final[colname] = res
            final[colname] = final[colname].multiply(100)
            final[colname] = final[colname].round(3)
            j += 1
        i += 1
    
    
    return final
b = ['0.0','1.0','2.0','3.0']
s = ['0.0','1.0','2.0']
fin = counts(s,b,'L',  opts[0]['value'] )
finR = counts(s,b,'R', opts[0]['value'])
#image_filename = 'oriole.jpg' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div([
                #common.get_header(),
                common.get_menu(),
                html.Div([
                    html.Div([
                        #html.Img(src='data:oriole/jpg;base64,{}'.format(encoded_image.decode()),style ={'width': '99%'}),
                        html.H1("Houston Astros Match Up Chart - Pitcher Tendencies",
                         style = {#'backgroundColor' : '#512888',
                                 'color': lighter,
                                  'text-align' : 'center',
                                  'height': '50px',
                                  'text-shadow' : '-1px -1px 0 #eb6e1f, 1px -1px 0 #eb6e1f, -1px 1px 0 #eb6e1f, 1px 1px 0 #eb6e1f'}),
                        
                        html.P([
                            html.P("Pitcher", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'opt', options = opts, value = opts[0]['value'])],
                            style = {'width': '300px',
                                            'fontSize' : '20px',
                                            'padding-left' : '5px',
                                            'display': 'inline-block'}), 
                
                        html.P([
                            html.P("Pitch Type", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'pitch6', options = tops, value = tops[0]['value'])],  #increase num
                            style = {'width': '250px',
                                            'fontSize' : '20px',
                                            'padding-left' : '75px',
                                            'display': 'inline-block'}),
                        html.P([
                            html.P("Ball", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'balls6',     #increase num
                                         options = balls6,
                                         value = balls6[0]['value'])],

                            style = {'width': '150px',
                                            'fontSize' : '20px',
                                            'padding-left' : '75px',
                                            'display': 'inline-block'}),
                        html.P([
                            html.P("Strike", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'strike6', options = strike6, value = strike6[0]['value'])],  #increase num
                            style = {'width': '150px',
                                            'fontSize' : '20px',
                                            'padding-left' : '75px',
                                            'display': 'inline-block'}),
                        html.P([
                            html.P("Batter Handedness", style={'color' : 'white'}),
                            dcc.Dropdown(id = 'batter6', options = batter6, value = batter6[0]['value'])],      #increase num
                            style = {'width': '300px',
                                            'fontSize' : '20px',
                                            'padding-left' : '75px',
                                            'display': 'inline-block'}),]), ], style = {'text-align' : 'center'}),
##                html.P([
##                    dcc.Dropdown(id = 'outs', options = outs, value = outs[0]['value'])],
##                    style = {'width': '100px',
##                                    'fontSize' : '20px',
##                                    'padding-left' : '75px',
##                                    'display': 'inline-block'}),
        
                #html.Div(id='app-1-display-value'),
                #dcc.Link('Go to First', href='/first'),

                html.Div([
                    html.Div([
                        html.H3('Pitch Location Heatmap', style={'color' : 'white'}),
                        dcc.Graph(id='g7',figure = fig5)],  style={                         #increase num
                                                                    "display": "block",
                                                                    "margin-left": "auto",
                                                                    "margin-right": "auto",
                                                                    "width" : "auto"
                                                                    }, className = "six columns"),
                    
                    html.Div([
                        html.H3('vs Left Handed Hitters', style={'color' : 'white'}),
                        dash_table.DataTable(
                        id='table12',        #increase num
                        columns=[{"name": i, "id": i} for i in fin.columns],
                        data=fin.to_dict('records'),
                        style_cell={'textAlign': 'center'},
                        style_data_conditional=[ {
                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 25 && {{{0}}} < 100'.format(x)},
                                'color': 'white',
                                'backgroundColor' : lighter
                            } for x in fin.columns.to_list()
                        ], style_table={'width': '95%'}),
                        
                        html.H3('vs Right Handed Hitters', style={'color' : 'white'}),
                        dash_table.DataTable(
                        id='table13',        #increase num
                        columns=[{"name": i, "id": i} for i in finR.columns],
                        data=finR.to_dict('records'),
                        style_cell={'textAlign': 'center'},
                        style_data_conditional=[ {
                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 25 && {{{0}}} < 100'.format(x)},
                                'color': 'white',
                                'backgroundColor' : lighter
                            } for x in finR.columns.to_list()
                        ],
                        style_table={'width': '95%'})], className = "six columns")], className = "row")], style={
                                                                    'backgroundColor' : darker                   
                                                                    },className = "all")
                    
##                    html.Div([
##                        html.H3('vs Right Handed Hitters'),
##                        dash_table.DataTable(
##                        id='table1',
##                        columns=[{"name": i, "id": i} for i in finR.columns],
##                        data=finR.to_dict('records'),
##                        style_cell={'textAlign': 'center'},
##                        style_data_conditional=[ {
##                                'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 25 && {{{0}}} < 100'.format(x)},
##                                'color': 'white',
##                                'backgroundColor' : 'rgb(111,76,179)'
##                            } for x in finR.columns.to_list()
##                        ],
##                        
##                        style_table={'width': '90%'})], className = "seven columns")], className = "r0w")
##                ], className = "all")


@app.callback(
    Output('g7', 'figure'), #increase num
    [Input('opt', 'value'),
    Input('pitch6','value'),
    Input('balls6','value'),
    Input('strike6','value'),
    Input('batter6', 'value')]
    )
                
def update_figure(input1, input2, input3, input4, input5):
    
    Final = pd.DataFrame()
    df11 = pd.DataFrame()
    df12 = pd.DataFrame()
    df13 = pd.DataFrame()
    df14 = pd.DataFrame()
    df1 = df.query('pitcher_id == @input1')
    df2 = df1.query('pitch_type == @input2')
    df11 = df11.append(df2)
    #for l in input5:
    df3 = df11.query('stand == @input5')
    df12 = df12.append(df3)
    #for j in input4:    
    df4 = df12.query('b_count == @input3')
    df13 = df13.append(df4)
    #for k in input3:    
    df5 = df13.query('s_count == @input4')
    Final = Final.append(df5)
    
    print(Final.shape)
    try:
        trace_2 = go.Histogram2d(x = Final.px, y = Final.pz, colorscale=teamColor ,
                reversescale = False)
        fig = go.Figure(data = [trace_2], layout = layouts)
        fig.layout.update(
            title = go.layout.Title(
                text = "View From Catcher's Viewpoint"),
            xaxis = go.layout.XAxis(
                title=go.layout.xaxis.Title(
                text="Distance From Center of Home Plate (in feet)")),
            yaxis = go.layout.YAxis(
                title=go.layout.yaxis.Title(
                text = "Distance From Ground (in feet, negative means it bounced)")),
        shapes=[
            # unfilled Rectangle
            go.layout.Shape(
                type="rect",
                x0=-.7083,
                y0=1.56,
                x1=.7083,
                y1=3.435,
                line=dict(
                    color="Black",
                ))])
        return fig
    except AttributeError:
        trace_2 = go.Histogram2d(x = df1.px, y = df1.pz, colorscale = 'Blues',reversescale = True)
        fig = go.Figure(data = [trace_2], layout = layouts)
        fig.layout.update(
        shapes=[
            # unfilled Rectangle
            go.layout.Shape(
                type="rect",
                x0=-.7083,
                y0=1.56,
                x1=.7083,
                y1=3.435,
                line=dict(
                    color="Black",
                ))])
        
        return fig1     #increase num

@app.callback(
    Output('table12', 'data'),       #increase num
    [Input('opt', 'value'),
    Input('pitch6','value')])
def update_table_Left(pitcher, value):
    pitches = df.query('pitcher_id == @pitcher').pitch_type.unique()
    j= 0
    i= 0
    bc = ['0','1','2','3']
    sc = ['0','1','2']
    final = pd.DataFrame(data = pitches, columns = ['Pitch Type'])
    for st in s:
        
        j = 0
        for ba in b:
            res = []
            total = df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and stand == "L"').shape[0]
            for value in pitches:
                res.append(df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and pitch_type == @value and stand == "L"').shape[0]
                       /total)
            colname = (bc[j] + '-'+ sc[i])
            #df1 = pd.DataFrame(data = res, columns = [colname])  
            final[colname] = res
            final[colname] = final[colname].multiply(100)
            final[colname] = final[colname].round(3)
            j += 1
        i += 1
    
    
    return final.to_dict('records')
@app.callback(
    Output('table13', 'data'),       #increase num
    [Input('opt', 'value'),
    Input('pitch6','value')])
def update_table_Right(pitcher, value):
    pitches = df.query('pitcher_id == @pitcher').pitch_type.unique()
    j= 0
    i= 0
    bc = ['0','1','2','3']
    sc = ['0','1','2']
    final = pd.DataFrame(data = pitches, columns = ['Pitch Type'])
    for st in s:
        
        j = 0
        for ba in b:
            res = []
            total = df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and stand == "R"').shape[0]
            for value in pitches:
                res.append(df.query('pitcher_id == @pitcher and b_count == @ba and s_count == @st and pitch_type == @value and stand == "R"').shape[0]
                       /total)
            colname = (bc[j] + '-'+ sc[i])
            #df1 = pd.DataFrame(data = res, columns = [colname])  
            final[colname] = res
            final[colname] = final[colname].multiply(100)
            final[colname] = final[colname].round(3)
            j += 1
        i += 1
    
    
    return final.to_dict('records')
@app.callback(
    Output('pitch6', 'options'),        #increase num
    [Input('opt', 'value')])
def update_dropdown(input1):
    pitchTypes = df.query('pitcher_id == @input1').pitch_type.unique()
    return [{'label' : j, 'value' : j} for j in pitchTypes]
    


if __name__ == '__main__':
    app.run_server(debug=True)



# https://community.plot.ly/t/two-graphs-side-by-side/5312
