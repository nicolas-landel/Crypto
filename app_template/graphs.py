import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import offline
import plotly.express as px


class dataGraph():

    def __init__(self):
        raw_df = pd.read_csv("data.csv")
        self.df = raw_df.set_index("time")

    def time_graph(self):
        '''
        This function creates a graph of the data evolution over time, 
        in the range start_time - end_time.
        :param start_time:
        :param end_time:
        '''
        data_by_currency = []
        for i, col in enumerate(self.df.columns):
            data_by_currency.append(
                go.Scatter(
                    x = self.df.index,
                    y = self.df[col],
                    mode = 'lines',
                    name = col,
                 )
            )
        layout = go.Layout(
            title = "Currency value over time",
            xaxis = dict(
                title = "time",
                tickmode = 'linear',
                tick0 = 0.5,
                dtick= 10,
            ),
            yaxis = dict(
                title = "Value (EUR)",
            ),
            
        )
        fig = go.Figure(data=data_by_currency, layout=layout)
        return fig
