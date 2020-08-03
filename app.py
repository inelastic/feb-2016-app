###############################################################################
#Import libraries
###############################################################################
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
###############################################################################
#Define Functions to be used here
###############################################################################
#the function for laser off
def loff_func(x,a,b,g):
    return a + b*np.exp(-g*x)

#create sample temperature plot
def temp_plot(df, ttitle):
    hovertemp ='<B>Time(s)</B>: %{x}'+'<br><b>Temperature(K)</b>: %{y}<extra></extra>'
    
    trace1 = go.Scatter(
        name='Sample Temperature',
        x=df['Time(s)'],
        y=df['Temp(K)'],
        hovertemplate=hovertemp,
        mode='lines',
        line=dict(color='rgb(31, 119, 255)'),
    )
    
    layout = go.Layout(
        xaxis=dict(title='Time(s)',
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='rgb(0,0,0)'),
        yaxis=dict(title='Temperature(K)',
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='rgb(0,0,0)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel_align = 'left',
        plot_bgcolor='rgb(255,255,255)',        
        title=ttitle,
        showlegend = True)
    
    fig = go.Figure(data=trace1, layout=layout)    
    return fig
    
#Create asymmetry plots. There are 3 options for display. The figures are added
#to the plot based on which options are checked.
def asym_plots(atitle, df, run, df2, plots):    
    hovertemp ='<B>Time(us)</B>: %{x}'+'<br><b>Asymmetry</b>: %{y}<extra></extra>'
    
    trace1e = go.Scatter(
        name='Laser Off',
        x=df['Time'],
        y=df['Laser Off'],
        hovertemplate=hovertemp,
        mode='lines',
        line=dict(color='rgb(31, 119, 255)'),
        error_y=dict(
            type='data',
            array=df['Laser Off Err'],
            visible=True,
            color='darkgray',
            thickness=1))
    
    trace2e = go.Scatter(
        name='Laser On',
        x=df['Time'],
        y=df['Laser On'],
        hovertemplate=hovertemp,        
        mode='lines',
        line=dict(color='rgb(0, 255, 35)'),
        error_y=dict(
            type='data',
            array=df['Laser On Err'],
            visible=True,
            color='darkgray',
            thickness=1))
    
    trace1 = go.Scatter(
        name='Laser Off',
        x=df['Time'],
        y=df['Laser Off'],
        hovertemplate=hovertemp,        
        mode='lines',
        line=dict(color='rgb(31, 119, 180)'))
    
    trace2 = go.Scatter(
        name='Laser On',
        x=df['Time'],
        y=df['Laser On'],
        hovertemplate=hovertemp,        
        mode='lines',
        line=dict(color='rgb(0, 255, 35)'))

    trace3 = go.Scatter(
        name='Laser Off Fit',
        x=df['Time'],
        y=loff_func(df['Time'],*[df2.loc[run]['Loff A'], df2.loc[run]['Loff B'], df2.loc[run]['Loff g']]),
        hovertemplate=hovertemp,        
        mode='lines',
        line=dict(color='rgb(255, 0, 0)'))
    
#The plots array is built by first checked, first written. So, all cases/permutations must be considered
    data = []
    if len(plots) == 0:
        data = [trace1]
    elif len(plots) == 1:
        if plots == ['LOF']:
            data = [trace1, trace3]
        elif plots == ['LOE']:
            data = [trace1, trace2]
        elif plots == ['EB']:
            data = [trace1e]
    elif len(plots) == 2:
        if plots == ['LOF', 'LOE']:
            data = [trace1, trace2, trace3]
        if plots == ['LOE', 'LOF']:
            data = [trace1, trace2, trace3]
        elif plots == ['LOF', 'EB']:
            data = [trace1e, trace3]
        elif plots == ['EB', 'LOF']:
            data = [trace1e, trace3]            
        elif plots == ['LOE', 'EB']:
            data = [trace1e, trace2e]
        elif plots == ['EB', 'LOE']:
            data = [trace1e, trace2e]            
    elif len(plots) == 3:
        data = [trace1e, trace2e, trace3]
        
#create layout of plot    
    layout = go.Layout(
        xaxis=dict(title='Time(us)',
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='rgb(0,0,0)'),
        yaxis=dict(title='Asymmetry',
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='rgb(0,0,0)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel_align = 'left',
        plot_bgcolor='rgb(255,255,255)',        
        title=atitle,
        showlegend = True)
    
    fig = go.Figure(data=data, layout=layout)
    return fig

#creating the butterfly graph
def butterfly_graph(sipe):
    hovertemp ='<B>Photon E(eV)</B>: %{x}'+'<br><b>Asymmetry(%)</b>: %{y}<extra></extra>'
    smtitle=r'$\sigma^{-} - \sigma^{+}$'
    sptitle=r'$\sigma^{+} - \sigma^{-}$'
    offsetlinex = [1.165,1.22]
    offsetlinex_rev = offsetlinex[::-1]
    offsetliney = [offsetval*100 for n in offsetlinex]
    offsetlineupper = [(offsetval+offsetval_err)*100 for n in offsetlinex]
    offsetlinelower = [(offsetval-offsetval_err)*100 for n in offsetlinex]
    plot_data = [{'x': offsetlinex+offsetlinex_rev, 'y': (offsetlineupper)+(offsetlinelower)}, 
                 {'x': sipe['Photon eV'], 'y': sipe['DSP']},
                 {'x': sipe['Photon eV'], 'y': -sipe['DSP']}]

    
    trace1 = go.Scatter(
        x=offsetlinex+offsetlinex_rev,
        y=(offsetlineupper)+(offsetlinelower),
        hovertemplate = hovertemp,
        fill='tozerox',
        fillcolor='rgba(0,100,80,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        name='Offset',
        yaxis='y1'
    )
    
    trace2 = go.Scatter(
        x=offsetlinex,
        y=offsetliney,
        hovertemplate = hovertemp,
        line=dict(color='rgb(0,100,80)'),
        mode='lines',
        name='Offset',
        yaxis='y1'    
    )
    
    trace3 = go.Scatter(
        x= sm['Photon E(eV)'],
        y=sm['Asym Diff']*100,
        hovertemplate = hovertemp,
        error_y=dict(
            type='data',
            array=(sm['Asym Diff Err'])*100,
            color='MediumPurple',
            visible=True),
        name=smtitle,
        mode='markers',
        marker_symbol='triangle-up',
        marker=dict(
            color='LightSkyBlue',
            size=20,
            line=dict(
                color='MediumPurple',
                width=2
            )
        ),
        yaxis='y1'
    )
    
    trace4 = go.Scatter(
        x= sp['Photon E(eV)'],
        y=sp['Asym Diff']*100,
        hovertemplate = hovertemp,
        error_y=dict(
            type='data',
            array=(sp['Asym Diff Err'])*100,
            visible=True),
        name=sptitle,
        mode='markers',
        marker_symbol='triangle-up',
        marker=dict(
            color='rgb(255,30,0)',
            size=20,
            line=dict(
                color='rgb(0,0,0)',
                width=2
            )
        ),    
        yaxis='y1'
    )
    
    trace5 = go.Scatter(
        x=plot_data[1]['x'],
        y=plot_data[1]['y'],
        hovertemplate = hovertemp,
        mode='lines',
        yaxis='y2',
        name='Sipe',
        line=dict(
            color='rgb(0,0,0)'
        )
    )
    
    trace6 = go.Scatter(
        x=plot_data[2]['x'],
        y=plot_data[2]['y'],
        hovertemplate = hovertemp,
        mode='lines',
        yaxis='y2',
        name='-Sipe',
        line=dict(
            color='rgb(255,0,0)'
        )
    )
    
        
    data = [trace1, trace2, trace3, trace4, trace5, trace6]
    
    layout = go.Layout(
        hoverlabel_align='left',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        width=800,
        height=600,
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(255,255,255)',
        xaxis=dict(
            title='Photon Energy(eV)',
            gridcolor='rgb(255,255,255)',
            range=offsetlinex,
            showgrid=False,
            showline=True,
            showticklabels=True,
            tickcolor='rgb(127,127,127)',
            ticks='outside',
            zeroline=False,
            mirror=True,
            linecolor='rgb(0,0,0)'
        ),
        yaxis=dict(
            title='Asymmetry(%)',
    
            gridcolor='rgb(0,255,255)',
            showgrid=False,
            showline=True,
            showticklabels=True,
            tickcolor='rgb(127,127,127)',
            ticks='outside',
            zeroline=False,
            mirror=True,
            linecolor='rgb(0,0,0)'
        ),
    
        yaxis2=dict(
            title='DSP(%)',
            gridcolor='rgb(255,255,255)',
            showgrid=False,
            showline=True,
            showticklabels=True,
            tickcolor='rgb(127,127,127)',
            ticks='outside',
            zeroline=False,
            overlaying='y',
            side='right',
            mirror=True,
            linecolor='rgb(0,0,0)'
        ),
    )
    return go.Figure(data=data, layout=layout)


###############################################################################
#Setup data to be displayed
###############################################################################
#setting the directory and grabbing the filenames
directory="https://raw.githubusercontent.com/inelastic/feb-2016-app/master/ProcessedCSV/"
#directory="E:\Storage\Documents\Python Files\RALAnalysis\Feb 2016 App\ProcessedCSV\\"
filenames = ['96329','96343','96362','96362','96383','96397','96411','96430','96458',
             '96478','96495','96511','96527','96542','96555','96569','96587','96605','96624','96635']
fitdata = pd.read_csv(directory+'fitdata.csv', index_col=0)
#remove the instances of 1054 that aren't 30% power drop
fitdata = fitdata.drop([96555, 96511])
#re-indexing fitdata to use in graphs

fitdataindex = fitdata['Wavelength(nm)'].astype(str)+'_'+fitdata['QWP Pos'].astype(str)
#fitdataindex = fitdataindex.str[:-2]
fitdata = fitdata.set_index(fitdataindex.values)

#set dict to hold data
tempdata = {}
Asym = {}

wavelengths = np.empty(len(filenames), dtype=object) 
qwppos = np.zeros(len(filenames))
for i in range(len(filenames)): 
    if ((filenames[i] != '96555') and (filenames[i] != '96569')):
        temp1 = pd.read_csv(directory+'Sample_Temperature/'+filenames[i]+'.csv', index_col=0)
        temp1['Time']= pd.to_datetime(temp1['Time']) 
        wavelengths[i] = str(temp1['Wavelength'].values[0])
        qwppos[i] = temp1['QWP_Pos'].values[0]
        name = str(temp1['Wavelength'].values[0])+'_'+str(temp1['QWP_Pos'].values[0])
        tempdata[name] = temp1
        temp2 = pd.read_csv(directory+'Asymmetry/'+filenames[i]+'.csv')
        Asym[name] = temp2

        
#Bring in Integral Data
butterfly = pd.read_csv(directory+'butterfly.csv', index_col=0)
offsetval = -0.000183
offsetval_err = 0.000046
sm = butterfly.loc[butterfly['QWP Pos'] == 0]
sp = butterfly.loc[butterfly['QWP Pos'] == 1]
#Importing Sipe data to add to plot, and create interp function
sipe = pd.read_csv(directory+'sipe.csv')
sipe.columns = ['hw - eV', 'DSP']
photonev = 1.158 + sipe['hw - eV']
sipe.insert(1,'Photon eV', photonev)
sipe = sipe.sort_values(by='Photon eV', ascending=True)
#creating butterfly graph
butterflyfig =butterfly_graph(sipe)

  

                    
###############################################################################
#Build Dash App
###############################################################################
#grab variables for menus
runs = pd.DataFrame(zip(wavelengths,qwppos),columns=['Wavelength', 'QWP_Pos'])
runs = runs.dropna()
fnameDict = {0: np.sort(runs.loc[runs['QWP_Pos'] == 0]['Wavelength'].values), 1: np.sort(runs.loc[runs['QWP_Pos'] == 1]['Wavelength'].values)}

#create Summary table
table_header = [
    #html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]
tempave = tempdata[fnameDict[0][0]+'_0']['Temp(K)'].mean()
tempaverr = tempdata[fnameDict[0][0]+'_0']['Temp(K)'].sem(axis=0)
row1 = html.Tr([html.Td("# Of Events (Mev)"), html.Td(fitdata.loc[fnameDict[0][0]+'_0']['Raw Events(MeV)'])])
row2 = html.Tr([html.Td("Signal (%)"), html.Td('%5.5f +- %5.5f' %(fitdata.loc[fnameDict[0][0]+'_0']['Asym Diff'], abs(fitdata.loc[fnameDict[0][0]+'_0']['Asym Diff Err'])))])
row3 = html.Tr([html.Td("Asym Drop (%)"), html.Td('%5.5f +- %5.5f' %(fitdata.loc[fnameDict[0][0]+'_0']['Power Drop']*100, abs(fitdata.loc[fnameDict[0][0]+'_0']['Power Drop Err']*100)))])
row4 = html.Tr([html.Td("Temp Ave (K)"), html.Td('%5.3f +- %5.5f' %(tempave, tempaverr))])


table_body = html.Tbody([row1, row2, row3, row4])

# Build App
stylesheet = 'https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/cerulean/bootstrap.min.css'
app = dash.Dash(__name__, external_scripts=[
  'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'],
  external_stylesheets=[stylesheet]
)
server = app.server


#create layout
app.layout = dbc.Container([
    html.H1("Feb 2016 Si Results"),
    dbc.Row(
        [
            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader("Data"),
                    dbc.CardBody(
                        [            
                            dbc.Row(dbc.Col(dcc.Dropdown(id='wavelength-dropdown',
                                         clearable=False,
                                         options=[{'label': i, 'value': i} for i in list(fnameDict[0])],
                                         value=fnameDict[0][0]
                           ),width=6),),
                            dbc.Row(dbc.Col(html.Label('QWP Position'),),),
                            dbc.Row(
                                [
                                dbc.Col(dcc.RadioItems(
                                    id='QWP-Pos',
                                    options=[{'label': i, 'value': i} for i in list(fnameDict.keys())],
                                    value = 0,
                                    labelStyle={'display': 'inline-block', 'margin-right': 5}
                                ), width=4),
                            ]
                            ),
                            dbc.Row(html.Div(id='notes')),
                        ]
                    ),                   
                ],
            ),),
        dbc.Col(dbc.Table(id="summary-table", children=table_body, bordered=True))
        ]),    
    html.Hr(),
    html.H2("Sample Temperature"),
    dcc.Graph(id='temp'),
    html.Hr(),
    html.H2("Integral Data"),
    dcc.Graph(figure=butterflyfig),
    html.Hr(),
    html.H2('Asymmetry Plots'),
    dcc.Graph(id='asym'),
    dcc.Checklist(
        id='plots',
        options=[
            {'label': 'Laser Off Fit', 'value': 'LOF'},
            {'label': 'Laser On', 'value': 'LOE'},
            {'label': 'Error Bars', 'value': 'EB'}
        ],
    value=['LOF', 'LOE', 'EB'],
    labelStyle={'display': 'inline-block', 'margin-right': 8}
    ),
])

# Define callbacks to update graph
@app.callback(
    Output('wavelength-dropdown', 'options'),
    [Input('QWP-Pos', 'value')]
)
def update_dropdown(name):
    return [{'label': i, 'value': i} for i in list(fnameDict[name])]

@app.callback(
    Output('notes', 'children'),
    [Input('wavelength-dropdown', 'value'),
     Input('QWP-Pos', 'value')]
)
def update_notes(tempdata_value, qwp_pos_value):
    try:
        run = str(tempdata_value)+'_'+str(qwp_pos_value)
        data = tempdata[run]
        return 'Note: Data updated sucessfully.'
    except:
        return 'Note: The wavelength {0} doesn\'t have data for QWP Position {1}. Data updated to wavelength {2} for QWP Pos {1}'.format(str(tempdata_value), str(qwp_pos_value), fnameDict[qwp_pos_value][0])

@app.callback(
   [Output('temp', 'figure'),
    Output('asym','figure')],
    [Input("wavelength-dropdown", "value"),
     Input("QWP-Pos", "value"),
     Input("plots", 'value')]
)
def update_figure(tempdata_value, qwp_pos_value, plots):
    try:
        run = str(tempdata_value)+'_'+str(qwp_pos_value)
        temperdata = tempdata[run]
        asymdata = Asym[run]
        ttitle = r"$\lambda: "+str(tempdata_value)+r"\text{, QWP Pos: } "+str(qwp_pos_value)+"$"
        atitle = r"$\lambda: "+str(tempdata_value)+r"\text{, QWP Pos: } "+str(qwp_pos_value)+"$"
    except:
        run = fnameDict[qwp_pos_value][0]+'_'+str(qwp_pos_value)
        temperdata = tempdata[run]
        asymdata = Asym[run]
        ttitle = r"$\lambda: "+fnameDict[qwp_pos_value][0]+r"\text{, QWP Pos: } "+str(qwp_pos_value)+"$"
        atitle = r"$\lambda: "+fnameDict[qwp_pos_value][0]+r"\text{, QWP Pos: } "+str(qwp_pos_value)+"$"
    finally:
        tempfig = temp_plot(temperdata,ttitle)
        asymfig = asym_plots(atitle, asymdata, run, fitdata, plots)
        return tempfig, asymfig
    
@app.callback(
    [Output('summary-table', 'children')],
    [Input("wavelength-dropdown","value"),
      Input("QWP-Pos","value")],    
)
def update_table(wavelength, qwp_pos):
    run = str(wavelength)+'_'+str(qwp_pos)
    tempave = tempdata[run]['Temp(K)'].mean()
    tempaverr = tempdata[run]['Temp(K)'].sem(axis=0)

    row1 = html.Tr([html.Td("# Of Events (Mev)"), html.Td(fitdata.loc[str(wavelength)+'_'+str(qwp_pos)]['Raw Events(MeV)'])])
    row2 = html.Tr([html.Td("Signal (%)"), html.Td('%5.5f +- %5.5f' %(fitdata.loc[str(wavelength)+'_'+str(qwp_pos)]['Asym Diff'], abs(fitdata.loc[str(wavelength)+'_'+str(qwp_pos)]['Asym Diff Err'])))])
    row3 = html.Tr([html.Td("Asym Drop (%)"), html.Td('%5.5f +- %5.5f' %(fitdata.loc[str(wavelength)+'_'+str(qwp_pos)]['Power Drop']*100, abs(fitdata.loc[str(wavelength)+'_'+str(qwp_pos)]['Power Drop Err']*100)))])
    row4 = html.Tr([html.Td("Temp Ave (K)"), html.Td('%5.3f +- %5.5f' %(tempave, tempaverr))])
    
    table_body = [html.Tbody([row1, row2, row3, row4])]
    return table_body
    
if __name__ == '__main__':    
    app.run_server(debug=True)