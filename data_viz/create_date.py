import pandas as pd
import plotly.express as px
import datetime
import dash
import dash_html_components as html
import dash_core_components as dcc

def create_dropdown(l, column_name, df):

    for c in df[column_name].unique():
        l.append({'label': c, 'value' : c})
    return l

df = pd.read_csv('data/complaint_clean_merged.csv')

#formatting date
df['incident_date'] = df['incident_date'].astype(str)
df = df[df['incident_date'] != "Unclear"] #filter out incidents without dates

df['incident_date'] = pd.to_datetime(df['incident_date'], infer_datetime_format= True)

df = df[df['complainant_age'] > 3] #filter out things with ages less than 3 (looked like errors)

#formating string
df.summary = df.summary.str.wrap(40)
df.summary = df.summary.apply(lambda x : x.replace('\n', '<br>'))
fig = px.scatter(df, title = "Age and Date of Incident", x = "incident_date", y = "complainant_age", color = 'general_cap_classification',
hover_data=['summary'])


#creating graph
fig.update_layout(xaxis_range = [datetime.datetime(2015, 1, 1), datetime.datetime(2020, 9, 1)])

opt_race = [{'label': 'all races', 'value' : 'all'}]
opt_sex = [{'label': 'all genders', 'value' : 'all'}]
opt_type = [{'label' : "ALL COMPLAINTS", 'value' : 'all'}]
opts = [opt_race, opt_sex, opt_type]
opts_column = ['complainant_race', 'complainant_sex', 'general_cap_classification']

for o in range(len(opts)):
    create_dropdown(opts[o], opts_column[o], df)

app = dash.Dash()


app.layout = html.Div([
    html.Div(
        [
            dcc.Dropdown(
                id='race_select',
                options= opt_race,
                value='all'
            )
        ],
        style={'width': '20%', 'display': 'inline-block'}
    ),
    html.Div(
        [
            dcc.Dropdown(
                id='sex_select',
                options=opt_sex,
                value='all'
            )
        ],
        style={'width': '20%', 'display': 'inline-block'}
    ),
    html.Div(
        [
            dcc.Dropdown(
                id='type_select',
                options= opt_type,
                value= 'all'
            )
        ],
        style={'width': '20%', 'display': 'inline-block'}
    ),
    dcc.Graph(figure = fig, id ='scatter_plt')
])

@app.callback(
    dash.dependencies.Output('scatter_plt', 'figure'),
    [
        dash.dependencies.Input('race_select', 'value'),
        dash.dependencies.Input('sex_select', 'value'),
        dash.dependencies.Input('type_select', 'value')
    ]
)
def update_graph(race, sex, type_opt):
    df_temp = df.copy()
    inputs = [race, sex, type_opt]
    for i in range(len(inputs)):
        if inputs[i] != "all":
            df_temp = df_temp[df_temp[opts_column[i]] == inputs[i]]

    if df_temp['general_cap_classification'].count() <= 1:
        fig = px.scatter(df_temp, x = "incident_date", y = "complainant_age", title = "Age and Date of Incident")
        fig.update_layout(xaxis_range = [2015, 2020.75], yaxis_range = [0, 100])
        
        
    else:
        fig = px.scatter(df_temp, title = "Age and Date of Incident", x = "incident_date", y = "complainant_age", color = 'general_cap_classification',
        hover_data=['summary'])

        
        #creating graph
        fig.update_layout(xaxis_range = [datetime.datetime(2015, 1, 1), datetime.datetime(2020, 9, 1)], yaxis_range = [0, 100])

        

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

