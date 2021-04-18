import dash
import dash_core_components as dcc
import dash_html_components as html
from main import calculator as calculator
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
        ## Some R of other infectious diseases.
        
        Measles:12-18;  Diphtheria: 6-7
        
        Smallpox: 5-7;  AIDS: 2-7
        
        SARS: 1-3;  The influenza of 1918: 2-3
        
        Ebola:1.5-2.5;  2019-nCoV-SARS: 1.4-7(not clear now)

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
                              {'label':'Mask everyone','value':'mask'},
                              {'label':'testing & tracing','value':'testing'}],
                     multi=True, placeholder='Choose government methods'
                 )
             ])

])

@app.callback(
    Output('graph-with-slider','figure'),
    [Input('R0-slider','value')]
)
def draw_SEIR_R0(R0):
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
            'title':'Graph based R and K(S0=100000, E0=0, I0=1, R0=0, K=0.1)'
        }
    }

    return figure

@app.callback(
    Output('graph-multiple-factors', 'figure'),
    [Input("N_Input","value"),Input('S_0_Input','value'),Input('E_0_Input','value'),Input('I_0_Input','value'),Input('recovery_Input','value'),Input('confirmTime_Input','value'),
     Input('latentTime_Input','value'),Input('meetNumber_Input','value'),Input('totalDays_Input','value'),Input('afterDays_Input','value'),Input('methods_Dropdown','value')]
)
def draw_SEIR_mutipleFactors(N, S_0, E_0,I_0,recovery,confirmTime,latentTime,r,T, afterDays, methods):

    S_t, E_t, I_t, R_t, R0List = calculator.multiple_factors_calculator(N,S_0, E_0,I_0,recovery,confirmTime, latentTime,r,T,afterDays,methods)


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


