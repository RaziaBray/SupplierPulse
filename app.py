import os

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dcc, html

# ==========================================
# 1. APP INITIALISATION & CONFIGURATION
# ==========================================

#fixes scaling issues across bootstrap
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

app = dash.Dash(
    __name__,
    assets_folder=assets_dir,
    external_stylesheets=[dbc.themes.LUX, dbc_css],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1,maximum-scale=1.0, shrink-to-fit=no",
        }
    ],
    external_scripts=[
        {
            "src": 'data:text/javascript,setTimeout(function(){ window.dispatchEvent(new Event("resize")); }, 500);'
        }
    ],
)

server = app.server

# ==========================================
# 2. DATA LOADING & PREPARATION
# ==========================================

df2 = pd.read_excel("supplier pulse data.ods", engine="odf")
df3 = pd.read_excel("supplier pulse monthly data.ods", engine="odf")
df4 = pd.read_excel("supplier pulse annual data.ods", engine="odf")
# ==========================================
# 3. COMPONENT CREATION & STYLING
# ==========================================

# right sidebar
RIGHT_SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "1rem 1rem",
    "background-color": "#d0dfc8",
    "alignItems": "center",
    "overflow-y": "auto",
}

# Main Content Area Styling
CONTENT_STYLE = {
    "margin-left": "1rem",
    "margin-right": "20rem",
    "margin-top": "1rem",
    "padding": "2rem 1rem",
}

header_style = {
    "top":0,
    "background": "linear-gradient(to right, #92b282,#92b282,#d0dfc8, #d0dfc8)",
    "display": "flex",
}

# ==========================================
# 4. APP LAYOUT
# ==========================================

header = dbc.Row(
    [
        dbc.Col(
            # Left: Logo
            children=html.Img(
                src="/assets/Splogo2.png",
                style={"height": "6rem", "width": "19rem", "marginRight": "auto"},
            )
        ),
        # Dropdown
        dbc.Col(
            children=dcc.Dropdown(
                id="supplier-dropdown",
                options=[{"label": k, "value": k} for k in df2["Name"]],
                value=df2["Name"][0],
                clearable=False,
                style={
                    "height": "3rem",
                    "width": "20rem",
                    "padding": "2rem 1rem",
                    "marginLeft": "31rem",
                },
            ),
            className="ms-auto",
        ),
    ],
    className="mb-4",
    style=header_style,
)


sidebar = dbc.Col(
    [
        dbc.Row(className="mb-5"),
        dbc.Row(className="mb-5"),
        dbc.Row(
            [
                dbc.Col(
                    children=dbc.Card(
                        [
                            dbc.CardHeader(
                                "SUPPLIER NEWS",
                                className="fw-bold bg-primary text-white",
                            ),
                            dbc.CardBody(
                                [
                                    html.H5("Press Release", className="card-title"),
                                    html.P(id="Externalnews", className="fs-4"),
                                ]
                            ),
                        ],
                        className="mb-4 shadow-sm",
                    )
                ),
                # Card 2: Confidential Info
                dbc.Col(
                    children=dbc.Card(
                        [
                            dbc.CardHeader(
                                "CONFIDENTIAL INFO",
                                className="fw-bold bg-primary text-white",
                            ),
                            dbc.CardBody(
                                [
                                    html.H5("Internal Status", className="card-title"),
                                    html.P(id="Internalstatus", className="fs-4"),
                                ]
                            ),
                        ],
                        className="mb-4 shadow-sm",
                    )
                ),
                # supplier truth logo
                dbc.Col(
                    children=html.Img(
                        src="/assets/Truth2.png",
                        style={"height": "auto", "width": "20rem"},
                    ),
                    align="left",
                ),
            ],
        ),
    ],
    width=2,
    style=RIGHT_SIDEBAR_STYLE,
)


# main layout content
title_row = dbc.Row(
    [
        dbc.Col(
            children=html.Img(
                src="/assets/factory.png",
                style={"width": "3rem", "height": "3rem", "object-fit": "cover"},
            ),
            width="auto",
            className="pe-2",
        ),
        dbc.Col(
            children=html.H1(
                id="supplier-title",
                className="display-4 text-uppercase tracking-wide mb-3",
            ),
            style={"height": "6rem", "width": "70rem", "padding": "2rem,1rem"},
        ),
    ],
    className="mb-3",
)

subheading_row = dbc.Row(
    [
        dbc.Col(
            children=html.H5([html.Strong("Location: "), html.Span(id="sub-location")]),
            width=7,
            sm=12,
            md=3,
        ),
        dbc.Col(
            children=html.H5(
                [html.Strong("Qualification: "), html.Span(id="sub-qualification")]
            ),
            width=7,
            sm=12,
            md=3,
        ),
        dbc.Col(
            children=html.H5([html.Strong("Type: "), html.Span(id="sub-type")]),
            width=7,
            sm=12,
            md=3,
        ),
        dbc.Col(
            children=html.H5(
                [html.Strong("Business Criticality: "), html.Span(id="sub-criticality")]
            ),
            width=7,
            sm=12,
            md=3,
        ),
    ],
    className="mb-3",
)

# dbc.Row(className="mb-3"), #whitespace

card_row = dbc.Row(
    [
        # Card 1: Materials
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardHeader(
                        "Supplied Materials and Related Product",
                        className="bg-primary text-white text-uppercase font-weight-bold",
                    ),
                    dbc.CardBody(id="card-material"),
                ],
                className="shadow-sm h-100",
            ),
            xs=8,
            sm=6,
            lg=3,
            style={"padding": "0.5rem"},
            className="mb-3",
        ),
        # Card 2: Site Certification
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardHeader(
                        "Site Certifications",
                        className="bg-dark text-white text-uppercase font-weight-bold",
                    ),
                    dbc.CardBody(id="card-certifications"),
                ],
                className="shadow-sm h-100",
            ),
            xs=8,
            sm=6,
            lg=3,
            style={"padding": "0.5rem"},
            className="mb-3",
        ),
        # Card 3: Audit data
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardHeader(
                        "Audit info",
                        className="bg-dark text-white text-uppercase font-weight-bold",
                    ),
                    dbc.CardBody(id="card-audit"),
                ],
                className="shadow-sm h-100",
            ),
            xs=8,
            sm=6,
            lg=4,
            style={"padding": "0.5rem"},
            className="mb-3",
        ),
        # Card 4: ESG Scores
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardHeader(
                        "ESG Rating",
                        className="bg-dark text-white text-uppercase font-weight-bold",
                    ),
                    dbc.CardBody(
                        id="card-esg",
                        className="card-text display-6 text-center py-4 font-weight-bold text-success",
                    ),
                ],
                className="shadow-sm h-100",
            ),
            xs=8,
            sm=4,
            lg=2,
            style={"padding": "0.5rem"},
            className="mb-3",
        ),
    ],
    className="mb-3",
)

chart_row = dbc.Row(
    [
        # quality performance chart
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Spinner(
                                dcc.Graph(
                                    id="bar-quality",
                                    style={"width": "100%", "display": "block"},
                                    config={"responsive": True},
                                ),
                                color="primary",
                                type="border",
                                fullscreen=False,
                            )
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "width": "100%",
                        },
                    )
                ],
                className="shadow-sm mb-4 p-1",
            ),
            style={"flex-shrink": "0", "flex-grow": "1", "min-width": "0"},
            md=4,
            sm=12,
            lg=4,
        ),
        # delivery performance chart
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Spinner(
                                dcc.Graph(
                                    id="line-quantity",
                                    style={"width": "100%", "display": "block"},
                                    config={"responsive": True},
                                ),
                                color="primary",
                                type="border",
                                fullscreen=False,
                            )
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "width": "100%",
                        },
                    )
                ],
                className="shadow-sm mb-4 p-1",
            ),
            style={"flex-shrink": "0", "flex-grow": "1", "min-width": "0"},
            md=4,
            sm=12,
            lg=4,
        ),
        # cost performance chart
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Spinner(
                                dcc.Graph(
                                    id="bar-cost",
                                    style={"width": "100%", "display": "block"},
                                    config={"responsive": True},
                                ),
                                color="primary",
                                type="border",
                                fullscreen=False,
                            )
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "width": "100%",
                        },
                    ),
                ],
                className="shadow-sm mb-4 p-1",
            ),
            style={"flex-shrink": "0", "flex-grow": "1", "min-width": "0"},
            md=4,
            sm=12,
            lg=4,
        ),
    ],
    className="mb-4",
)

table_row = dbc.Row(
    [
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardHeader(
                        html.H2(
                            "Supplier Health Check :",
                            className="fst-italic text-info text-uppercase tracking-wide mb-3",
                        ),
                        style={"height": "4rem", "padding": "1rem,2rem"},
                        className="bg-white",
                    ),
                    dbc.CardBody(id="supplier-table", className="fs-3"),
                ],
                className="shadow-sm mb-4",
            ),
            width=8,
        ),
        dbc.Col(
            children=dbc.Card(
                [
                    dbc.CardHeader(
                        html.H2(
                            [
                                "Supplier Risk Score : ",
                                html.Span(
                                    id="level",
                                    className="fst-italic text-danger text-uppercase tracking-wide mb-3",
                                ),
                            ],
                            className="fst-italic text-info text-uppercase tracking-wide mb-3",
                            style={
                                "height": "4rem",
                            },
                        ),
                        className="bg-white",
                    ),
                    dbc.CardBody(
                        dcc.Graph(id="risk-gauge"),
                        className="d-flex flex-column align-items-right",
                    ),
                ],
                className="shadow-sm mb-4",
            ),
            width=4,
        ),
    ],
    className="mb-4",
)

main_content = dbc.Col(
    [title_row, subheading_row, card_row, chart_row, table_row], width=10
)


app.layout = dbc.Container(
    [
        header,
        dbc.Row([main_content, sidebar]),
    ],
    fluid=True, className="dbc p-0"
)

# ==========================================
# 5. FUNCTIONS & CALLBACKS
# ==========================================


# Callback for Interactivity
@app.callback(
    [
        Output("supplier-title", "children"),
        Output("sub-location", "children"),
        Output("sub-qualification", "children"),
        Output("sub-type", "children"),
        Output("sub-criticality", "children"),
        Output("card-material", "children"),
        Output("card-certifications", "children"),
        Output("card-esg", "children"),
        Output("card-audit", "children"),
        Output("bar-quality", "figure"),
        Output("line-quantity", "figure"),
        Output("bar-cost", "figure"),
        Output("supplier-table", "children"),
        Output("Externalnews", "children"),
        Output("Internalstatus", "children"),
        Output("level", "children"),
        Output("risk-gauge", "figure"),
    ],
    [Input("supplier-dropdown", "value")],
)
def update_dashboard(selected_supplier):

    data2 = df2[df2["Name"] == selected_supplier]
    data3 = df3[df3["Name"] == selected_supplier]
    data4 = df4[df4["Name"] == selected_supplier]

    title = f" {selected_supplier}"

    location = data2["Location"]
    qualification = data2["Qualification"]
    type = data2["Type"]
    criticality = data2["Criticality"]

    # Structure lists into neat HTML bullet elements
    materials_list = html.Ul(
        [html.Li(mat) for mat in data2["Materials"]], className="pl-3"
    )
    certs_list = html.Ul(
        [html.Li(cert) for cert in data2["Certifications"]], className="pl-3"
    )
    audit_list = html.Ul([html.Li(aud) for aud in data2["Auditing"]], className="pl-3")
    esg_list = data2["ESG"]

    # Delivery performance visual
    fig_line = px.bar(
        data3,
        x=["OTIF", "Lead time adherence"],
        y="Month",
        barmode="group",
        orientation="h",
        text_auto="True",
        title="<b>Delivery Performance </b>",
        color_discrete_map={"OTIF": "#5ea4ad", "Lead time adherence": "#c5d9e2"},
    )

    fig_line.update_layout(
        template="plotly_white",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.3,
            "xanchor": "right",
            "x": 0.75,
        },
        xaxis={"automargin": True},
        yaxis={"automargin": True},
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        autosize=True,
    )
    fig_line.add_annotation(
        x=70,
        y="Jan",
        text="Target = 98%",
        showarrow=False,
        ax=50,
        ay=-30,
        font={"size": 12, "color": "white"},
        bgcolor="#ccb2a5",
        bordercolor="#ccb2a5",
        borderwidth=2,
        borderpad=4,
        opacity=0.9,
    )

    # Quality Performance visual
    fig_quality = px.bar(
        data3,
        x="Month",
        y=["INV", "CAPA", "Deviations"],
        barmode="stack",
        text_auto="True",
        title="<b>Quality Performance </b>",
        color_discrete_map={
            "INV": "#a3c7dc",
            "CAPA": "#d0dfc8",
            "Deviations": "#4c5d79",
        },
    )

    fig_quality.update_layout(
        template="plotly_white",
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.3, "xanchor": "right", "x": 0.75},
        xaxis={"automargin": True},
        yaxis={"automargin": True},
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        autosize=True,
    )

    # 3. Procurement Performance (Savings)
    fig_cost = px.bar(
        data4,
        x="Year",
        y=["Annual Savings", "Annual Spend"],
        barmode="overlay",
        text_auto="True",
        title="<b>Cost Saving via Cost Avoidance/Strategic Saving</b>",
        color_discrete_map={"Annual Spend": "#38887b", "Annual Savings": "#374894"},
    )
    fig_cost.add_hline(
        y=(max(data4["Annual Spend"]) + 500000),
        line_dash="dot",
        line_color="#ccb2a5",
        line_width=2,
        annotation_text="Market Average Baseline",
        annotation_position="bottom right",
        annotation_font_color="#ccb2a5",
    )
    fig_cost.update_layout(
        template="plotly_white",
        legend={
            "orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "right", "x": 0.75
        },
        xaxis={"automargin": True},
        yaxis={"automargin": True},
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        autosize=True,
        title={"font": {"size": 14}, "x": 0.02, "xanchor": "left"},
    )

    # Table header
    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th("Open INV's ?", className="fs-5 fw-bold"),
                    html.Th("Open CAPA's ?", className="fs-5 fw-bold"),
                    html.Th("Material returns this month?", className="fs-5 fw-bold"),
                    html.Th("Last 3 deliveries on time?", className="fs-5 fw-bold"),
                    html.Th("Last delivery date:", className="fs-5 fw-bold"),
                    html.Th(
                        "Production stoppages this month:", className="fs-5 fw-bold"
                    ),
                ]
            ),
            className="table-info",
        )
    ]

    # Table body
    table_body = [
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(data2["Open INV"], className="text-center"),
                        html.Td(data2["Open CAPA"], className="text-center"),
                        html.Td(data2["Material returns"], className="text-center"),
                        html.Td(data2["Last deliv on time"], className="text-center"),
                        html.Td(data2["Last deliv date"], className="text-center"),
                        html.Td(data2["Production stoppages"], className="text-center"),
                    ],
                    className="table-secondary",
                )
            ]
        )
    ]

    # Combine table header and body
    table = dbc.Table(
        table_header + table_body,
        bordered=True,
        striped=False,
        hover=False,
        responsive=True,
        className="fs-4",
    )

    # sidebar cards
    externalnews = data2["External news"]
    internalstatus = data2["Internal update"]

    # Risk score title &gauge
    score1 = data2["Risk score"].item()
    level1 = data2["Risk level"]

    # Create the Plotly Gauge Figure
    riskfig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score1,
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "gray"},
                "bgcolor": "white",
                "borderwidth": 1,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 40], "color": "#AFE1AF"},  # Green: Low Risk
                    {"range": [40, 80], "color": "#ffff8a"},  # Yellow: Medium Risk
                    {"range": [80, 100], "color": "#FF8A8A"},  # Red: High Risk
                ],
                "threshold": {
                    "line": {"color": "gray", "width": 6},
                    "thickness": 0.90,
                    "value": score1,
                },
            },
        )
    )
    riskfig.update_layout(margin={"l": 10, "r": 10, "t": 30, "b": 20}, height=180)

    return (
        title,
        location,
        qualification,
        type,
        criticality,
        materials_list,
        certs_list,
        esg_list,
        audit_list,
        fig_quality,
        fig_line,
        fig_cost,
        table,
        externalnews,
        internalstatus,
        level1,
        riskfig,
    )


# ==========================================
# 6. RUN THE SERVER
# ==========================================
if __name__ == "__main__":
    # debug=True allows you to see live error messages in your browser while developing
    app.run(debug=True)
