import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import ast
import base64
from copy import deepcopy
from dash.dependencies import Input, Output, State

class GenerateApp():
    """
    Generate the html code of the app
    """
    classes_name_with_psy = ["pas de risque","a risque","psychose"]
    classes_name_without_psy = ["pas de risque","a risque"]
    list_moda = [('label', 'psychose')]  #default list_modalities
    period = 4
    test_size = 0.2
    df_distances = pd.DataFrame()
    counter = 0

    def __init__(self, *args, **kwargs):
        self.app = kwargs.get('app')

        self.html = [
            html.H1(className="app-title", children='Evolution des crypto'),
        ]