import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json 
import requests 



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Link de obtenção dos dados: https://covid.saude.gov.br/
link = 'https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/2827dd737e968b1e84556406ec0530ac_HIST_PAINEL_COVIDBR_20mar2021.csv'
df = pd.read_csv(link, sep=';')

#df = pd.read_csv('HIST_PAINEL_COVIDBR_07mar2021.csv', sep=';')
#df_lat = pd.read_csv("municipios_lat_long.csv")

df_lat = pd.read_csv('https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv', sep=',')

#json_file = 'br_states.json'
#geo_json_data  = json.load(open(json_file))

json_file = 'https://github.com/datalivre/Conjunto-de-Dados/raw/master/br_states.json'
response = requests.get(json_file)
geo_json_data = response.json()

df_lat.rename(columns = {'nome': 'municipio'}, inplace=True)


df['ano'] = pd.to_datetime(df['data'], format='%Y-%m').dt.strftime('%Y')


sum_casos_novos_por_dt_notificacao = df[['data', 'ano','casosNovos', 'estado']].groupby(['data','ano', 'estado']).sum().reset_index() 
sum_casos_novos_semana_epi = df[['semanaEpi', 'casosNovos', 'estado', 'ano']].groupby(['semanaEpi', 'estado', 'ano']).sum().reset_index()

sum_casos_acumulados_por_dt_notificacao = df[['data', 'ano','casosAcumulado', 'estado']].groupby(['data','ano', 'estado']).sum().reset_index() 
sum_casos_acumulados_semana_epi = df[['semanaEpi', 'casosAcumulado', 'estado', 'ano']].groupby(['semanaEpi', 'estado', 'ano']).sum().reset_index()

sum_casos_acumu_por_dt_notificacao_regiao = df[['data', 'ano','casosAcumulado', 'regiao', 'estado']].groupby(['data','ano', 'regiao', 'estado']).sum().reset_index() 
sum_casos_acumu_por_semanaepi_regiao = df[['semanaEpi', 'ano','casosAcumulado', 'regiao', 'estado']].groupby(['semanaEpi','ano', 'regiao', 'estado']).sum().reset_index() 

sum_casos_acumu_por_municipio = df[['ano','casosAcumulado', 'regiao', 'estado', 'municipio']].groupby(['ano', 'regiao', 'estado', 'municipio']).sum().reset_index() 
sum_casos_acumu_por_municipio = sum_casos_acumu_por_municipio.merge(df_lat[['municipio', 'latitude', 'longitude']], how='inner', on='municipio')
sum_casos_acumu_por_municipio = sum_casos_acumu_por_municipio[['ano',
                                                                'casosAcumulado', 
                                                                'regiao', 
                                                                'estado', 
                                                                'municipio', 
                                                                'latitude', 
                                                                'longitude']].groupby(['ano', 
                                                                                        'regiao', 
                                                                                        'estado', 
                                                                                        'municipio',
                                                                                        'latitude', 
                                                                                        'longitude']).max().reset_index() 


sum_obitos_novos_por_dt_notificacao = df[['data', 'ano','obitosNovos', 'estado']].groupby(['data','ano', 'estado']).sum().reset_index() 
sum_obitos_novos_semana_epi = df[['semanaEpi', 'obitosNovos', 'estado', 'ano']].groupby(['semanaEpi', 'estado', 'ano']).sum().reset_index()

sum_obitos_acumu_por_dt_notificacao = df[['data', 'ano','obitosAcumulado', 'estado']].groupby(['data','ano', 'estado']).sum().reset_index() 
sum_obitos_acumu_semana_epi = df[['semanaEpi', 'obitosAcumulado', 'estado', 'ano']].groupby(['semanaEpi', 'estado', 'ano']).sum().reset_index()


sum_obitos_acumu_por_dt_notificacao_regiao = df[['data', 'ano','obitosAcumulado', 'regiao', 'estado']].groupby(['data','ano', 'regiao', 'estado']).sum().reset_index() 
sum_obitos_acumu_por_semanaepi_regiao = df[['semanaEpi', 'ano','obitosAcumulado', 'regiao', 'estado']].groupby(['semanaEpi','ano', 'regiao', 'estado']).sum().reset_index() 


sum_obitos_acumu_por_municipio = df[['ano','obitosAcumulado', 'regiao', 'estado', 'municipio']].groupby(['ano', 'regiao', 'estado', 'municipio']).sum().reset_index() 
sum_obitos_acumu_por_municipio = sum_obitos_acumu_por_municipio.merge(df_lat[['municipio', 'latitude', 'longitude']], how='inner', on='municipio')
sum_obitos_acumu_por_municipio = sum_obitos_acumu_por_municipio[['ano',
                                                                'obitosAcumulado', 
                                                                'regiao', 
                                                                'estado', 
                                                                'municipio', 
                                                                'latitude', 
                                                                'longitude']].groupby(['ano', 
                                                                                        'regiao', 
                                                                                        'estado', 
                                                                                        'municipio',
                                                                                        'latitude', 
                                                                                        'longitude']).max().reset_index() 





estados = df[~df['estado'].isna()].sort_values('estado')['estado'].unique()
anos = df['ano'].unique()
regiao = df['regiao'].unique()
app.layout = html.Div([
    html.Div([
        html.Label("Selecione uma UF"),
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in estados],
                value='CE'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            
            dcc.Dropdown(
                id='filter-rage-date',
                options=[{'label': i, 'value': i} for i in anos],
                value=anos[0]
            )
        ],
        style={'width': '49%'}),
        html.Br(),
    
        ], style={
                    'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'padding': '20px 10px'
            }
    ),
    html.Div([
        html.H5('CASOS CONFIRMADOS', className='my-class', id='my-p-element')
    ], style={'marginBottom': 50, 'marginTop': 25}),
    #html.Br(),
    

    # html.Div([
    #    dcc.Graph(
    #        id='crossfilter-indicator-scatter',
    #        hoverData={'points': [{'customdata': 'Japan'}]}
    #    )
    # ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    
    #Casos confirmados 
    html.Div([
        dcc.Graph(id='bar-chart-casos-novos-covid-por-dia'),
        html.Br(),
        dcc.Graph(id='line-chart-casos-acumulados-por-dia'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div([
        dcc.Graph(id='bar-chart-casos-novos-covid-semanaepi'),
        html.Br(),
        dcc.Graph(id='line-chart-casos-acumulados-semanaEpi'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                id='filter-regiao',
                options=[{'label': i, 'value': i} for i in regiao if 'Brasil' not in i],
                value=regiao[1]
            )
        ],
        style={'width': '20%'}),

    html.Div([
        dcc.Graph(id='line-chart-casos-acumulados-covid-por-dia-regiao'),
        html.Br(),
        dcc.Graph(id='map-chart-casos-acumulados-covid-dt-notificacao'),
        
    ], style={'display': 'inline-block', 'width': '49%'}),
 
    html.Div([ 
        dcc.Graph(id='line-chart-casos-acumulados-covid-por-semanaepi-regiao'),
        html.Br(),
        dcc.Graph(id='map-chart-casos-acumulados-covid-semapaepi')
        
    ], style={'display': 'inline-block', 'width': '49%'}),



    #Casos Obitos 
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Graph(id='bar-chart-casos-obitos-covid-por-dia'),
        html.Br(),
        dcc.Graph(id='line-chart-casos-acumu-obitos-por-dia'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div([
        dcc.Graph(id='bar-chart-casos-obitos-covid-semanaepi'),
        html.Br(),
        dcc.Graph(id='line-chart-casos-acumu-obitos-semanaEpi'),
    ], style={'display': 'inline-block', 'width': '49%'}),


    html.Div([
        dcc.Graph(id='line-chart-casos-acumu-obitos-covid-por-dia-regiao'),
        html.Br(),
        dcc.Graph(id='map-chart-obitos-acumulados-covid-dt-notificacao'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div([
        dcc.Graph(id='line-chart-casos-acumu-obitos-covid-semanaepi-regiao'),
        html.Br(),
        dcc.Graph(id='map-chart-obitos-acumulados-covid-semapaepi')

    ], style={'display': 'inline-block', 'width': '49%'}),
    
])



#CASOS CONFIRMADOS 
def create_bar_chart_casos_novos_covid_por_dia(dff, axis_type, title):

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dff['data'],
        y= dff['casosNovos'][dff['casosNovos'] >= 0], 
        marker_color='green',
        name='Casos'

    ))

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.update_layout(
        title='<b>Casos novos de COVID-19 por data de notificação</b>',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='<b>Casos Novos</b>',
            titlefont_size=16,
            tickfont_size=14,
        ),

        xaxis=dict(
            title='<b>Data de Notificação</b>',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis_tickformat = '%m-%d',
        xaxis_tickangle=-45,
        height=500
    )

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback(
    dash.dependencies.Output('bar-chart-casos-novos-covid-por-dia', 'figure'),
    [
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]

)
def bar_chart_casos_novos_covid_por_dia(yaxis_column_name, xaxis_type, filter_range_date):   
    uf = yaxis_column_name
    df = sum_casos_novos_por_dt_notificacao[sum_casos_novos_por_dt_notificacao['ano'] == filter_range_date]
    df = df[df['estado'] == uf].sort_values(by='data')
    title='<b>{}</b>'.format(uf)
    return create_bar_chart_casos_novos_covid_por_dia(df, xaxis_type, title)




def create_bar_chart_casos_novos_covid_semanaepi(dff, axis_type, title):

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dff['semanaEpi'],
        y= dff['casosNovos'][dff['casosNovos'] >= 0], 
        marker_color='green',
        name='Casos',

    ))

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
    fig.update_layout(
        title='<b>Casos novos de COVID-19 por Semana Epidemiológica de notificação</b>',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='<b>Casos Novos</b>',
            titlefont_size=16,
            tickfont_size=14,
        ),

        xaxis=dict(
            title='<b>Semana Epidemiológica</b>',
            titlefont_size=16,
            tickfont_size=14,
        ),
        #xaxis_tickformat = '%m-%d',
        yaxis_tickformat = '',
        xaxis_tickangle=-45,
        height=500 
    )

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig



@app.callback(
    dash.dependencies.Output('bar-chart-casos-novos-covid-semanaepi', 'figure'),
    [
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]

)
def bar_chart_casos_novos_covid_semanaepi(yaxis_column_name, xaxis_type, filter_range_date):   
    uf = yaxis_column_name
    df = sum_casos_novos_semana_epi[sum_casos_novos_semana_epi['ano'] == filter_range_date]
    
    df = df[df['estado'] == uf].sort_values(by='semanaEpi')
    title='<b>{}</b>'.format(uf)
    return create_bar_chart_casos_novos_covid_semanaepi(df, xaxis_type, title)



def create_line_chart_casos_acumulados_por_dt_notificacao(df, axis_type, title):
    
    def create_shape(k, df, color):
        y=list(df['casosAcumulado'])
        zero = 0
        dt = df['data']
        
        
        return dict(type='path',
                    path=f'M {dt[k]}, {y[k]} L {dt[k+1]}, {y[k+1]} L {dt[k+1]} {zero}'+\
                            f' L {dt[k]}, {zero} Z',
                    fillcolor=color,
                    line=dict(color=color, width=0)
                )

    
    df = df.reset_index(drop=True)
    shapes=[]
    for k in range(len(df.index) - 1):
        shapes.append(create_shape(k, df, 'rgba(0,255,0,0.2)' ))

        
                            
    fig= go.Figure(go.Scatter(  
            x=df.data, 
            y=df.casosAcumulado,
            name='Acumulados',
            mode='lines',
            line_width=5.0, 
            line_color='rgb(0, 255, 0)',
            ))

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.update_layout(
            title='<b>Casos acumulados de COVID-19 por data de notificação</b>',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='<b>Casos Acumulados</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),

            xaxis=dict(
                title='<b>Data de Notificação</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),
            xaxis_tickformat = '%m-%d',
            yaxis_tickformat = '',
            xaxis_tickangle=-45,
            height=500,
            #width=600,
            shapes=shapes)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    return fig


@app.callback(
    dash.dependencies.Output('line-chart-casos-acumulados-por-dia', 'figure'),
    [
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]

)
def line_chart_casos_acumulados_por_dt_notificacao(yaxis_column_name, xaxis_type, filter_range_date):
    uf = yaxis_column_name
        
    df = sum_casos_acumulados_por_dt_notificacao[sum_casos_acumulados_por_dt_notificacao['ano'] == filter_range_date]
    df = df[df['estado'] == uf]
    title='<b>{}</b>'.format(uf)
    return create_line_chart_casos_acumulados_por_dt_notificacao(df, xaxis_type, title)





def create_line_chart_casos_novos_covid_semanaepi(df, axis_type, title):
    
    def create_shape(k, df, color):
        y=list(df['casosAcumulado'])
        zero = 0
        dt = df['semanaEpi']
        
        
        return dict(type='path',
                    path=f'M {dt[k]}, {y[k]} L {dt[k+1]}, {y[k+1]} L {dt[k+1]} {zero}'+\
                            f' L {dt[k]}, {zero} Z',
                    fillcolor=color,
                    line=dict(color=color, width=0)
                )

    
    df = df.reset_index(drop=True)
    shapes=[]
    for k in range(len(df.index) - 1):
        shapes.append(create_shape(k, df, 'rgba(0,255,0,0.2)' ))

        
                            
    fig= go.Figure(go.Scatter(  
            x=df.semanaEpi, 
            y=df.casosAcumulado,
            name='Acumulados',
            mode='lines',
            line_width=5.0, 
            line_color='rgb(0, 255, 0)',
            ))

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.update_layout(
            title='<b>Casos acumulados de COVID-19 por data de notificação</b>',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='<b>Casos Acumulados</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),

            xaxis=dict(
                title='<b>Semana Epidemiológica</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),
            #xaxis_tickformat = '%m-%d',
            yaxis_tickformat = '',
            xaxis_tickangle=-45,
            height=500,
            #width=600,
            shapes=shapes)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback( 
    dash.dependencies.Output('line-chart-casos-acumulados-semanaEpi', 'figure'),
    [
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]

)
def line_chart_casos_novos_covid_semanaepi(yaxis_column_name, xaxis_type, filter_range_date):
    uf = yaxis_column_name
        
    df = sum_casos_acumulados_semana_epi[sum_casos_acumulados_semana_epi['ano'] == filter_range_date]
    df = df[df['estado'] == uf]
    title='<b>{}</b>'.format(uf)
    return create_line_chart_casos_novos_covid_semanaepi(df, xaxis_type, title)    




def create_line_chart_casos_novos_covid_por_dia_regiao(df, axis_type, title):
           
    
    fig = px.line(df, x="data", y="casosAcumulado", color='estado')
    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
 

    fig.update_layout(
            title='<b>Casos acumulados de COVID-19 por região e data de notificação</b>',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='<b>Casos Acumulados</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),

            xaxis=dict(
                title='<b>Data de Notificação</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),
            #xaxis_tickformat = '%m-%d',
            yaxis_tickformat = '',
            xaxis_tickangle=-45,
            height=500)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback(
    dash.dependencies.Output('line-chart-casos-acumulados-covid-por-dia-regiao', 'figure'),
    [
        dash.dependencies.Input('filter-regiao', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
        
    ]

)
def line_chart_casos_novos_covid_por_dia_regiao(filter_regiao, xaxis_type, filter_range_date):
    regiao = filter_regiao
    df = sum_casos_acumu_por_dt_notificacao_regiao[sum_casos_acumu_por_dt_notificacao_regiao['ano'] == filter_range_date]
    df = df[df['regiao'] == regiao]
    title='<b>{}</b>'.format(regiao)
    return create_line_chart_casos_novos_covid_por_dia_regiao(df, xaxis_type, title)    





def create_line_chart_casos_novos_covid_por_semanaepi_regiao(df, axis_type, title):
           
    
    fig = px.line(df, x="semanaEpi", y="casosAcumulado", color='estado')
    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
 

    fig.update_layout(
            title='<b>Casos acumulados de COVID-19 por região e Semana Epidemiológica</b>',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='<b>Casos Acumulados</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),

            xaxis=dict(
                title='<b>Semana Epidemiológica</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),
            #xaxis_tickformat = '%m-%d',
            yaxis_tickformat = '',
            xaxis_tickangle=-45,
            height=500)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback(
    dash.dependencies.Output('line-chart-casos-acumulados-covid-por-semanaepi-regiao', 'figure'),
    [
        dash.dependencies.Input('filter-regiao', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
        
    ]

)
def line_chart_casos_novos_covid_semanaepi_regiao(filter_regiao, xaxis_type, filter_range_date):
    regiao = filter_regiao
    
    df = sum_casos_acumu_por_semanaepi_regiao[sum_casos_acumu_por_semanaepi_regiao['ano'] == filter_range_date]
    
    df = df[df['regiao'] == regiao]
    
    title='<b>{}</b>'.format(regiao)
    return create_line_chart_casos_novos_covid_por_semanaepi_regiao(df, xaxis_type, title)    




def create_map_chart_casos_acumulados_covid_dt_notificacao(df):

    
    fig = px.choropleth_mapbox(df, geojson=geo_json_data, color="casosAcumulado",
                            color_continuous_scale="Blues",
                            locations="estado", featureidkey="id",
                            center={"lat": -14.2400732, "lon": -53.1805017},
                            mapbox_style="carto-positron", zoom=3)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig 


@app.callback(
    dash.dependencies.Output('map-chart-casos-acumulados-covid-dt-notificacao', 'figure'),
    [
        dash.dependencies.Input('filter-rage-date', 'value')
        
    ]
)

def map_chart_casos_acumulados_covid_dt_notificacao(filter_range_date):
    df = sum_casos_acumu_por_dt_notificacao_regiao[['estado', 'casosAcumulado', 'ano']].groupby(['estado', 'ano']).max().reset_index().sort_values('casosAcumulado')
    df = df[df['ano'] == filter_range_date]

    return create_map_chart_casos_acumulados_covid_dt_notificacao(df)   




def create_map_chart_casos_acumulados_covid_semapaepi(df):
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="estado", hover_data=["municipio", "casosAcumulado"],
                            color_discrete_sequence=["blue"], zoom=3, height=450)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig 


@app.callback(
    dash.dependencies.Output('map-chart-casos-acumulados-covid-semapaepi', 'figure'),
    [
        dash.dependencies.Input('filter-rage-date', 'value')
    ]
)

def map_chart_casos_acumulados_covid_dt_notificacao(filter_range_date):
    df = sum_casos_acumu_por_municipio[sum_casos_acumu_por_municipio['ano'] == filter_range_date]
    
    return create_map_chart_casos_acumulados_covid_semapaepi(df)   



#CASOS OBITOS 
#OBITOS POR DIA 
def create_bar_chart_casos_obitos_covid_por_dia(dff, axis_type, title):

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dff['data'],
        y= dff['obitosNovos'][dff['obitosNovos'] >= 0], 
        marker_color='red',
        name='Casos'

    ))

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.update_layout(
        title='<b>Óbitos novos de COVID-19 por data de notificação</b>',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='<b>Novos óbitos</b>',
            titlefont_size=16,
            tickfont_size=14,
        ),

        xaxis=dict(
            title='<b>Data de Notificação</b>',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis_tickformat = '%m-%d',
        xaxis_tickangle=-45,
        height=500
    )

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback(
    dash.dependencies.Output('bar-chart-casos-obitos-covid-por-dia', 'figure'),
    [
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]

)


def bar_chart_casos_obitos_covid_por_dia(yaxis_column_name, xaxis_type, filter_range_date):   
    uf = yaxis_column_name
    df = sum_obitos_novos_por_dt_notificacao[sum_obitos_novos_por_dt_notificacao['ano'] == filter_range_date]
    df = df[df['estado'] == uf].sort_values(by='data')
    title='<b>{}</b>'.format(uf)
    return create_bar_chart_casos_obitos_covid_por_dia(df, xaxis_type, title)



#OBITOS POR SEMANA EPIDEMIOLOGICA
def create_bar_chart_casos_obitos_covid_semanaepi(dff, axis_type, title):

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dff['semanaEpi'],
        y= dff['obitosNovos'][dff['obitosNovos'] >= 0], 
        marker_color='red',
        name='Casos'

    ))

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.update_layout(
        title='<b>Óbitos novos de COVID-19 por Semana Epidemiológica</b>',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='<b>Novos óbitos</b>',
            titlefont_size=16,
            tickfont_size=14,
        ),

        xaxis=dict(
            title='<b>Semana Epidemiológica</b>',
            titlefont_size=16,
            tickfont_size=14,
        ),
        #xaxis_tickformat = '%m-%d',
        xaxis_tickangle=-45,
        height=500
    )

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback(
    dash.dependencies.Output('bar-chart-casos-obitos-covid-semanaepi', 'figure'),
    [
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]
)

def bar_chart_casos_obitos_covid_semanaepi(yaxis_column_name, xaxis_type, filter_range_date):   
    uf = yaxis_column_name
    df = sum_obitos_novos_semana_epi[sum_obitos_novos_semana_epi['ano'] == filter_range_date]
    df = df[df['estado'] == uf].sort_values(by='semanaEpi')
    title='<b>{}</b>'.format(uf)
    return create_bar_chart_casos_obitos_covid_semanaepi(df, xaxis_type, title)



#Grafico linha obitos acumulados por dia 
def create_line_chart_casos_acumu_obitos_por_dia(df, axis_type, title):
    
    def create_shape(k, df, color):
        y=list(df['obitosAcumulado'])
        zero = 0
        dt = df['data']
        
        
        return dict(type='path',
                    path=f'M {dt[k]}, {y[k]} L {dt[k+1]}, {y[k+1]} L {dt[k+1]} {zero}'+\
                            f' L {dt[k]}, {zero} Z',
                    fillcolor=color,
                    line=dict(color=color, width=0)
                )

    
    df = df.reset_index(drop=True)
    shapes=[]
    for k in range(len(df.index) - 1):
        shapes.append(create_shape(k, df, 'rgba(255,0,0,0.2)' ))

        
                            
    fig= go.Figure(go.Scatter(  
            x=df.data, 
            y=df.obitosAcumulado,
            name='Acumulados',
            mode='lines',
            line_width=5.0, 
            line_color='#FF0000',
            ))

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.update_layout(
            title='<b>Casos acumulados de COVID-19 por data de notificação</b>',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='<b>Óbitos Acumulados</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),

            xaxis=dict(
                title='<b>Data de Notificação</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),
            xaxis_tickformat = '%m-%d',
            yaxis_tickformat = '',
            xaxis_tickangle=-45,
            height=500,
            #width=600,
            shapes=shapes)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    return fig


@app.callback(
    dash.dependencies.Output('line-chart-casos-acumu-obitos-por-dia', 'figure'),
    [
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]

)
def line_chart_casos_acumu_obitos_por_dia(yaxis_column_name, xaxis_type, filter_range_date):
    uf = yaxis_column_name
        
    df = sum_obitos_acumu_por_dt_notificacao[sum_obitos_acumu_por_dt_notificacao['ano'] == filter_range_date]
    df = df[df['estado'] == uf]
    title='<b>{}</b>'.format(uf)
    return create_line_chart_casos_acumu_obitos_por_dia(df, xaxis_type, title)




#Grafico linha obitos acumulados por semana Epidemiologica
def create_line_chart_casos_acumu_obitos_semanaEpi(df, axis_type, title):
    
    def create_shape(k, df, color):
        y=list(df['obitosAcumulado'])
        zero = 0
        dt = df['semanaEpi']
        
        
        return dict(type='path',
                    path=f'M {dt[k]}, {y[k]} L {dt[k+1]}, {y[k+1]} L {dt[k+1]} {zero}'+\
                            f' L {dt[k]}, {zero} Z',
                    fillcolor=color,
                    line=dict(color=color, width=0)
                )

    
    df = df.reset_index(drop=True)
    shapes=[]
    for k in range(len(df.index) - 1):
        shapes.append(create_shape(k, df, 'rgba(255,0,0,0.2)' ))

        
                            
    fig= go.Figure(go.Scatter(  
            x=df.semanaEpi, 
            y=df.obitosAcumulado,
            name='Acumulados',
            mode='lines',
            line_width=5.0, 
            line_color='#FF0000',
            ))

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.update_layout(
            title='<b>Casos acumulados de COVID-19 por data de notificação</b>',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='<b>Óbitos Acumulados</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),

            xaxis=dict(
                title='<b>Semana Epidemiológica</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),
            #xaxis_tickformat = '%m-%d',
            yaxis_tickformat = '',
            xaxis_tickangle=-45,
            height=500,
            #width=600,
            shapes=shapes)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback( 
    dash.dependencies.Output('line-chart-casos-acumu-obitos-semanaEpi', 'figure'),
    [
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]

)
def line_chart_casos_acumu_obitos_semanaEpi(yaxis_column_name, xaxis_type, filter_range_date):
    uf = yaxis_column_name
        
    df = sum_obitos_acumu_semana_epi[sum_obitos_acumu_semana_epi['ano'] == filter_range_date]
    df = df[df['estado'] == uf]
    title='<b>{}</b>'.format(uf)
    return create_line_chart_casos_acumu_obitos_semanaEpi(df, xaxis_type, title)    





def create_line_chart_casos_acumu_obitos_covid_por_dia_regiao(df, axis_type, title):
           
    
    fig = px.line(df, x="data", y="obitosAcumulado", color='estado')
    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
 

    fig.update_layout(
            title='<b>Óbitos acumulados de COVID-19 por região e data de notificação</b>',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='<b>Óbitos Acumulados</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),

            xaxis=dict(
                title='<b>Data de Notificação</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),
            #xaxis_tickformat = '%m-%d',
            yaxis_tickformat = '',
            xaxis_tickangle=-45,
            height=500)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback(
    dash.dependencies.Output('line-chart-casos-acumu-obitos-covid-por-dia-regiao', 'figure'),
    [
        dash.dependencies.Input('filter-regiao', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
    ]
)
def line_chart_casos_acumu_obitos_covid_por_dia_regiao(filter_regiao, xaxis_type, filter_range_date):
    regiao = filter_regiao
    df = sum_obitos_acumu_por_dt_notificacao_regiao[sum_obitos_acumu_por_dt_notificacao_regiao['ano'] == filter_range_date]
    df = df[df['regiao'] == regiao]
    title='<b>{}</b>'.format(regiao)
    return create_line_chart_casos_acumu_obitos_covid_por_dia_regiao(df, xaxis_type, title)    





def create_line_chart_casos_acumu_obitos_covid_semanaepi_regiao(df, axis_type, title):
           
    
    fig = px.line(df, x="semanaEpi", y="obitosAcumulado", color='estado')
    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
 

    fig.update_layout(
            title='<b>Óbitos acumulados de COVID-19 por região e Semana Epidemiológica</b>',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='<b>Óbitos Acumulados</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),

            xaxis=dict(
                title='<b>Semana Epidemiológica</b>',
                titlefont_size=16,
                tickfont_size=14,
            ),
            #xaxis_tickformat = '%m-%d',
            yaxis_tickformat = '',
            xaxis_tickangle=-45,
            height=500)

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    return fig


@app.callback(
    dash.dependencies.Output('line-chart-casos-acumu-obitos-covid-semanaepi-regiao', 'figure'),
    [
        dash.dependencies.Input('filter-regiao', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('filter-rage-date', 'value')
        
    ]

)
def line_chart_casos_acumu_obitos_covid_semanaepi_regiao(filter_regiao, xaxis_type, filter_range_date):
    regiao = filter_regiao
    
    df = sum_obitos_acumu_por_semanaepi_regiao[sum_obitos_acumu_por_semanaepi_regiao['ano'] == filter_range_date]
    
    df = df[df['regiao'] == regiao]
    
    title='<b>{}</b>'.format(regiao)
    return create_line_chart_casos_acumu_obitos_covid_semanaepi_regiao(df, xaxis_type, title) 




def create_map_chart_obitos_acumulados_covid_dt_notificacao(df):

    
    fig = px.choropleth_mapbox(df, geojson=geo_json_data, color="obitosAcumulado",
                            color_continuous_scale="Reds",
                            locations="estado", featureidkey="id",
                            center={"lat": -14.2400732, "lon": -53.1805017},
                            mapbox_style="carto-positron", zoom=3)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig 


@app.callback(
    dash.dependencies.Output('map-chart-obitos-acumulados-covid-dt-notificacao', 'figure'),
    [
        dash.dependencies.Input('filter-rage-date', 'value')
        
    ]
)

def map_chart_obitos_acumulados_covid_dt_notificacao(filter_range_date):
    df = sum_obitos_acumu_por_dt_notificacao_regiao[['estado', 'obitosAcumulado', 'ano']].groupby(['estado', 'ano']).max().reset_index().sort_values('obitosAcumulado')
    df = df[df['ano'] == filter_range_date]

    return create_map_chart_obitos_acumulados_covid_dt_notificacao(df)   




def create_map_chart_obitos_acumulados_covid_semapaepi(df):
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="estado", hover_data=["municipio", "obitosAcumulado"],
                            color_discrete_sequence=["red"], zoom=3, height=450)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig 

 
@app.callback(
    dash.dependencies.Output('map-chart-obitos-acumulados-covid-semapaepi', 'figure'),
    [
        dash.dependencies.Input('filter-rage-date', 'value')
    ]
)

def map_chart_obitos_acumulados_covid_dt_notificacao(filter_range_date):
    df = sum_obitos_acumu_por_municipio[sum_obitos_acumu_por_municipio['ano'] == filter_range_date]
    
    return create_map_chart_obitos_acumulados_covid_semapaepi(df) 


if __name__ == '__main__':
    app.run_server(debug=True)

