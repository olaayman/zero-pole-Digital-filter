from bokeh.plotting import figure, output_file, show, Column
from random import random
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.core.enums import ButtonType, SizingMode
from bokeh.core.property.numeric import Size
from bokeh.io import show
from bokeh.models import CustomJS, RadioGroup,Button,Span
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource
from bokeh.models.annotations import Label
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.layouts import grid
from bokeh.events import MouseMove, Tap ,MouseLeave ,PressUp
import numpy as np
import matplotlib.pyplot as plt


#Choosen="red"
zeros_coef = []
poles_coef = []
LABELS = ["Zeros", "Poles"]
ZeroPoleChoose = RadioGroup(labels=LABELS, active=0)
ZeroPoleChoose.js_on_click(CustomJS(code="""
    console.log('ZeroPoleChoose: active=' + this.active, this.toString())
"""))

index= 0

ResetButton=Button(label="Reset",button_type="danger")

UndoButton=Button(label="Undo",button_type="warning")
SaveButton=Button(label="Save",button_type="success")
LoadButton=Button(label="Load",button_type="success")

mag_response = figure(title="magnitude response ",plot_width=400, plot_height=225)
mag_response.xaxis.axis_label ="Frequency [Hz]"
mag_response.yaxis.axis_label="Amplitude"

phase_response = figure(title="phase response " , plot_width=400, plot_height=225)
phase_response.xaxis.axis_label ="Frequency [Hz]"
phase_response.yaxis.axis_label="Phase"

fig = figure(title="Z Plane",x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),plot_width=500, plot_height=500)  # sets size and makes it square
fig.xaxis.axis_label ="Real"
fig.yaxis.axis_label="Imaginary"
ax=fig.axis

theta = np.linspace(-np.pi, np.pi, 201)
fig.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

vline = Span(location=0, dimension='height', line_color='red', line_width=3)
# Horizontal line
hline = Span(location=0, dimension='width', line_color='red', line_width=3)

fig.renderers.extend([vline, hline])


col = ['red' ,'blue']
Zeros = ColumnDataSource(
    data=dict(
        x = [], 
        y = []
    )
    
)
Poles = ColumnDataSource(
    data=dict(
        x = [], 
        y = []
    )
)
# Zeros = ColumnDataSource({
#     'x': [.5 , .2], 'y': [.5 ,.2]
# })
# Poles = ColumnDataSource({
#     'x': [.1], 'y': [.1]
# })

# Zeros = [[0.5,0.5],[0.1,0.1]]
# Poles = [[.2,.2],[.4,.4]]
# if index == 0 :
# else :
#     ZerosRenderer = fig.scatter(x='x', y='y', source=Zeros, color='black', size=10)
#     PolesRenderer = fig.scatter(x='x', y='y', source=Poles, color='blue', size=10)
PolesRenderer = fig.scatter(x='x', y='y', source=Poles, color='blue', size=10)
ZerosRenderer = fig.scatter(x='x', y='y', source=Zeros, color='red', size=10)

# ZerosRenderer = fig.scatter(x=Zeros[0], y=Zeros[1], color='black', size=10)
# PolesRenderer = fig.scatter(x=Poles[0], y=Poles[1], color='blue', size=10)

def addding_ZerosAndPloes(first,second):
    draw_tool = PointDrawTool(renderers=[first,second], empty_value='blue')
    fig.add_tools(draw_tool)
    fig.toolbar.active_tap = draw_tool


def ChangeIndex(i):
    global index
    index = i
    print(index)
    if index == 0 :
        addding_ZerosAndPloes(ZerosRenderer,PolesRenderer)
    else :
        print("one")
        addding_ZerosAndPloes(PolesRenderer,ZerosRenderer)
    print("heey",Zeros.data['x'],Zeros.data['y'],Poles.data['x'],Poles.data['y'])

ZeroPoleChoose.on_click(ChangeIndex)
addding_ZerosAndPloes(ZerosRenderer,PolesRenderer)


def Draw_transfer_function():

    mag_response.renderers=[]
    phase_response.renderers=[]
    w = np.linspace(0,np.pi, 200)    # for evauluating H(w)
    z = np.exp(1j*w)
    f = np.linspace(0, 180, 200)         # for ploting H(w)
    print("draw" ,type(zeros_coef),type(poles_coef))
    if type(zeros_coef) == float and type(poles_coef) == np.ndarray:
        print("only poles")
        H = 1 / np.polyval(poles_coef, z) 
    elif type(poles_coef) == float and type(zeros_coef) == np.ndarray :
        print("only zeros")
        H = np.polyval(zeros_coef, z)  
    else:
        print("both")
        H = np.polyval(zeros_coef, z) / np.polyval(poles_coef, z) 


    phase =  np.unwrap(np.angle(H))
    #print(H)
    mag_response.line(f, abs(H), line_width=2)
    phase_response.line(f, phase, line_width=2)

    
    

def Set_Coefs():
    global zeros_coef , poles_coef
    zeros_pos =[]
    poles_pos = []
    for i in range(len(Zeros.data['x'])):
        zeros_pos.append(Zeros.data['x'][i]+1j*Zeros.data['y'][i])

    for i in range(len(Poles.data['x'])):
        poles_pos.append(Poles.data['x'][i]+1j*Poles.data['y'][i])

    
    zeros_coef = np.poly(zeros_pos)
    poles_coef = np.poly(poles_pos)
    print(zeros_coef ,poles_coef)
    Draw_transfer_function()



fig.on_event(Tap, Set_Coefs)
fig.on_event(MouseLeave, Set_Coefs)



# trans = plt.figure()
# plt.subplot(121)
# plt.loglog(f, abs(H))
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Amplitude')
# plt.subplot(122)
# plt.plot(f,phase)

#fig.grid()
x=column(ZeroPoleChoose,ResetButton,UndoButton,SaveButton,LoadButton)

x2 = column(fig)
x3 = column(mag_response,phase_response)
z=row(x , x2 , x3)

curdoc().add_root(row(z))


# Choosen="Zeros"
# LABELS = ["Zeros", "Poles"]
# ZeroPoleChoose = RadioGroup(labels=LABELS, active=1)
# ZeroPoleChoose.js_on_click(CustomJS(code="""
#     console.log('ZeroPoleChoose: active=' + this.active, this.toString())
# """))
# print(ZeroPoleChoose.active)
# index= 0 
# # def ChangeIndex(i):
# #     global index
# #     index = i
# # ZeroPoleChoose.on_click(ChangeIndex)
# ResetButton=Button(label="Reset",button_type="danger")
# UndoButton=Button(label="Undo",button_type="warning")
# SaveButton=Button(label="Save",button_type="success")
# LoadButton=Button(label="Load",button_type="success")


# fig = figure(title="Z Plane",x_range=(-1.1, 1.1), y_range=(-1.1, 1.1))  # sets size and makes it square
# fig.xaxis.axis_label ="Real"
# fig.yaxis.axis_label="Imaginary"
# ax=fig.axis


# theta = np.linspace(-np.pi, np.pi, 201)
# fig.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

# vline = Span(location=0, dimension='height', line_color='red', line_width=3)
# # Horizontal line
# hline = Span(location=0, dimension='width', line_color='red', line_width=3)

# fig.renderers.extend([vline, hline])

# # drag and drop
# p = figure(x_range=(0, 10), y_range=(0, 10), tools=[],
#            title='Point Draw Tool')
# p.background_fill_color = 'lightgrey'

# source = ColumnDataSource({
#     'x': [1, 5, 9], 'y': [1, 5, 9], 'color': ['red', 'green', 'yellow']
# })

# if index == 0:
#     renderer = p.scatter(x='x', y='y', source=source, color='color', size=10)
#     draw_tool = PointDrawTool(renderers=[renderer], empty_value='black')
# elif index == 1 :
#     renderer = p.scatter(x='x', y='y', source=source, color='color', size=10)
#     draw_tool = PointDrawTool(renderers=[renderer], empty_value='green')

# columns = [TableColumn(field="x", title="x"),
#            TableColumn(field="y", title="y"),
#            TableColumn(field='color', title='color')]
# table = DataTable(source=source, columns=columns, editable=True, height=200)

# p.add_tools(draw_tool)
# p.toolbar.active_tap = draw_tool



# x=column(ZeroPoleChoose,ResetButton,UndoButton,SaveButton,LoadButton)
# x2 = column(fig)
# x3 = column(p , table)
# z=row(x , x2 ,x3)
# show(z)
# curdoc().add_root(row(z))