import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from scout_apm.flask import ScoutApm

external_stylesheets = [ dbc.themes.BOOTSTRAP, 'https://codepen.io/almostburtmacklin/pen/QWWKEJb.css']




app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
flask = app.server
ScoutApm(flask)
flask.config["SCOUT_NAME"] = "Baseball App"
