from bokeh.plotting import figure, output_file, show, Column
from random import random
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.core.enums import ButtonType, SizingMode
from bokeh.core.property.numeric import Size
from bokeh.io import show
from bokeh.models import CustomJS, RadioGroup,Button,Span , Slider
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource
from bokeh.models.annotations import Label
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.layouts import grid
from bokeh.events import MouseMove, Tap ,MouseLeave 
import numpy as np
import matplotlib.pyplot as plt
import math

#Choosen="red"
zeros_coef = [1]
poles_coef = [1]
zero_filter_coef =[]
pole_filter_coef =[]

LABELS = ["Zeros", "Poles"]
ZeroPoleChoose = RadioGroup(labels=LABELS, active=0)
ZeroPoleChoose.js_on_click(CustomJS(code="""
    console.log('ZeroPoleChoose: active=' + this.active, this.toString())
"""))

index= 0

ResetButton=Button(label="Reset",button_type="danger")

#UndoButton=Button(label="Undo",button_type="warning")
ClearPoles=Button(label="Clear Poles",button_type="warning")
ClearZeros=Button(label="Clear Poles",button_type="warning")

w = np.linspace(0,np.pi, 200)    # for evauluating H(w)
z = np.exp(1j*w)
f = np.linspace(0, 180, 200)         # for ploting H(w)
H = np.polyval(zeros_coef, z) / np.polyval(poles_coef, z) 
phase =  np.unwrap(np.angle(H))
mag_response = figure(title="magnitude response ",plot_width=400, plot_height=300)
mag_response.xaxis.axis_label ="Frequency [Hz]"
mag_response.yaxis.axis_label="Amplitude"
mag_response.line(f, abs(H), line_width=2)
phase_response = figure(title="phase response " , plot_width=400, plot_height=300)
phase_response.xaxis.axis_label ="Frequency [Hz]"
phase_response.yaxis.axis_label="Phase"
phase_response.line(f, phase, line_width=2)

fig = figure(title="Z Plane",x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),plot_width=450, plot_height=450)  # sets size and makes it square
fig.xaxis.axis_label ="Real"
fig.yaxis.axis_label="Imaginary"
ax=fig.axis

theta = np.linspace(-np.pi, np.pi, 201)
fig.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

vline = Span(location=0, dimension='height', line_color='red', line_width=3)
# Horizontal line
hline = Span(location=0, dimension='width', line_color='red', line_width=3)

fig.renderers.extend([vline, hline])

all_pass = figure(title="Z Plane",x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),plot_width=300, plot_height=300)  # sets size and makes it square
all_pass.xaxis.axis_label ="Real"
all_pass.yaxis.axis_label="Imaginary"
ax=all_pass.axis

theta = np.linspace(-np.pi, np.pi, 201)
all_pass.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

vline = Span(location=0, dimension='height', line_color='red', line_width=3)
# Horizontal line
hline = Span(location=0, dimension='width', line_color='red', line_width=3)

all_pass.renderers.extend([vline, hline])

# real_slider = Slider(start=-1, end=1, value=0, step=.01, title="Real")
# img_slider = Slider(start=-1, end=1, value=0, step=.01, title="Imaginary")
# def batata(val):
#     print(val)
#     print(real_slider.value)
# real_slider.on_change('value', batata)
#img_slider.on_change('value', callback1, callback2, ..., callback_n)


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
draw_tool=0
def addding_ZerosAndPloes(first,second):
    draw_tool. PointDrawTool(renderers=[ZerosRenderer])
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

def clearPoles(event):
    Poles.Poles = {k: [] for k in Poles.data}
    Poles = ColumnDataSource(dict(x=[],y=[]))
ClearPoles.on_event(clearPoles)


ZeroPoleChoose.on_click(ChangeIndex)
addding_ZerosAndPloes(ZerosRenderer,PolesRenderer)


def Draw_transfer_function():

    mag_response.renderers=[]
    phase_response.renderers=[]
    zero_coef = zeros_coef
    pole_coef = poles_coef
    if type(zeros_coef) == float:
        zero_coef = [zeros_coef]

    if type(poles_coef) == float:
        pole_coef = [poles_coef]
    

    all_zeros = np.concatenate((np.array(zero_coef) , np.array(zero_filter_coef)))
    all_poles = np.concatenate((np.array(pole_coef) , np.array(pole_filter_coef)))

    w = np.linspace(0,np.pi, 200)    # for evauluating H(w)
    z = np.exp(1j*w)
    f = np.linspace(0, 180, 200)         # for ploting H(w)
    H = np.polyval(all_zeros, z) / np.polyval(all_poles, z) 
    phase =  np.unwrap(np.angle(H))
    
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

def Add_All_pass_filter():
    x= 0.5
    y= 0.5
    pole_pos = x+1j*y
    pole_filter_coef.append(pole_pos)
    angle = math.atan(y/x)
    zero_x =abs(pole_pos)*np.cos(angle)
    zero_y = abs(pole_pos)*np.sin(angle)
    zero_filter_coef.append(zero_x+1j*zero_y)
    Plot_Filter_points()

def Plot_Filter_points():

    all_pass.circle(x=[1, 2], y=[1, 2],color=['blue','red'], size=20)

    


# trans = plt.figure()
# plt.subplot(121)
# plt.loglog(f, abs(H))
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Amplitude')
# plt.subplot(122)
# plt.plot(f,phase)

#fig.grid()
x=column(fig , ZeroPoleChoose,ResetButton,UndoButton,SaveButton,LoadButton)
#x=column(ZeroPoleChoose,ResetButton,UndoButton,SaveButton,LoadButton , real_slider ,img_slider)
x2 = column( mag_response,phase_response)
x3 = column( all_pass)
x4 =column()
z=row(x , x2 , x3)
# y=column(real_slider , img_slider)
# z2=row(y)
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