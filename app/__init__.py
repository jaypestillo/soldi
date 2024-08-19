from dash import Dash
import dash_bootstrap_components as dbc
from flask import Flask

server = Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

from app import layout, callbacks

app.layout = layout.layout
app.config.suppress_callback_exceptions = True
