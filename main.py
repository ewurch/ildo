from fasthtml import FastHTML
import fasthtml.common as html
import pandas as pd

css = html.Style(':root { --pico-font-size: 100%; --pico-font-family: sans-serif;}')
picolink = html.Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")

app = FastHTML(hdrs=(picolink, css))


@app.get("/")
def home():
    return html.Div(
        html.Br(),
        html.H1('Inth - A simple web app for data analysis'), 
        html.P('Upload your dataset to get started'), 
        html.Input(type='file', name='file'),
        cls='container'
    )


def load_data(file):
    return pd.read_csv(file)
