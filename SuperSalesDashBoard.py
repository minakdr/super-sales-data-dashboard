import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from scipy.stats import linregress

df = pd.read_csv(r"D:\Projects\Dashboard\SuperSalesStore\cleanSalesData.csv")

total_sales = df['Sales'].sum()

fig_totalSalesIndicator = go.Figure(go.Indicator(
    mode="gauge+number",
    value=total_sales,
    number={
        'valueformat': ',.0f',
        'font': {'size': 25}  # Adjust text size in the middle
    },
    gauge={
        'axis': {'range': [0, 2.5e6]},  # Set range of the gauge
        'bar': {'color': '#0052ef'},  # Set bar color to your shade of blue
        'steps': [],  # Remove background bands
        'threshold': None  # Remove the red threshold line
    },
    domain={'x': [0, 1], 'y': [0, 1]}
))

fig_totalSalesIndicator.update_layout(
    title="Total Sales",
    height=400,  # Adjust height as needed
    margin=dict(l=50, r=50, t=50, b=50)
)


total_profit = df['Profit'].sum()


fig_total_profitIndicator = go.Figure(go.Indicator(
    mode="gauge+number",
    value=total_profit,  # Current value (total profit)
      number={
        'prefix': "$", 
        'valueformat': ',.0f',
        'font': {'size': 25}  # Adjust text size in the middle
    },
    gauge={
        'axis': {
            'range': [0, 750000],  # Set range of the gauge from 0 to 750k
            'tickvals': [0, 250000, 500000, 750000],  # Define tick positions at 0, 250k, 500k, and 750k
            'ticktext': ['$0', '$250k', '$500k', '$750k'],  # Add labels for tick positions
        },
        'bar': {'color': "#594bf2"},  
        'steps': [],  # Remove background color bands
        'threshold': None  # Remove the red threshold line
    },
    domain={'x': [0, 1], 'y': [0, 1]}
))

fig_total_profitIndicator.update_layout(
    title="Total Profit",
    height=400,  # Adjust height as needed
    margin=dict(l=50, r=50, t=50, b=50)  # Optional: Adjust margins to center the indicator card
)





total_quantity = df['Quantity'].sum()


fig_total_quantityIndicator = go.Figure(go.Indicator(
    mode="number",
    value=total_quantity,  
    number={'valueformat': ',.0f'}, 
    domain={'x': [0, 1], 'y': [0, 1]}
))


fig_total_quantityIndicator.update_layout(
    paper_bgcolor="lightgray",
    title="Total Quantity",
    height=150, 
    width=250,   
    margin=dict(t=40, b=40, l=40, r=40) 

    
)








total_customers = df['Type_of_customer'].count()

fig_TypeOfCustomers = {
    'data': [
        go.Pie(
            labels=df['Type_of_customer'].unique(),
            values=df['Type_of_customer'].value_counts(),
            textinfo='label',  
            textposition='outside',  # Position the text outside of the graph
            hole=0.5, 
            opacity=0.9,
            marker=dict(
                colors=[
                    '#28b8ff',  
                    '#0052ef',  
                    '#5462ff'
                ]
            ),
            outsidetextfont={'size': 16, 'color': '#222222'}  # Larger and darker text outside the pie
            
        )
    ],
    'layout': go.Layout(
        title='Distribution of Customer Types',
        showlegend=False,
        hovermode='closest',
        annotations=[  
            {
                'text': f'total: {total_customers}',
                'x': 0.5,
                'y': 0.5,
                'font': {'size': 18, 'color': '#222222'},
                'showarrow': False
            }
        ]
    )
}







ship_mode_counts = df['Ship Mode'].value_counts().reset_index()
ship_mode_counts.columns = ['Ship Mode', 'Count']


fig_ShipModeTreemap = go.Figure(
    data=[go.Treemap(
        labels=ship_mode_counts['Ship Mode'], 
        parents=[''] * len(ship_mode_counts),  # Root has no parent
        root_color="lightgrey",
        values=ship_mode_counts['Count'],  
        textinfo='label+value',  
        marker=dict(
            colors=ship_mode_counts['Count'],  
            colorscale=[
                [0, '#0052ef'],  # Starting color (blue)
                [1, '#9224ff']   # Ending color (purple)
            ],  # Custom gradient from blue to purple
            showscale=True  # Display color scale
        )
    )],
    layout=go.Layout(
        title='Distribution of Ship Modes',
        showlegend=False,
        hovermode='closest',
        margin=dict(t=50, b=50, l=50, r=50),
        paper_bgcolor='white',  # Clean background
        plot_bgcolor='white',   # Plot area background
        font=dict(size=12),  # Font size for text
        xaxis=dict(showgrid=False, zeroline=False),  # Hide gridlines for x-axis
        yaxis=dict(showgrid=False, zeroline=False)   # Hide gridlines for y-axis
    )
)






state_sales = df.groupby('State')['Sales'].sum().reset_index().round(0)
state_sales = state_sales.sort_values(by='Sales', ascending=False)

# Map of full state names to abbreviations for the choropleth map
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
    'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}
df['State_Abbrev'] = df['State'].map(state_abbrev)

state_sales_map = df.groupby('State_Abbrev')['Sales'].sum().reset_index().round(0)
fig_SalesByStateMap = go.Figure(data=go.Choropleth(
    locations=state_sales_map['State_Abbrev'],
    z=state_sales_map['Sales'],
    locationmode='USA-states',
    colorscale='Blues',
    colorbar_title="Total Sales"
))

fig_SalesByStateMap.update_layout(
    title_text='Total Sales by State in the USA',
    geo=dict(scope='usa')
)


















































color_map = {
    'South': '#9224ff',  # Purple 
    'West': '#201cfb',   # Dark Blue
    'Central': '#205cf4', # Lighter Blue 
    'East': '#5f28fd'    # Violet
}


fig_sun = px.sunburst(df, 
                      path=['Region', 'State'], 
                      color='Region',  # Color by Region
                      color_discrete_map=color_map,  # Custom color map
                      title="Region vs State Sunburst Chart")











































fig_discount = px.scatter(
    df,
    x='Discount',
    y='Sales',
    title='Correlation Between Discount and Sales',
    labels={'Discount': 'Discount (%)', 'Sales': 'Sales '},
    template='plotly_white'
)

# Add customization
fig_discount .update_traces(marker=dict(size=10, color='blue', opacity=0.7))
fig_discount .update_layout(
    xaxis=dict(title='Discount (%)'),
    yaxis=dict(title='Sales '),
    title=dict(x=0.5),  # Center the title
    margin=dict(l=20, r=20, t=40, b=20)  # Adjust margins
)




















fig_discount_quantity = px.scatter(
    df,
    x='Discount',
    y='Quantity',
    title='Correlation Between Discount and Quantity',
    labels={'Discount': 'Discount (%)', 'Quantity': 'Quantity '},
    template='plotly_white'
)

# Add customization
fig_discount_quantity .update_traces(marker=dict(size=10, color='blue', opacity=0.7))
fig_discount_quantity .update_layout(
    xaxis=dict(title='Discount (%)'),
    yaxis=dict(title='Quantity '),
    title=dict(x=0.5),  # Center the title
    margin=dict(l=20, r=20, t=40, b=20)  # Adjust margins
)

































# Aggregate the data: we’ll count the number of products (entries) per state as a proxy for number of stores
global_sales = df.groupby('State').agg(
    total_sales=('Sales', 'sum'),
    total_entries=('Sales', 'count')  # Number of entries per state (or "stores")
).reset_index()

# Perform linear regression (find the trend line between number of entries and total sales)
slope, intercept, r_value, p_value, std_err = linregress(global_sales['total_entries'], global_sales['total_sales'])

# Create a trend line (y = mx + b)
trend_line = slope * global_sales['total_entries'] + intercept
fig_trend = {
       'data': [
        # Scatter plot: Number of entries vs Total Sales
        go.Scatter(
            x=global_sales['total_entries'],
            y=global_sales['total_sales'],
            mode='markers',
            name='Sales vs. Number of Entries (Stores)',
            marker=dict(color='blue', size=10, opacity=0.7)
        ),
        # Trend line
        go.Scatter(
            x=global_sales['total_entries'],
            y=trend_line,
            mode='lines',
            name='Trend Line',
            line=dict(color='red', width=2, dash='dash')
        )
    ],
    'layout': go.Layout(
        title='Correlation Between Number of Stores and Total Sales',
        xaxis=dict(title='Number of Entries (Stores)'),
        yaxis=dict(title='Total Sales'),
        showlegend=True
    )
}





































































app = dash.Dash(__name__)
# Updated Dash App Layout
app.layout = html.Div(className='main-container',
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f5f5f5',
        'color': '#333',
        'padding': '20px'
    },
    children=[

        html.Div("Superstore Sales Dashboard", style={
            'textAlign': 'center',
            'fontSize': '30px',
            'fontWeight': 'bold',
            'marginBottom': '40px',
            'color': '#2c3e50'
        }),

        # Graphs Section: Total Sales Gauge, Total Profit Gauge, Top 10 States
        html.Div([
            # RadioButtons placed above the chart with a seamless background
            html.Div([
                dcc.RadioItems(
                    id='top-bottom-selector',
                    options=[
                        {'label': 'Top 10 States', 'value': 'top'},
                        {'label': 'Bottom 10 States', 'value': 'bottom'}
                    ],
                    value='top',
                    labelStyle={'display': 'inline-block', 'marginRight': '20px'},
                    style={
                        'textAlign': 'left',
                        'margin': '7px',
                        'width': '600px',
                        'padding': '10px',
                        'backgroundColor': '#ffffff', 
                    }
                ),
                dcc.Graph(
                    id='sales-by-state',
                    style={'margin': '7px', 'width': '600px', 'borderRadius': '10px'} 
                )
            ],className='chart-container', style={
                'textAlign': 'center',
                'display': 'inline-block',
                'width': 'auto',
                'backgroundColor': '#ffffff',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'padding': '10px'
            }),

            # Total Sales Gauge
         html.Div(
             dcc.Graph(figure=fig_totalSalesIndicator), className='gauge-graph',
             style={
             'borderRadius': '10px',  
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  
             'width': '350px',
             'margin': '5px',
           'overflow': 'hidden', 
        'backgroundColor': 'white',  
    }
), html.Div(
            # Total Profit Gauge
            dcc.Graph(
                figure=fig_total_profitIndicator, className='gauge-graph',
                 style={
              'borderRadius': '10px',  
              'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
              'width': '350px',
              'margin': '5px',
            'overflow': 'hidden', 
              'backgroundColor': 'white'} 
            ),),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'flexWrap': 'wrap',
            'gap': '2px'
        }),

    
        # Dropdown and Graph Section with the same styling as Top 10 States
html.Div([
html.Div([  
    # First Dropdown: Metric Selector
    html.Div([
        dcc.Dropdown(
            id='metric-selector', className='dropdown',
            options=[
                {'label': 'Sales', 'value': 'Sales'},
                {'label': 'Profit', 'value': 'Profit'},
                {'label': 'Quantity', 'value': 'Quantity'}
            ],
            value='Sales',  # Default value for Metric Selector
            clearable=False,
            style={'width': '50%', 'textAlign': 'center'}  
        )
    ], style={
        'backgroundColor': '#ffffff',
        'textAlign': 'center',
         'flex': '1',
        'padding': '0',  
        'marginRight': '10px',  
    }),

    # Second Dropdown: Level Selector
    html.Div([
        dcc.Dropdown(
            id='level-selector',
            options=[
                {'label': 'Category', 'value': 'Category'},
                {'label': 'Sub-Category', 'value': 'Sub-Category'}
            ],
            value='Sub-Category',  # Default value to 'Sub-Category'
            clearable=False,
            style={'width': '50%', 'textAlign': 'center'} 
        )
    ], style={
        'flex': '1',
        'backgroundColor': '#ffffff',
        'textAlign': 'center',
        'padding': '0',  
    })
], style={
    'display': 'flex',  # Flexbox for side-by-side alignment
    'justifyContent': 'flex-start',  # Align items to the left
    'gap': '10px',  # Small gap between the dropdowns
    'backgroundColor': '#ffffff',
    'borderRadius': '10px',
    'marginBottom': '20px',
    'width': 'auto',  # Automatically adjust the container width
})
,


# Graph Section
dcc.Graph(
    id='sales-by-category',  className='category-graph',
    style={
        'marginTop': '20px', 
        'width': '100%',  
    }
),
], style={
    'textAlign': 'center',
    'backgroundColor': '#ffffff',
    'borderRadius': '10px',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    'padding': '10px',
    'marginTop': '20px',
    'width': '100%',  
}),



  # Other graphs with a top margin
html.Div([
    # Container for the two graphs with margin-top
    html.Div([
      html.Div(  dcc.Graph(figure=fig_TypeOfCustomers ,className='graph', style={
              'borderRadius': '10px',  
              'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  
              'margin': '5px',
            'overflow': 'hidden',  
              'backgroundColor': 'white'} 
            ),),
       html.Div( dcc.Graph(figure=fig_ShipModeTreemap, className='graph',style={
              'borderRadius': '10px', 
              'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
              'margin': '5px',
            'overflow': 'hidden', 
              'backgroundColor': 'white'} 
            ),),
    ], className='graph-container', style={
        'display': 'flex',
        'justify-content': 'space-between',  
        'gap': '20px', 
        'marginTop': '20px' 
    })
])

    , html.Div([
       html.Div( dcc.Graph(figure=fig_SalesByStateMap, className='graph',style={
              'borderRadius': '10px',  
              'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
              'margin': '5px',
            'overflow': 'hidden',  
              'backgroundColor': 'white'}
            ),),
        html.Div([ dcc.Graph(figure=fig_sun, style={
              'borderRadius': '10px', 
              'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
              'margin': '5px',
            'overflow': 'hidden',  
              'backgroundColor': 'white'} 
            )],),
    ],  className='graph-container',style={
        'display': 'flex',
        'justify-content': 'space-between', 
        'gap': '20px', 
        'marginTop': '30px' 
    }),
    
html.Div([
    # Container for two scatter plots
    html.Div([
        # First scatter plot
        dcc.Graph(
            figure=fig_discount,className='graph',
            style={
                'borderRadius': '10px', 
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'marginTop': '30px',
                'overflow': 'hidden', 
                'backgroundColor': 'white', 
                'width': '46%' 
            }
        ),
        # Second scatter plot
        dcc.Graph(
            figure=fig_discount_quantity,
            style={
                'borderRadius': '10px',  
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                'marginTop': '30px',
                'overflow': 'hidden',  
                'backgroundColor': 'white',  
                'width': '46%'  
            }
        )
    ],className='graph',
    style={
        'display': 'flex',  
        'flexDirection': 'row',  # Align items horizontally
        'justifyContent': 'space-between',  # Space evenly between items
        'gap': '20px'  # Reduced spacing between items
    }),

    # Container for the third plot below
    html.Div([
        dcc.Graph(
            figure=fig_trend,
            style={
                'borderRadius': '10px', 
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                'marginTop': '30px',
                'overflow': 'hidden',  
                'backgroundColor': 'white' 
            }
        )
    ],className='scatter-plot-container',
    style={
        'marginTop': '30px'  # Add margin above the third plot
    })])
])




















































# Callbacks and app.run_server() follow as before


# Callback to update the sales-by-state figure based on radio button selection

color_scale = [[0, '#8b69ff'], [1, '#0057ff']]  # Custom gradient from purple to blue


@app.callback(
    Output('sales-by-state', 'figure'),
    Input('top-bottom-selector', 'value')
)
def update_sales_by_state(selected_option):
    if selected_option == 'top':
        selected_states = state_sales.head(10)  # Get top 10 states by sales
        title = 'Top 10 States by Total Sales'
    else:
        selected_states = state_sales.tail(10)  # Get bottom 10 states by sales
        title = 'Bottom 10 States by Total Sales'
    
    # Define the custom color scale from purple (#8b69ff) to blue (#0057ff)
    color_scale = [[0, '#4225f4'], [1, '#0057ff']]  # Custom gradient from purple to blue

    # Define the figure
    fig = {
        'data': [
            go.Bar(
                x=selected_states['State'],  # Categories (States)
                y=selected_states['Sales'],  # Values (Sales)
                width=0.7,
                marker=dict(
                    color=selected_states['Sales'],  # Color bars based on sales values
                    colorscale=color_scale # Apply the custom purple to blue gradient
                )
            )
        ],
        'layout': go.Layout(
            title=title,  # Title of the chart
            showlegend=False,
            hovermode='closest'
        )
    }

    # Return the figure
    return fig



@app.callback(
    Output('sales-by-category', 'figure'),
    [Input('metric-selector', 'value'), Input('level-selector', 'value')]
)
def update_figure(selected_metric, selected_level):
    # Group the data by selected level and metric, then sort it
    data_grouped = df.groupby(selected_level)[selected_metric].sum().reset_index().round(0)
    data_grouped = data_grouped.sort_values(by=selected_metric, ascending=False)

    # Define a custom color scale from purple (#8b69ff) to blue (#0057ff)
    #color_scale = [[0, '#8b69ff'], [1, '#0057ff']]  # Custom gradient from purple to blue
    
    fig = {
        'data': [
            go.Bar(
                x=data_grouped[selected_level],  # Categories (e.g., sub-category or category)
                y=data_grouped[selected_metric],  # Values (e.g., total sales or profit)
                marker=dict(
                    color=data_grouped[selected_metric],  # Color bars based on metric values
                    colorscale=color_scale # Apply custom purple to blue gradient
               
                )
            )
        ],
        'layout': go.Layout(
            title=f"Total {selected_metric} by {selected_level}",
            showlegend=False,
            hovermode='closest',
            yaxis_title=selected_metric,
            xaxis_title=selected_level,  # Add the x-axis title to match the level
            margin={'l': 40, 'r': 40, 't': 40, 'b': 40}  # Adjust margins for clarity
        )
    }
    return fig



if __name__ == '__main__':
    app.run_server(debug=False)

