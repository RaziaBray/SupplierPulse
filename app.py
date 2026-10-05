import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

# ==========================================
# 1. APP INITIALISATION & CONFIGURATION
# ==========================================

# We use 'os' to make sure Dash always finds your 'assets' folder perfectly, 
# even when deployed onto a cloud server later!
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

app = dash.Dash(
    __name__,
    assets_folder=assets_dir,
    external_stylesheets=[dbc.themes.LUX]  # If you used a specific theme like CERULEAN or DARKLY, change BOOTSTRAP to that!
)

# This exposes the underlying Flask server, which production web hosts require to run your app
server = app.server 

# ==========================================
# 2. DATA LOADING & PREPARATION
# ==========================================
# PASTE YOUR DATA LOADING CODE HERE! For example:
df2= pd.read_excel("supplier pulse data.ods", engine="odf")
df3= pd.read_excel("supplier pulse monthly data.ods", engine="odf")
df4= pd.read_excel("supplier pulse annual data.ods", engine="odf")
# ==========================================
# 3. COMPONENT CREATION & STYLING
# ==========================================

#right sidebar
RIGHT_SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "1rem 1rem",
    "background-color": "#d0dfc8",
    "alignItems":"center",
    #"border-left": "1px solid #f4f6ef",
    "overflow-y": "auto",
        #"position": "fixed",
        #"top": 0,
        #"right": 0,
        #"bottom": 0,
        #"width": "15rem",
        #"padding": "2rem 1rem",
        #"backgroundColor": "#f8f9fa",
        #"borderRight": "1px solid #e9ecef"
}

# Main Content Area Styling
CONTENT_STYLE = {
    "margin-left": "10px",
    "margin-right":"220px",
    "margin-top":"15px",
    "padding": "2rem 1rem",
}

# ==========================================
# 4. APP LAYOUT
# ==========================================


header1 =html.Div(
            [
                # Left: Logo
                html.Img(
                    src="/assets/splogo2.png",
                    style={"height": "90px", "width":"300px", "marginRight": "auto"},),
                 #html.H2("Supplier Pulse", className="text-dark mb-4",style={"height": "40px", "marginLeft": "10px"},),
                # Center: Dropdown
                html.Div(
                    dcc.Dropdown(
                        id="supplier-dropdown",
                        options=[{"label": k, "value": k} for k in df2["Name"]],
                        #value=list(SUPPLIER_DATA.keys())[0],
                        value=df2["Name"][0],
                        clearable=False,
                        #),
                    style={"Display":"flex","height": "80px","width": "300px","marginRight":"350px","padding": "2rem 1rem",},),  # Adjust width as needed
                ),
                # Right: Empty placeholder to balance the flex space on the right
                #html.Div(style={"width": "40px", "marginLeft": "auto"}),
                ],
            style={
                "background": "linear-gradient(to right, #92b282,#92b282,#d0dfc8, #d0dfc8)",
                "display": "flex",
               # "alignItems":"right",
               # "justifyContent": "space-between",
                #"padding": "10px"20px",
                #"backgroundColor": "#92b282",
                #"borderBottom": "1px solid #d0dfc8",
            },
        )

# Main Content Component
main_content = html.Div([
    dbc.Container([
        dbc.Row(
                [
                dbc.Col(html.Img(src="/assets/factory.png",style={"width": "40px", "height": "50px", "object-fit": "cover"}),
                       width="auto",className="pe-2",),
                dbc.Col(html.H1(id="supplier-title", className="display-4 text-uppercase tracking-wide mb-3",),
                        style={"height":"100px","width":"150","padding":"1rem,2rem"},
                               
                       ),                    
                       
                ],className="align-items-left g-0"),
                ],style={"display":"flex","marginLeft":"10px", "width":"100%",}),

                
            dbc.Row(           
                [
                    dbc.Col(html.H5([html.Strong("Location: "), html.Span(id="sub-location")]),width=7, sm=12, md=3 ),
                    dbc.Col(html.H5([html.Strong("Qualification: "), html.Span(id="sub-qualification")]), width=5, sm=12, md=3),
                    dbc.Col(html.H5([html.Strong("Type: "), html.Span(id="sub-type")]), width=5, sm=12, md=3),
                    dbc.Col(html.H5([html.Strong("Business Criticality: "), html.Span(id="sub-criticality")]), width=5, sm=12, md=3),
                    
                ],className="text-emphasis"
                ),
        dbc.Row(className="mb-3"),
        
# Main Layout-Cards
        dbc.Row(
            [
                # Card 1: Materials
                dbc.Col(
                    dbc.Card(
                        [dbc.CardHeader("Supplied Materials and Related Product", className="bg-primary text-white text-uppercase font-weight-bold"),
                        dbc.CardBody(id="card-material")],className="shadow-sm h-100"),width=5, lg=3, className="mb-4"),
                
                # Card 2: Site Certification
                dbc.Col(
                    dbc.Card(
                        [dbc.CardHeader("Site Certifications", className="bg-dark text-white text-uppercase font-weight-bold"),
                        dbc.CardBody(id="card-certifications")],className="shadow-sm h-100"),width=5, lg=3, className="mb-4"),
               
                # Card 3: Audit data
                dbc.Col(
                    dbc.Card(
                        [dbc.CardHeader("Audit info", className="bg-dark text-white text-uppercase font-weight-bold"),
                        dbc.CardBody(id="card-audit")],className="shadow-sm h-100"),width=5, lg=3, className="mb-4"),
                
                # Card 4: ESG Scores
                dbc.Col(
                    dbc.Card(
                        [dbc.CardHeader("ESG Rating", className="bg-dark text-white text-uppercase font-weight-bold"),
                        dbc.CardBody(id="card-esg", className="card-text display-6 text-left py-4 font-weight-bold text-success")],
                        className="shadow-sm h-100"),width=5, lg=2, className="mb-4"),
               
                ]
            ),
        
# main layout -charts Row

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([dcc.Graph(id="bar-quality")])], className="shadow-sm mb-4"), width=4),
            dbc.Col(dbc.Card([dbc.CardBody([dcc.Graph(id="line-quantity")])], className="shadow-sm mb-4"), width=4),
            dbc.Col(dbc.Card([dbc.CardBody([dcc.Graph(id="bar-cost")])], className="shadow-sm mb-5"), width=4),
                ]),
        dbc.Row(className="mb-3"), #to create white space in layout
    
#main layout -heading and table for next section
    
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H1("Supplier Health Check :", className="fst-italic text-info text-uppercase tracking-wide mb-3",),
                                style={"height":"70px","width":"80","padding":"1rem,2rem"}, className="bg-white"),
                    dbc.CardBody(id="supplier-table", className="fs-3")
                        ], className="shadow-sm mb-4"),width=7
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.H1(["Supplier Risk Score : ", html.Span(id="level", className="fst-italic text-danger text-uppercase tracking-wide mb-3")], className="fst-italic text-info text-uppercase tracking-wide mb-3",
                        style={"height":"70px","width":"60"},),className="bg-white"),
                        #html.Span(id="level", className="fst-italic text-primary text-uppercase mb-3"),
                    dbc.CardBody(dcc.Graph(id="risk-gauge"), className= "d-flex flex-column align-items-left"),
                        
                ], className="shadow-sm mb-4"), width=4  
            ),
        ])
            ], style=CONTENT_STYLE)

#right sidebar
right_sidebar = html.Div(
    [
        dbc.Row(className="mb-5"),
        dbc.Row(className="mb-4"),

        #card 1: external news
        dbc.Card(
            [
                dbc.CardHeader("SUPPLIER NEWS", className="fw-bold bg-primary text-white"),
                dbc.CardBody(
                    [
                        html.H5("Press Release", className="card-title"),
                        html.P(id= "Externalnews", className="fs-4"),
                    ]
                ),
            ],
            className="mb-4 shadow-sm",
            ),
        
        # Card 2: Confidential Info
        dbc.Card(
            [
                dbc.CardHeader("CONFIDENTIAL INFO", className="fw-bold bg-primary text-white"),
                dbc.CardBody(
                    [
                        html.H5("Internal Status", className="card-title"),
                        html.P(id="Internalstatus", className="fs-4"),
                        #
                    ]
                ),
            ],
            className="mb-4 shadow-sm",
            ),
        html.Img(src="/assets/TRUTH2.png",
                    style={"height": "300px", "width":"300px", "marginLeft": "5%"},),
        
        
    ],style=RIGHT_SIDEBAR_STYLE, className="d-flex flex-column justify-content-bottom")
        

# Combine elements into master structure
app.layout = html.Div([header1, main_content, right_sidebar])



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
        Output("risk-gauge", "figure")
    ],
    [Input("supplier-dropdown", "value")]
)
def update_dashboard(selected_supplier):
    #dff = df[df["Supplier"] == selected_supplier]
    #data1 = df1[selected_supplier]
    #df1 = pd.DataFrame(SUPPLIER_DATA)
    #data1 = df1[selected_supplier]
    
    data2 = df2[df2["Name"]==selected_supplier]
    data3 = df3[df3["Name"]==selected_supplier]
    data4 = df4[df4["Name"]==selected_supplier]

    
    title = f" {selected_supplier}"
    
    
     # Structure lists into neat HTML bullet elements
    materials_list = html.Ul([html.Li(mat) for mat in data2["Materials"]], className="pl-3")
    

    
    
    certs_list = html.Ul([html.Li(cert) for cert in data2["Certifications"]], className="pl-3")
    audit_list = html.Ul([html.Li(aud) for aud in data2["Auditing"]], className="pl-3")
    
    # Delivery performance visual
    fig_line = px.bar(data3,x=["OTIF", "Lead time adherence"], y="Month", barmode='group', orientation="h", text_auto="True", title="<b>Delivery Performance </b>",
                      color_discrete_map={
                            "OTIF": "#5ea4ad",
                            "Lead time adherence": "#c5d9e2"})
   
    
    fig_line.update_layout(template="plotly_white", 
                          legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=0.75))
    fig_line.add_annotation(
    x=70,                  # Position on the X-axis (numeric value)
    y="Jan",             # Position on the Y-axis (categorical label)
    text="Target = 98%", # The note content
    #textangle=-90,
    showarrow=False,        # Set to True to point an arrow at the target coordinate
    #arrowhead=2,           # Arrow style (1-7)
    ax=50,                 # X offset for the text box (pixels right)
    ay=-30,                # Y offset for the text box (pixels up)
    font=dict(size=12, color="white"),
    bgcolor="#ccb2a5",     # Bootstrap primary blue background
    bordercolor="#ccb2a5",
    borderwidth=2,
    borderpad=4,
    opacity=0.9)

    
    # Quality Performance visual
    fig_quality = px.bar(data3, x="Month", y=["INV","CAPA","Deviations"], barmode="stack", text_auto="True", title="<b>Quality Performance </b>", 
                          color_discrete_map={
                            "INV": "#a3c7dc",
                            "CAPA": "#d0dfc8",
                          "Deviations":"#4c5d79" })
    
    #fig_quality.update_yaxes(range=[-1, 6]),
    fig_quality.update_layout(template="plotly_white",
                             legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1.08)
                             )
    
    # 3. Procurement Performance (Savings)
    fig_cost = px.bar(data4, x="Year", y=["Annual Savings", "Annual Spend"],barmode="overlay", text_auto="True", title="<b>Cost Saving via Cost Avoidance/Strategic Saving</b>",
                      color_discrete_map={
                          "Annual Spend": "#38887b",
                          "Annual Savings":"#374894"})
    fig_cost.add_hline(
    y=(max(data4["Annual Spend"]) + 500000),  # The target value on the Y-axis
    line_dash="dot",                     # Style options: 'dash', 'dot', 'dashdot', or 'solid'
    line_color="#ccb2a5",                 # Eye-catching color (e.g., Crimson Red)
    line_width=2,                         # Thickness of the line
    annotation_text="Market Average Baseline",     # Text label for the line
    annotation_position="bottom right",      # Positions: 'top left', 'top right', 'bottom left', 'bottom right'
    annotation_font_color="#ccb2a5"       # Match text color with the line color
)
    fig_cost.update_layout(template="plotly_white",
                          legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.04,
                                xanchor="right",
                                x=0.75))
    
    # 4. Table
    #table=data1.to_dict("records")
    
    # Build the Bootstrap Table header
    table_header = [
        html.Thead(html.Tr([
            html.Th("Open INV's ?",className="fs-5 fw-bold"),
            html.Th("Open CAPA's ?",className="fs-5 fw-bold"),
            html.Th("Material returns this month?",className="fs-5 fw-bold"),
            html.Th("Last 3 deliveries on time?",className="fs-5 fw-bold"),
            html.Th("Last delivery date:",className="fs-5 fw-bold"),
            html.Th("Production stoppages this month:",className="fs-5 fw-bold")
        ]), className="table-info",)
    ]
    
    # Build the Bootstrap Table body by iterating over rows
    table_body = [
        html.Tbody([
            html.Tr([
                html.Td(data2["Open INV"], className="text-center"),
                html.Td(data2["Open CAPA"], className="text-center"),
                html.Td(data2["Material returns"], className="text-center"),
                html.Td(data2["Last deliv on time"], className="text-center"),
                html.Td(data2["Last deliv date"], className="text-center"),
                html.Td(data2["Production stoppages"], className="text-center")
            ],className="table-secondary",) 
        ])
    ]
    
    # Combine into a responsive Dash Bootstrap Table
    table= dbc.Table(
        table_header + table_body,
        bordered=True,
        striped=False,
        hover=False,
        #color="primary",
        responsive=True,
        className= "fs-4",
        #style={"border": "2px solid #ff5733",},
        
    )
    
    #sidebar cards
    externalnews= data2["External news"]
    internalstatus= data2["Internal update"]
    
    
    # Risk score title &gauge
    #supplier_info = data2.get(selected_supplier, {"Risk score": 0, "Risk level": "Unknown"})
    score1=data2["Risk score"].item()
    level1=data2["Risk level"]
    #score1 = supplier_info["Risk score"]
    #level1 = supplier_info["Risk level"]
    
    # Create the Plotly Gauge Figure
    riskfig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score1,
        #title={'text': f"Risk Score: {level1}", 'font': {'size': 24}},
        gauge={
            'axis': {'range':[0,100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "gray"}, # The needle/pointer color representation
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "gray",
            'steps': [
                {'range':[0,40], 'color': '#AFE1AF'},   # Green: Low Risk
                {'range':[40,80], 'color': '#ffff8a'},  # Yellow: Medium Risk
                {'range':[80,100], 'color': '#FF8A8A'}  # Red: High Risk
                ],
            "threshold": {
                "line": {"color": "gray", "width": 6},
                "thickness": 0.90,
                "value":score1,
            },
            }
        ))
    riskfig.update_layout(margin=dict(l=10, r=10, t=30, b=20),height=180)
    
    
    
    return title,data2["Location"],data2["Qualification"],data2["Type"], data2["Criticality"], materials_list, certs_list,data2["ESG"], audit_list, fig_quality,fig_line, fig_cost,table,externalnews, internalstatus, level1, riskfig










# ==========================================
# 6. RUN THE SERVER
# ==========================================
if __name__ == '__main__':
    # debug=True allows you to see live error messages in your browser while developing
    app.run(debug=True)