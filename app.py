from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json

BARRA_LATERAL_SHINY = {
    "min-height": "20px",
    "padding": "19px",
    "margin-bottom": "20px",
    "background-color": "#f5f5f5",
    "border": "1px solid #e3e3e3",
    "border-radius": "4px",
    "-webkit-box-shadow": "inset 0 1px 1px rgb(0 0 0 / 5%)",
    "box-shadow": "inset 0 1px 1px rgb(0 0 0 / 5%)",
}

with open("./boston-housing-meta.json", "r") as json_file:
    boston_housing_metadata = json.load(json_file)

data_url = "https://raw.githubusercontent.com/scikit-learn/scikit-learn/0d378913be6d7e485b792ea36e9268be31ed52d0/sklearn/datasets/data/boston_house_prices.csv"
boston_housing = pd.read_csv(data_url, skiprows=2)
boston_housing.columns = boston_housing_metadata.keys()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

barra_lateral = html.Div(
    [
        html.H3("Variáveis"),
        dcc.Dropdown(
            id="variavel",
            options=[
                {"label": column, "value": column} for column in boston_housing.columns
            ],
        ),
        dcc.Graph(id="graficoResumo"),
        html.H4("Estrutura"),
        html.P(id="estrutura"),
        html.H4("Sobre"),
        html.P(id="sobre"),
    ],
    className="col-sm-3",
    style=BARRA_LATERAL_SHINY,
)

principal = html.Div(
    [
        html.H3("Relação com MEDV"),
        dcc.Graph(id="graficoRegressao"),
        html.Div(
            [
                html.H3("Mapa de Densidade"),
                dcc.Dropdown(
                    id="variavelMapa",
                    options=[
                        {"label": column, "value": column}
                        for column in boston_housing.columns
                    ],
                ),
            ],
            className="row"
        ),
        dcc.Graph(id="mapaDensidade")
    ],
    className="col-sm-8",
)

titulo = html.H1("Boston Housing - Painel criado com Dash", className="row")
painel = html.Div([barra_lateral, principal], className="row")
app.layout = html.Div([titulo, painel], style={"padding-left": "10px", "height": "100vh"})
server = app.server

@app.callback(
    Output("graficoResumo", "figure"),
    Output("estrutura", "children"),
    Output("sobre", "children"),
    Output("graficoRegressao", "figure"),
    Input("variavel", "value"),
)
def atualizar(variavel):
    if variavel is None:
        raise PreventUpdate
    if(variavel == "chas"):
        contagem = boston_housing[variavel].value_counts()
        graficoResumo = px.pie(names=contagem.index, values=contagem.values)
    else:
        graficoResumo = px.box(boston_housing, y=variavel)
    estrutura = str(boston_housing[variavel].dtype)
    sobre = boston_housing_metadata[variavel]
    graficoRegressao = px.scatter(boston_housing, x=variavel, y="medv", trendline="ols")
    return graficoResumo, estrutura, sobre, graficoRegressao

@app.callback(
    Output("mapaDensidade", "figure"),
    Input("variavelMapa", "value"),
    Input("variavel", "value"),
)
def atualizar(variavelMapa, variavel):
    if variavel is None or variavelMapa is None:
        raise PreventUpdate
    mapaDensidade = px.density_heatmap(boston_housing, x=variavel, y=variavelMapa)
    return mapaDensidade

if __name__ == "__main__":
    app.run_server(debug=True)
