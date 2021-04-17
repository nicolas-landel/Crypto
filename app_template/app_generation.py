import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import ast
import base64
from copy import deepcopy
from dash.dependencies import Input, Output, State
from .graphs import dataGraph


class GenerateApp():
    """
    Generate the html code of the app
    """

    def __init__(self, *args, **kwargs):
        self.app = kwargs.get('app')
        graph = dataGraph()
        self.fig = graph.time_graph()
        self.html = [
            html.H1(className="app-title", children='Evolution des crypto'),
            dcc.Graph(figure=self.fig)
        ]