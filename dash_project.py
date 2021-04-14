import dash
import dash_core_components as dcc
import dash_html_components as html
import new_calculator as calculator
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id= 'graph-with-slider'),
    dcc.Slider(
        id = 'R0-slider',
        min =1,
        max =10,
        marks = {i:'R={}'.format(i) for i in range(1,10)},
        value = 5,
        step =None
    ),

    html.Div(className='markDown',
             children=[
                 dcc.Markdown('''
                This is the SEIR graph based on R and K.
                
                Total population is 100000.
                
                Initial Suspectible is 100000, Initial Exposed is 0, Initial Infectious is 1, Initial Recovery is 0.
                ''')]),

    html.Div(className='multiple-factors',
             children=[
                 dcc.Graph(id='graph-multiple-factors'),
                 dcc.Markdown("Total population, Start suspectible, Start exposed, Start infectious, Start recovery, Time between infection and confirm, Latent Time, People meet, Total days"),
                 dcc.Input(id='N_Input', type='number', placeholder='Total population'),
                 dcc.Input(id='S_0_Input',type='number', placeholder='Start Suspectible'),
                 dcc.Input(id='E_0_Input', type='number', placeholder='Start Exposed'),
                 dcc.Input(id='I_0_Input', type='number', placeholder='Start Infectious'),
                 dcc.Input(id='recovery_Input', type='number', placeholder='Start recovery'),
                 dcc.Input(id='confirmTime_Input', type='number', placeholder='Confirm time'),
                 dcc.Input(id='latentTime_Input', type='number', placeholder='Latent Time'),
                 dcc.Input(id='meetNumber_Input', type='number', placeholder='People meet'),
                 dcc.Input(id='totalDays_Input', type='number', placeholder='Total days'),
                 dcc.Markdown("Please input some epidemic prevention measures"),
                 dcc.Markdown("Input after X days, and choose government methods"),
                 dcc.Input(id='afterDays_Input', type='number', placeholder='After X days'),
                 dcc.Dropdown(
                     id='methods_Dropdown',
                     options=[{'label':'30% vaccine','value':'30%vaccine'},
                              {'label':'50% vaccine','value':'50%vaccine'},
                              {'label':'70% vaccine','value':'70%vaccine'},
                              {'label':'Stay at home','value':'home'},
                              {'label':'Mask everyone','value':'mask'}],
                     multi=True, placeholder='Choose government methods'
                 )
             ])

])

@app.callback(
    Output('graph-with-slider','figure'),
    [Input('R0-slider','value')]
)
def draw_R0(R0):
    S_t, E_t,I_t,R_t = calculator.R0_calculator(100000,100000,0,1,0,R0,100)
    dayList =[]
    for i in range(len(S_t)):
        dayList.append(i)
    figure = {
        'data':[
            {'x': dayList, 'y':S_t, 'type': 'bar','name':'Suspectible'},
            {'x': dayList, 'y': E_t, 'type': 'bar', 'name': 'Exposed'},
            {'x': dayList, 'y': I_t, 'type': 'bar', 'name': 'Infectious'},
            {'x': dayList, 'y': R_t, 'type': 'bar', 'name': 'Recovery'},
        ],
        'layout' :{
            'title':'数据展示'
        }
    }

    return figure

@app.callback(
    Output('graph-multiple-factors', 'figure'),
    [Input("N_Input","value"),Input('S_0_Input','value'),Input('E_0_Input','value'),Input('I_0_Input','value'),Input('recovery_Input','value'),Input('confirmTime_Input','value'),
     Input('latentTime_Input','value'),Input('meetNumber_Input','value'),Input('totalDays_Input','value'),Input('methods_Dropdown','value')]
)
def draw_mutipleFactors(N, S_0, E_0,I_0,recovery,confirmTime,latentTime,r,T,methods):

    S_t, E_t, I_t, R_t = calculator.multiple_factor_calculator(N,S_0, E_0,I_0,recovery,confirmTime, latentTime,r,T,methods)


    dayList =[]
    for i in range(len(S_t)):
        dayList.append(i)

    figure = {
        'data':[
            {'x': dayList, 'y':S_t, 'type': 'bar','name':'Suspectible'},
            {'x': dayList, 'y': E_t, 'type': 'bar', 'name': 'Exposed'},
            {'x': dayList, 'y': I_t, 'type': 'bar', 'name': 'Infectious'},
            {'x': dayList, 'y': R_t, 'type': 'bar', 'name': 'Recovery'},
        ]
    }

    return figure


if __name__ == '__main__':
    app.run_server(debug=False)


