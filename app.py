# 1. Import Dash
from ctypes import alignment
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
from statistics import mode
import plotly.express as px

print('BERHASIL')

# 2. Create a Dash app instance, THEME
app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY],
    name='Co2 Emissions'
)

# -- Navbar & Title Tab --
app.title='CO2 Emissions'
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
    ],
    brand="Carbon Dioxide Emissions Around The Globe",
    brand_href="#",
    color="primary",
    dark=True,
    brand_style={'fontSize' : '28px'},
    style={'fontSize':'20px'},
)

# -- IMPORT & QUERYING DATASET CO2 --
df1=pd.read_csv('owid-co2-data.csv')
df = df1[['country', 'year', 'iso_code', 'co2_per_capita']]
df.drop(df[df['year'] < 1980].index, inplace=True)

# -- CHOROPLETH --
df_choropleth = df.rename(columns = {'co2_per_capita':'CO2 Per Capita'})
plot_map= px.choropleth(df_choropleth,
    locations='iso_code',
    color_continuous_scale='OrRd',
    color='CO2 Per Capita',
    range_color=[0, 20],
    animation_frame='year',
    labels={
        'year':'Year'
    },
    hover_name='country',
    hover_data={
        'iso_code': False,
        'year' : False
    }
)

# -- LINE CHART --
df_line = df.drop('iso_code', axis = 1).dropna()

line_chart = px.line(
    df_line[df_line['country'] == 'World'], 
    x="year", 
    y="co2_per_capita",
    color='country',
    labels={
        'co2_per_capita': 'CO2 Per Capita (Tonnes)',
        'year' : 'Year',
        'country' : 'Country'
    },
    title='The Trend of CO2 Emissions Per Capita Around World',
    template='seaborn'
)

line_chart.update_layout(hovermode="x")
line_chart.update_traces(
    hovertemplate= 
    "CO2 Per Capita: %{y:.2f} Tonne"
)

# --------- BAR ---------- 
df_bar = df.dropna()
df_bar = df_bar[df_bar['year']==2021].sort_values('co2_per_capita')

bar_plot = px.bar(
    data_frame=df_bar.tail(10),
    y='country',
    x='co2_per_capita',
    labels={
        'country' : 'Country',
        'co2_per_capita' : 'CO2 Per Capita (Tonnes)'
    },
    title='Top 10 Country with The Highest CO2 Emission per Capita',
    
    #template='seaborn'
)
bar_plot.update_traces(
    hovertemplate= 
    "<b>%{y}</b><br><br>"
    "CO2 Per Capita: %{x:.2f} Tonne"    
)

# ------------------- PIE ---------------
df_pie2 = df1[['year', 'cement_co2', 'coal_co2', 'flaring_co2', 'gas_co2', 'oil_co2', 'other_industry_co2']]
df_pie2 = df_pie2[df_pie2['year'] == 2021]
df_pie2 = df_pie2.groupby(by='year').sum().reset_index()
df_pie2 = pd.melt(df_pie2, id_vars='year')
change={
    'coal_co2':'Coal',
    'oil_co2':'Oil',
    'gas_co2':'Gas',
    'cement_co2':'Cement',
    'flaring_co2':'Flaring',
    'other_industry_co2':'Other Industry'
}
df_pie2 = df_pie2.replace({'variable':change})
pie_plot = px.pie(
    df_pie2,
    values='value',
    names='variable',
    color='variable',
    title='CO2',
    template='plotly',
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
pie_plot.update_traces(
    hovertemplate= 
    "<b>%{label}</b><br><br>"
    "CO2 (in million Tonnes): %{value:,.2f}",
    textinfo='label+percent',
    textfont_size=14
)

pie_plot.update_layout(
    title={
        'text': "The Source of CO2 Emissions in 2021",
        'y':0.9,
        'x':0.47,
        'xanchor': 'center',
        'yanchor': 'top'})

# ---------------------- LAYOUT ----------------------------
app.layout = html.Div(children=[
    navbar,

    html.Br(),
    
    # --Component Main Page--
    html.Div([
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Carbon Dioxide (CO2) Gas Emission'),
                    dbc.CardBody([
                        html.P("Emissions of greenhouse gases, predominantly carbon dioxide, have been steadily increasing and kicking the greenhouse effect out of balance. What does this mean? Essentially, there are too many greenhouse gases absorbing the sun's energy, which means our planet is slowly warming up. We know this as climate change.", 
                            style={
                                'textAlign' : 'justify',
                                'fontFamily' : 'Helvetica'
                            }
                        ),
                        html.P('Carbon dioxide (CO2) is a colourless, odourless and non-poisonous gas formed by combustion of carbon and in the respiration of living organisms and is considered a greenhouse gas. Emissions means the release of greenhouse gases and/or their precursors into the atmosphere over a specified area and period of time. Carbon dioxide emissions or CO2 emissions are emissions stemming from the burning of fossil fuels and the manufacture of cement; they include carbon dioxide produced during consumption of solid, liquid, and gas fuels as well as gas flaring.',
                            style={
                                'textAlign' : 'justify',
                                'fontFamily' : 'Helvetica'
                            }
                        ),
                        html.H6('Source:',
                            style={
                                'textAlign' : 'justify',
                                'fontFamily' : 'Helvetica'
                            }
                        ),
                        dbc.CardLink('Our World in Data ', href='https://ourworldindata.org/per-capita-co2'),
                        dbc.CardLink('Eurostat Statistics Explained', href='https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Carbon_dioxide_emissions#:~:text=Carbon%20dioxide%20(CO2)%20is,area%20and%20period%20of%20time.'),
                        #html.P('Carbon dioxide is a chemical compound made up of molecules that each have one carbon atom covalently double bonded to two oxygen atoms. It is found in the gas state at room temperature.'),
                        #html.P("In the air, carbon dioxide is transparent to visible light but absorbs infrared radiation, acting as a greenhouse gas. It is a trace gas in Earth's atmosphere at 417 ppm (about 0.04%) by volume, having risen from pre-industrial levels of 280 ppm. Burning fossil fuels is the primary cause of these increased CO2 concentrations and also the primary cause of global warming and climate change. Carbon dioxide is soluble in water and is found in groundwater, lakes, ice caps, and seawater. When carbon dioxide dissolves in water it forms carbonic acid (H2CO3), which causes ocean acidification as atmospheric CO2 levels increase.")
                    ])
                ])
            ],
            width=6
            ),
            dbc.Col([
                dcc.Graph(
                    id='choropleth',
                    figure=plot_map
                )
            ],
            width=6
            ),
        ]),

        dbc.Row([
            html.Br(),
            html.Br(),
            dbc.Col([
                html.H4('Anlysis by Country', style={'paddingTop':'10px'}),
                dbc.Tabs([
                    dbc.Tab([
                        dcc.RadioItems(
                        options=[
                            {
                                'label': 'Highest', 
                                'value': True
                            },
                            {
                                'label':'Lowest',
                                'value': False,
                            },
                        ],
                        value=True,
                        id='bar_sort',
                        style={
                            'paddingTop' : '10px'
                        }
                        ),
                        dcc.Graph(
                            id='bar_plot',
                            figure=bar_plot
                        )],
                        label='Ranking'
                    ),
                    dbc.Tab([
                        dcc.Dropdown(
                            id='choose_country',
                            options=df_line['country'].unique(),
                            value='World',
                            multi=True
                        ),
                        dcc.Graph(
                            id='line_chart',
                            figure=line_chart 
                        )],
                        label='Trend'
                    ),
                ]),
            ],
            width=6
            ),
            dbc.Col([
                html.H4('Anlysis by The Source', style={'paddingTop':'10px'}),
                dcc.Graph(
                    id='pie_chart',
                    figure=pie_plot,
                )
            ],
            width=6
            ),
        ]),
        
    ],
    style={
        'paddingRight':'25px',
        'paddingLeft':'25px'
    })
])

# -- Callback Line Chart Country
@app.callback(
    Output(component_id='line_chart',component_property='figure'),
    Input(component_id='choose_country', component_property='value')
)
def update_plot1(country_list):
    #line_chart = px.line(df[df['country'].isin(country_list)], x="year", y="co2_per_capita", color='country')
    line_chart = px.line(
        df_line[df_line['country'].isin(country_list)], 
        x="year", 
        y="co2_per_capita",
        color='country',
        labels={
            'co2_per_capita': 'CO2 Per Capita (Tonnes)',
            'year' : 'Year',
            'country' : 'Country'
        },
        title='CO2 Trend',
        template='seaborn'
    )

    line_chart.update_layout(hovermode="x")
    line_chart.update_traces(
        hovertemplate= 
        "CO2 Per Capita: %{y:.2f} Tonne"
    )

    return line_chart

# -- Callback Sort Bar Chart
@app.callback(
    Output(component_id='bar_plot',component_property='figure'),
    Input(component_id='bar_sort', component_property='value')
)
def update_plot1(bar_sort):
    if bar_sort:
        bar_plot = px.bar(
            data_frame=df_bar.tail(10),
            y='country',
            x='co2_per_capita',
            title='Top 10 Country with The Highest CO2 Emission per Capita',
            labels={
                'country' : 'Country',
                'co2_per_capita' : 'CO2 Per Capita (Tonnes)'
            },
            template='seaborn'
        )
    else:
        bar_plot = px.bar(
            data_frame=df_bar.head(10),
            y='country',
            x='co2_per_capita',
            title='Top 10 Country with The Lowest CO2 Emission per Capita',
            labels={
                'country' : 'Country',
                'co2_per_capita' : 'CO2 Per Capita (Tonnes)'
            },
            template='seaborn'
        )

    bar_plot.update_traces(
        hovertemplate= 
        "<b>%{y}</b><br><br>"
        "CO2 Per Capita: %{x:.2f} Tonne"
        
    )
    
    return bar_plot

# 3. Start the Dash server
if __name__ == "__main__":
    app.run_server()
