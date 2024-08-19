import dash
from dash import html, dcc, Input, Output, State  # Ensure all necessary imports are included
from app import app
from app.data_fetcher import load_and_filter_stock_data

@app.callback(
    [Output('graph', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [State('input-symbol', 'value')]
)
def update_graph(n_clicks, symbol):
    if n_clicks is None or not symbol:
        return [{}]  # Return an empty graph if no input is provided

    # Load and filter stock data for the given symbol
    filtered_data = load_and_filter_stock_data(symbol)

    # Create the figure for the graph
    figure = {
        'data': [{
            'x': filtered_data['date'],
            'y': filtered_data['close'],
            'type': 'line',
            'name': symbol
        }],
        'layout': {
            'title': f'Stock Data for {symbol}',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price'},
            'plot_bgcolor': '#f8f8f8',
            'paper_bgcolor': '#f8f8f8',
            'margin': {'l': 40, 'r': 20, 't': 40, 'b': 40},
        }
    }
    
    return [figure]

@app.callback(
    [Output('tab-content', 'children'),
     Output('home-tab', 'className'),
     Output('stock-data-tab', 'className')],
    [Input('home-tab', 'n_clicks'),
     Input('stock-data-tab', 'n_clicks')]
)
def render_content(home_clicks, stock_data_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return html.Div(), "is-active", ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'home-tab':
        return (
            html.Div([
                html.H2("Welcome to the Home Page", className="subtitle has-text-centered"),
                html.P("This is the home page content.", className="has-text-centered"),
            ]),
            "is-active", ""
        )
    elif button_id == 'stock-data-tab':
        return (
            html.Div([
                html.Div(className="field has-addons has-text-centered", children=[
                    html.Div(className="control", children=[
                        dcc.Input(id='input-symbol', type='text', placeholder='Enter stock symbol', className='input')
                    ]),
                    html.Div(className="control", children=[
                        html.Button('Submit', id='submit-button', n_clicks=0, className='button is-primary')
                    ]),
                ], style={'justify-content': 'center', 'padding': '20px'}),
                dcc.Graph(id='graph')
            ]),
            "", "is-active"
        )
