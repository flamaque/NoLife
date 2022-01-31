import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
#import chart_studio.plotly as py
import plotly.graph_objs as go
import io
from base64 import b64encode

buffer = io.StringIO()

# Styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialise the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Load data

sf = pd.read_csv('CO2Meting.csv')
af = pd.read_csv('Test_AlleWaarden.csv')

available_indicators = af['Waarde'].unique()

# Draw graph CO2
fig = px.line(sf, x='Date', y=['CO2PWM', 'CO2Analog'], title='CO2 Meting')
fig.layout = dict(
    title='CO2',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="minute",
                     stepmode="backward"),
                dict(count=5,
                     label="5m",
                     step="minute",
                     stepmode="backward"),
                dict(count=1,
                     label="1h",
                     step="hour",
                     stepmode="backward"),
                dict(count=12,
                     label="12h",
                     step="hour",
                     stepmode="backward"),
                dict(count=1,
                     label="1day",
                     step="day",
                     stepmode="backward"),
                dict(step='all')
            ])
        ))
)
fig.update_yaxes(
    # tickvals=[350, 400, 450, 500, 550, 600, 650],
    dtick=25,
    nticks=7,
    title_text='CO2 (PPM)',
    title_font={"size": 15},
    title_standoff=25)

fig.update_xaxes(
    nticks=20,
    tickangle=30,
    title_text='Time',
    title_font={"size": 15},
    title_standoff=15
)
fig.update_xaxes(type='date')

# Draw graph Alles
fig2 = px.line(af, x='Date',
               y=['CO2PWM', 'CO2Analog', 'Hartslag', 'Ademhaling', 'CO', 'Aanwezigheid'],
               title='Alle waarden')
fig2.layout = dict(
    title='Alle waarden',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="minute",
                     stepmode="backward"),
                dict(count=5,
                     label="5m",
                     step="minute",
                     stepmode="backward"),
                dict(count=1,
                     label="1h",
                     step="hour",
                     stepmode="backward"),
                dict(count=12,
                     label="12h",
                     step="hour",
                     stepmode="backward"),
                dict(count=1,
                     label="1day",
                     step="day",
                     stepmode="backward"),
                dict(step='all')
            ])
        ))
)
fig2.update_xaxes(
    nticks=20,
    tickangle=30,
    title_text='Time',
    title_font={"size": 15},
    title_standoff=15
)
fig2.update_xaxes(type='date')

fig.write_html(buffer)
fig2.write_html(buffer)
html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()


# Creates a list of dictionaries, which have the keys 'label' and 'value'.
def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


# Define the app
app.layout = html.Div(children=[
    html.Div(children=[
        html.H2('No-Life Data'),
        html.P('''CO2[PWM/Analog], CO, Ademhaling, Aanwezigheid, Hartslag'''),
    ]),
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='four columns div-user-controls'),  # Define the left element
                 html.Div(className='eight columns div-for-charts bg-grey')  # Define the right element
             ]),
    html.Div(dcc.Graph(
        id='example-graph',
        figure=fig
    )),

    html.Div(dcc.Graph(
        id='example-graph2',
        figure=fig2
    )
    ),
    html.A(
        html.Button("Download HTML"),
        id="download",
        href="data:text/html;base64," + encoded,
        download="plotly_graph.html"
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
