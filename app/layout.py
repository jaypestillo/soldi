from dash import dcc, html

# Link to Bulma CSS
bulma_css = "https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css"

layout = html.Div([
    html.Link(href=bulma_css, rel="stylesheet"),
    html.H1("Stock Data Dashboard", className="title has-text-centered", style={'padding': '20px'}),

    # Navigation bar with two tabs
    html.Div(className="tabs is-centered", children=[
        html.Ul([
            html.Li(html.A("Home", href="#", id="home-tab", className="is-active", n_clicks=0)),
            html.Li(html.A("Stock Data", href="#", id="stock-data-tab", n_clicks=0)),
        ])
    ]),

    # Content will be rendered here based on selected tab
    html.Div(id='tab-content', style={'padding': '20px'})
])
