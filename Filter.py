from itertools import count
from logging import Filter
from typing import List
from bokeh.core.enums import ButtonType, SizingMode
from bokeh.core.property.numeric import Size
from bokeh.io import show
from bokeh.models import CustomJS, RadioGroup,Button,Span,Slider ,Range1d , filters
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource
from bokeh.models.annotations import Label
from bokeh.models.widgets.groups import CheckboxGroup
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.layouts import grid
from bokeh.events import MouseMove, Tap ,MouseLeave
import numpy as np
import matplotlib.pyplot as plt
import math

Choosen="red"
Checkboxs=[]
Count=0
#Choosen="red"
zeros_coef = [1]
poles_coef = [1]
# zero_filter_coef =[]
# pole_filter_coef =[]
zero_filter_pos =[]
pole_filter_pos =[]
zero_filter_pos_conj =[]
pole_filter_pos_conj =[]
zero_filter_x =[]
zero_filter_y =[]
pole_filter_x =[]
pole_filter_y= []
conj = False
pole_filter_pos_active =[]
zero_filter_pos_active = []
H = []
phase =[]
f= []
Filters = CheckboxGroup(labels=Checkboxs)
Filters.js_on_click(CustomJS(code="""
    console.log('checkbox_group: active=' + this.active, this.toString())
"""))
LABELS = ["Zeros", "Poles"]
ZeroPoleChoose = RadioGroup(labels=LABELS, active=0)
ZeroPoleChoose.js_on_click(CustomJS(code="""
    console.log('ZeroPoleChoose: active=' + this.active, this.toString())
"""))

#UndoButton=Button(label="Undo",button_type="warning")
ResetButton=Button(label="Reset",button_type="danger")
ClearPoles=Button(label="Clear Poles",button_type="warning")
ClearZeros=Button(label="Clear Zeros",button_type="warning")

def Calculate_mag_and_phase(zeros_coef,poles_coef):
    global H , phase , f
    w = np.linspace(0,np.pi, 200)    # for evauluating H(w)
    z = np.exp(1j*w)
    f = np.linspace(0, 180, 200)         # for ploting H(w)
    H = np.polyval(zeros_coef, z) / np.polyval(poles_coef, z) 
    phase =  np.unwrap(np.angle(H))

Calculate_mag_and_phase(zeros_coef , poles_coef)
mag_response = figure(title="magnitude response ",plot_width=400, plot_height=400)
mag_response.xaxis.axis_label ="Frequency [Hz]"
mag_response.yaxis.axis_label="Amplitude"
mag_response.line(f, abs(H), line_width=2)

phase_response = figure(title="phase response " , plot_width=400, plot_height=400)
phase_response.xaxis.axis_label ="Frequency [Hz]"
phase_response.yaxis.axis_label="Phase"
phase_response.line(f, phase, line_width=2)

filter_response = figure(title="phase response " , plot_width=400, plot_height=400)
filter_response.xaxis.axis_label ="Frequency [Hz]"
filter_response.yaxis.axis_label="Phase"
#filter_response.line(f, phase, line_width=2)


def Draw_Circle_And_Axis(graph):

    graph.xaxis.axis_label ="Real"
    graph.yaxis.axis_label="Imaginary"
    ax=graph.axis
    theta = np.linspace(-np.pi, np.pi, 201)
    graph.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

    vline = Span(location=0, dimension='height', line_color='red', line_width=3)
    # Horizontal line
    hline = Span(location=0, dimension='width', line_color='red', line_width=3)

    graph.renderers.extend([vline, hline])

fig = figure(title="Z Plane",x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),plot_width=400, plot_height=400)  # sets size and makes it square
Draw_Circle_And_Axis(fig)

###raz3 btngana
all_pass = figure(title="Z Plane",x_range=(-3, 3), y_range=(-3, 3),plot_width=400, plot_height=400)  # sets size and makes it square
Draw_Circle_And_Axis(all_pass)

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

Zeros_conj = ColumnDataSource(
    data=dict(
        x = [], 
        y = []
    )
)

Poles_conj = ColumnDataSource(
    data=dict(
        x = [], 
        y = []
    )
)
def Draw_Zeros_And_Poles():

    ZerosRenderer = fig.scatter(x='x', y='y', source=Zeros, color='red', size=10)
    PolesRenderer = fig.cross(x='x', y='y', source=Poles, color='blue', size=10)
    ZerosRenderer_conj = fig.scatter(x='x', y='y', source=Zeros_conj, color='red', size=10)
    PolesRenderer_cong = fig.cross(x='x', y='y', source=Poles_conj, color='blue', size=10)

    draw_tool_1 = PointDrawTool(renderers=[ZerosRenderer,ZerosRenderer_conj],empty_value="red")
    draw_tool_2 = PointDrawTool(renderers=[PolesRenderer,PolesRenderer_cong], empty_value="blue")
    fig.add_tools(draw_tool_1,draw_tool_2)
    fig.toolbar.active_tap = draw_tool_1
    fig.toolbar.active_tap = draw_tool_2

Draw_Zeros_And_Poles()

# def update():
#     if ZeroPoleChoose.active==0:
#         Choosen=="red"

#     if ZeroPoleChoose.active==1:
#         Choosen=="blue"

# ZeroPoleChoose.on_change('active', lambda attr, old, new: update())


def Draw_transfer_function():

    mag_response.renderers=[]
    phase_response.renderers=[]
    zero_coef = zeros_coef
    pole_coef = poles_coef
    if type(zeros_coef) == float:
        zero_coef = [zeros_coef]

    if type(poles_coef) == float:
        pole_coef = [poles_coef]
    
    Calculate_mag_and_phase(zero_coef,pole_coef)

    mag_response.line(f, abs(H), line_width=2)
    mag_response.y_range=Range1d(min(abs(H)), max(abs(H)))
    mag_response.x_range=Range1d(min(f), max(f))

    phase_response.line(f, phase, line_width=2)
    phase_response.y_range=Range1d(min(phase), max(phase))
    phase_response.x_range=Range1d(min(f), max(f))




def Set_Coefs():
    global zeros_coef , poles_coef
    zeros_pos =[]
    poles_pos = []
    poles_pos_conj = []
    zeros_pos_conj = []
    Zeros_conj.data['x']=[]
    Zeros_conj.data['y']=[]
    Poles_conj.data['x']=[]
    Poles_conj.data['y']=[]
   
    for i in range(len(Zeros.data['x'])):
        zeros_pos.append(Zeros.data['x'][i]+1j*Zeros.data['y'][i])
        if conj:
            Zeros_conj.data['x']=Zeros.data['x']
            Zeros_conj.data['y']=-1*np.array(Zeros.data['y'])
            zeros_pos_conj.append(Zeros.data['x'][i]-1j*Zeros.data['y'][i])

    for i in range(len(Poles.data['x'])):
        poles_pos.append(Poles.data['x'][i]+1j*Poles.data['y'][i])
        if conj:
            Poles_conj.data['x']=Poles.data['x']
            Poles_conj.data['y']=-1*np.array(Poles.data['y'])
            poles_pos_conj.append(Poles.data['x'][i]-1j*Poles.data['y'][i])
    
    print(Poles.data['x'],Poles_conj.data['x'],poles_pos_conj)
    poles_coef = np.poly(poles_pos+pole_filter_pos_active+poles_pos_conj)
    zeros_coef = np.poly(zeros_pos+zero_filter_pos_active+zeros_pos_conj)
    
    Draw_transfer_function()



fig.on_event(Tap, Set_Coefs)
fig.on_event(MouseLeave, Set_Coefs)

def Add_All_pass_filter():
    x= real_slider.value
    y= img_slider.value
    #pole_filter_x.append(x)
    #pole_filter_y.append(y)
    pole_pos = x+1j*y
    pole_filter_pos.append(pole_pos)

    angle = math.atan(y/x)
    zero_x =(1/abs(pole_pos))*np.cos(angle)
    zero_y = (1/abs(pole_pos))*np.sin(angle)
    #zero_filter_x.append(zero_x)
    #zero_filter_y.append(zero_y)
    zero_filter_pos.append(zero_x+1j*zero_y)
    if conj:
        pole_filter_pos_conj.append(x-1j*y)
        zero_filter_pos_conj.append(zero_x-1j*zero_y)

    Set_Coefs()

def Plot_Filter_points():
    pole_x =real_slider.value
    pole_y =img_slider.value
    all_pass.renderers = []
    if pole_x:
        angle = math.atan(pole_y/pole_x)
        zero_x =(1/abs(pole_x+1j*pole_y))*np.cos(angle)
        zero_y =(1/ abs(pole_x+1j*pole_y))*np.sin(angle)
        if conj:
            X=[pole_x,pole_x,zero_x,zero_x]
            Y=[pole_y,-pole_y,zero_y,-zero_y]
            all_pass.circle(x=X, y=Y,color=['blue','blue','red','red'], size=10)
            Plot_Filter_response([pole_x+1j*pole_y,pole_x-1j*pole_y],[zero_x+1j*zero_y,zero_x+1j*zero_y])
        else:
            X=[pole_x,zero_x]
            Y=[pole_y,zero_y]
            all_pass.circle(x=X, y=Y,color=['blue','red'], size=10)
            Plot_Filter_response(pole_x+1j*pole_y,zero_x+1j*zero_y)


def Plot_Filter_response(p_pos,z_pos):
    if conj:
        pole_filter_coef = np.poly(p_pos)
        zero_filter_coef = np.poly(z_pos)
    else:
        pole_filter_coef = np.poly([p_pos])
        zero_filter_coef = np.poly([z_pos])

    filter_response.renderers=[]
    Draw_Circle_And_Axis(all_pass)
    Calculate_mag_and_phase(zero_filter_coef,pole_filter_coef)

    filter_response.line(f, phase, line_width=2)
    filter_response.y_range=Range1d(min(phase), max(phase))
    filter_response.x_range=Range1d(min(f), max(f))


def set_conj():
    global conj
    if conj == False:
        conj =True
    else:
        conj = False

    Zeros_conj.data = {k: [] for k in Zeros_conj.data}
    Poles_conj.data = {k: [] for k in Poles_conj.data}
    Set_Coefs()
    UpdateGUI()

conj_button=Button(label="enable /disable conjugate",button_type="success")
conj_button.on_click(set_conj)

def clearPoles(event):
    global Poles , Poles_conj
    Poles.data = {k: [] for k in Poles.data}
    Poles_conj.data = {k: [] for k in Poles_conj.data}
    #Poles = ColumnDataSource(dict(x=[],y=[]))
ClearPoles.on_click(clearPoles)

def clearZeros(event):
    global Zeros , Zeros_conj
    Zeros.data = {k: [] for k in Zeros.data}
    Zeros_conj.data = {k: [] for k in Zeros_conj.data}
    #Zeros = ColumnDataSource(dict(x=[],y=[]))

ClearZeros.on_click(clearZeros)

def Reset(event):
    global Poles , Poles_conj
    Poles.data = {k: [] for k in Poles.data}
    Poles_conj.data = {k: [] for k in Poles_conj.data}
    global Zeros , Zeros_conj
    Zeros.data = {k: [] for k in Zeros.data}
    Zeros_conj.data = {k: [] for k in Zeros_conj.data}
    #Zeros = ColumnDataSource(dict(x=[],y=[]))
ResetButton.on_click(Reset)

real_slider = Slider(start=-1, end=1, value=0, step=.01, title="Real")
img_slider = Slider(start=-1, end=1, value=0, step=.01, title="Imaginary")

def batata(attrname, old, new):
    Plot_Filter_points()

real_slider.on_change('value', batata)
img_slider.on_change('value', batata)


####Don't touch 
AddFilter=Button(label="Add Filter",button_type="success")
def AddFilterFunc(event):
    #print("1")
    Add_All_pass_filter()
    curdoc().clear()
    Add_All_pass_filter()
    global Checkboxs
    global Filters
    global Count
    activ=[0]
    if Count>0:
        activ.clear()
        activ=Filters.active
        activ.append(Count)
        #print(activ)
        #print(Filters.active)
    text="Filter"+str(len(Checkboxs)+1)
    Checkboxs.append(text)
    #fil.append(len(Checkboxs)-1)
    #Filters=CheckboxGroup(labels=Checkboxs)
    Filters=CheckboxGroup(labels=Checkboxs,active=activ)
    Count=Count+1
    Filters.js_on_click(CustomJS(code="""
    console.log('checkbox_group: active=' + this.active, this.toString())
    """))
<<<<<<< HEAD:circle.py
<<<<<<< HEAD
    Filters.on_change('active', lambda attr, old, new: ActivateFiltters())
=======
>>>>>>> 83425b8715e774709806cf7d8639faf43c9c11e7
=======
    ActivateFiltters()
>>>>>>> cde80da5ccdedd34081ac7c93134f430fa1f0f5e:Filter.py
    UpdateGUI()
    
AddFilter.on_click(AddFilterFunc)

def ActivateFiltters():
    global zero_filter_pos_active ,pole_filter_pos_active,pole_filter_pos,zero_filter_pos  
    
    list=Filters.active
    if conj:
        zero_filter_pos_active = [zero_filter_pos[i] for i in list] + [zero_filter_pos_conj[i] for i in list]
        pole_filter_pos_active = [pole_filter_pos[i] for i in list] + [pole_filter_pos_conj[i] for i in list]
    else:
        zero_filter_pos_active = [zero_filter_pos[i] for i in list] 
        pole_filter_pos_active = [pole_filter_pos[i] for i in list] 
    Set_Coefs()
    UpdateGUI()
    
#Filters.on_change('active', lambda attr, old, new: ActivateFiltters())
##### ha2tlk ya btngana
def UpdateGUI():
    curdoc().clear()
    x=column(ResetButton,ClearPoles,ClearZeros,conj_button)
    x2 = column(fig)
    z=row(x , x2)
    x3=column(real_slider,img_slider,AddFilter,Filters)
    x4=column(all_pass)
    z2=row(x3,x4)
    x5 = column( mag_response,filter_response)
    x6 =column(phase_response )
    z3=row(column(z,z2),x5,x6)
    curdoc().add_root(row(z3))
UpdateGUI()