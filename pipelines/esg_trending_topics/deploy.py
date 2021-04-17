import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chart_studio.plotly as py

def create_plot(dfr, dft):
    """ Create treemap for Trending (="Rising") - dfr - and Top keywords - dft """
    
    assert dfr.columns.str.contains("labels").any(), "dfr does not contain 'labels' columns"
    assert dft.columns.str.contains("labels").any(), "dft does not contain 'labels' columns"
    assert dfr.columns.str.contains("ranking_label").any(), "dfr does not contain 'ranking_label' columns"
    assert dft.columns.str.contains("ranking_label").any(), "dft does not contain 'ranking_label' columns"
    assert dfr.columns.str.contains("value_normalized").any(), "dfr does not contain 'value_normalized' columns"
    assert dft.columns.str.contains("value_normalized").any(), "dft does not contain 'value_normalized' columns"
    
    fig = make_subplots(2, 1, specs=[[{"type": "domain"}], [ {"type": "domain"}]])

    fig.add_trace(go.Treemap(
        labels = dfr['labels'], #_href
        parents = dfr.ranking_label, 
        values = dfr.value_normalized, 
    ), 1, 1)

    fig.add_trace(go.Treemap(
        labels = dft['labels'],
        parents = dft.ranking_label, 
        values = dft.value_normalized
    ), 2, 1)

    fig.update_layout(margin=dict(t=10, b=10, r=10, l=10), 
                      plot_bgcolor= "rgba(0, 0, 0, 0)",
                      paper_bgcolor= "rgba(0, 0, 0, 0)",
                     )

    fig.update_traces(
        opacity=1, 
        textposition='middle center', 
        textfont={'family':"Arial", 'size': 20}, 
        hoverinfo= "label", # "skip",
        tiling = {'squarifyratio': 1, 'pad': 0}, 
        textfont_size=24, 
        marker={
            'depthfade': True,
            'cauto': True,
        }
    )
    
    return fig

def create_plot_rising(dfr):
    """ Create treemap for Trending (="Rising") - dfr - keywords """
    
    assert dfr.columns.str.contains("labels").any(), "dfr does not contain 'labels' columns"
    assert dfr.columns.str.contains("ranking_label").any(), "dfr does not contain 'ranking_label' columns"
    assert dfr.columns.str.contains("value_normalized").any(), "dfr does not contain 'value_normalized' columns"
    
    fig = make_subplots(1, 1, specs=[[{"type": "domain"}]])

    fig.add_trace(go.Treemap(
        labels = dfr['labels'], #_href
        parents = dfr.ranking_label, 
        values = dfr.value_normalized, 
    ), 1, 1)

    fig.update_layout(margin=dict(t=10, b=10, r=10, l=10), 
                      plot_bgcolor= "rgba(0, 0, 0, 0)",
                      paper_bgcolor= "rgba(0, 0, 0, 0)",
                     )

    fig.update_traces(
        opacity=1, 
        textposition='middle center', 
        textfont={'family':"Arial", 'size': 20}, 
        hoverinfo= "label", # "skip",
        tiling = {'squarifyratio': 1, 'pad': 0}, 
        textfont_size=24, 
        marker={
            'depthfade': True,
            'cauto': True,
        }
    )
    
    return fig

def deploy_plot(figure, filename):    
    """ Upload graph to chartstudio """
    print(f"Upload {filename} figure to plotly")
    py.plot(figure, filename=filename)


