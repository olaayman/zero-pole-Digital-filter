from logging import Filter
from bokeh.core.enums import ButtonType, SizingMode
from bokeh.core.property.numeric import Size
from bokeh.io import show
from bokeh.models import CustomJS, RadioGroup,Button,Span,Slider ,Range1d
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

#Choosen="red"
zeros_coef = [1]
poles_coef = [1]
# zero_filter_coef =[]
# pole_filter_coef =[]
zero_filter_pos =[]
pole_filter_pos =[]
zero_filter_x =[]
zero_filter_y =[]
pole_filter_x =[]
pole_filter_y= []
conj = False
Filters=CheckboxGroup(labels=Checkboxs)
Filters.js_on_click(CustomJS(code="""
    console.log('checkbox_group: active=' + this.active, this.toString())
"""))
LABELS = ["Zeros", "Poles"]
ZeroPoleChoose = RadioGroup(labels=LABELS, active=0)
ZeroPoleChoose.js_on_click(CustomJS(code="""
    console.log('ZeroPoleChoose: active=' + this.active, this.toString())
"""))

#UndoButton=Button(label="Undo",button_type="warning")
ClearPoles=Button(label="Clear Poles",button_type="warning")
ClearZeros=Button(label="Clear Zeros",button_type="warning")

###raz3 ola 
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
filter_response = figure(title="phase response " , plot_width=300, plot_height=300)
filter_response.xaxis.axis_label ="Frequency [Hz]"
filter_response.yaxis.axis_label="Phase"
#filter_response.line(f, phase, line_width=2)




def Draw_Circle_And_Axis(graph):

    theta = np.linspace(-np.pi, np.pi, 201)
    graph.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

    vline = Span(location=0, dimension='height', line_color='red', line_width=3)
    # Horizontal line
    hline = Span(location=0, dimension='width', line_color='red', line_width=3)

    graph.renderers.extend([vline, hline])

fig = figure(title="Z Plane",x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),plot_width=400, plot_height=400)  # sets size and makes it square
fig.xaxis.axis_label ="Real"
fig.yaxis.axis_label="Imaginary"
ax=fig.axis
Draw_Circle_And_Axis(fig)
#fig.legend(loc='upper left')
#ax = fig.axes()
#plot unit circle
#axis=fig.add_subplot(1,1,1)

###raz3 btngana
all_pass = figure(title="Z Plane",x_range=(-3, 3), y_range=(-3, 3),plot_width=400, plot_height=400)  # sets size and makes it square
all_pass.xaxis.axis_label ="Real"
all_pass.yaxis.axis_label="Imaginary"
ax=all_pass.axis
Draw_Circle_And_Axis(all_pass)
# theta = np.linspace(-np.pi, np.pi, 201)
# all_pass.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

# vline = Span(location=0, dimension='height', line_color='red', line_width=3)
# # Horizontal line
# hline = Span(location=0, dimension='width', line_color='red', line_width=3)

# all_pass.renderers.extend([vline, hline])

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
    #PolesRenderer_conj = fig.scatter(x='x', y= -'y', source=Poles, color='green', size=10)

    draw_tool_1 = PointDrawTool(renderers=[ZerosRenderer,ZerosRenderer_conj],empty_value="red")
    draw_tool_2 = PointDrawTool(renderers=[PolesRenderer,PolesRenderer_cong], empty_value="blue")
    fig.add_tools(draw_tool_1,draw_tool_2)
    fig.toolbar.active_tap = draw_tool_1
    fig.toolbar.active_tap = draw_tool_2

Draw_Zeros_And_Poles()

def update():
    if ZeroPoleChoose.active==0:
        Choosen=="red"
        #print("11")
    if ZeroPoleChoose.active==1:
        Choosen=="blue"
        #print("22")
ZeroPoleChoose.on_change('active', lambda attr, old, new: update())
ResetButton=Button(label="Reset",button_type="danger")

def Draw_transfer_function():

    mag_response.renderers=[]
    phase_response.renderers=[]
    zero_coef = zeros_coef
    pole_coef = poles_coef
    if type(zeros_coef) == float:
        #print("z float")
        zero_coef = [zeros_coef]

    if type(poles_coef) == float:
        #print("p float")
        pole_coef = [poles_coef]
    

    # all_zeros = np.concatenate((np.array(zero_coef) , np.array(zero_filter_coef)))
    # all_poles = np.concatenate((np.array(pole_coef) , np.array(pole_filter_coef)))

    w = np.linspace(0,np.pi, 200)    # for evauluating H(w)
    z = np.exp(1j*w)
    f = np.linspace(0, 180, 200)         # for ploting H(w)
    H = np.polyval(zero_coef, z) / np.polyval(pole_coef, z) 
    phase =  np.unwrap(np.angle(H))
    
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
    #fig.renderers=[]
    #Draw_Circle_And_Axis(fig)
    #Draw_Zeros_And_Poles()
    #UpdateGUI()
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
    print(poles_pos_conj)

    poles_coef = np.poly(poles_pos+pole_filter_pos+poles_pos_conj)
    zeros_coef = np.poly(zeros_pos+zero_filter_pos+zeros_pos_conj)
    #if conj:
        # data_pole =np.array(Poles.data['y'])
        # data_zero = np.array(Zeros.data['y'])
        #fig.circle(x=Poles.data['x'], y=-1*data_pole,color='blue', size=10)
        #fig.circle(x=Zeros.data['x'], y=-1*data_zero,color='red', size=10)
    # else:
    #     poles_coef = np.poly(poles_pos+pole_filter_pos)
    #     zeros_coef = np.poly(zeros_pos+zero_filter_pos)

    #print("coefs",zeros_coef ,poles_coef)

    #UpdateGUI()
    Draw_transfer_function()



fig.on_event(Tap, Set_Coefs)
fig.on_event(MouseLeave, Set_Coefs)

def Add_All_pass_filter():
    x= real_slider.value
    y= img_slider.value
    pole_filter_x.append(x)
    pole_filter_y.append(y)
    pole_pos = x+1j*y
    pole_filter_pos.append(pole_pos)

    angle = math.atan(y/x)
    zero_x =(1/abs(pole_pos))*np.cos(angle)
    zero_y = (1/abs(pole_pos))*np.sin(angle)
    zero_filter_x.append(zero_x)
    zero_filter_y.append(zero_y)
    zero_filter_pos.append(zero_x+1j*zero_y)
    if conj:
        pole_filter_pos.append(x-1j*y)
        zero_filter_pos.append(zero_x-1j*zero_y)
    Set_Coefs()

def Plot_Filter_points():
    pole_x =real_slider.value
    pole_y =img_slider.value
    all_pass.renderers = []
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

    #plt.plot(zero_filter_coef,pole_filter_coef)
    filter_response.renderers=[]
    Draw_Circle_And_Axis(all_pass)

    w = np.linspace(0,np.pi, 200)    # for evauluating H(w)
    z = np.exp(1j*w)
    f = np.linspace(0, 180, 200) 
    mag = np.polyval(zero_filter_coef, z) / np.polyval(pole_filter_coef, z) 
    phase =  np.unwrap(np.angle(mag))
    #print(phase)
    filter_response.line(f, phase, line_width=2)
    filter_response.y_range=Range1d(min(phase), max(phase))
    filter_response.x_range=Range1d(min(f), max(f))

# def Add_All_pass_filter():
#     x= real_slider.value
#     y= img_slider.value
#     pole_filter_x.append(x)
#     pole_filter_y.append(y)
#     pole_pos = x+1j*y
#     pole_filter_pos.append(pole_pos)
#     angle = math.atan(y/x)
#     zero_x =(1/abs(pole_pos))*np.cos(angle)
#     zero_y = (1/abs(pole_pos))*np.sin(angle)
#     zero_filter_x.append(zero_x)
#     zero_filter_y.append(zero_y)
#     zero_filter_pos.append(zero_x+1j*zero_y)
#     Set_Coefs()

# def Plot_Filter_points():
#     pole_x =real_slider.value
#     pole_y =img_slider.value
#     all_pass.renderers = []
#     angle = math.atan(pole_y/pole_x)
#     zero_x =(1/abs(pole_x+1j*pole_y))*np.cos(angle)
#     zero_y =(1/ abs(pole_x+1j*pole_y))*np.sin(angle)
#     X=[pole_x,zero_x]
#     Y=[pole_y,zero_y]
#     all_pass.circle(x=X, y=Y,color=['blue','red'], size=15)
#     Plot_Filter_response(pole_x+1j*pole_y,zero_x+1j*zero_y)


# def Plot_Filter_response(p_pos,z_pos):
#     zero_filter_coef = np.poly([z_pos])
#     pole_filter_coef = np.poly([p_pos])
#     plt.plot(zero_filter_coef,pole_filter_coef)
#     filter_response.renderers=[]
#     Draw_Circle_And_Axis(all_pass)
#     # theta = np.linspace(-np.pi, np.pi, 201)
#     # all_pass.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

#     # vline = Span(location=0, dimension='height', line_color='red', line_width=3)
#     # # Horizontal line
#     # hline = Span(location=0, dimension='width', line_color='red', line_width=3)

#     # all_pass.renderers.extend([vline, hline])
#     zero_coef = zero_filter_coef
#     pole_coef = pole_filter_coef
#     if type(zero_filter_coef) == float:
#         print("z float")
#         zero_coef = [zero_filter_coef]

#     if type(pole_filter_coef) == float:
#         print("p float")
#         pole_coef = [pole_filter_coef]
#     w = np.linspace(0,np.pi, 200)    # for evauluating H(w)
#     z = np.exp(1j*w)
#     f = np.linspace(0, 180, 200) 
#     mag = np.polyval(zero_filter_coef, z) / np.polyval(pole_filter_coef, z) 
#     phase =  np.unwrap(np.angle(mag))
#     #print(phase)
#     filter_response.line(f, phase, line_width=2)


def activateFilters():
    global zero_filter_pos ,pole_filter_pos ,zero_filter_x ,zero_filter_y ,pole_filter_x ,pole_filter_y    
    zero_filter_pos1 =[]
    pole_filter_pos1 =[]
    zero_filter_x1 =[]
    zero_filter_y1 =[]
    pole_filter_x1 =[]
    pole_filter_y1= []
    for active in Filters.active:
        zero_filter_pos1.append(zero_filter_pos[active])
        pole_filter_pos1.append(pole_filter_pos[active])
        zero_filter_x1.append(zero_filter_x[active])
        zero_filter_y1.append(zero_filter_y[active])
        pole_filter_x1.append(pole_filter_x[active])
        pole_filter_y1.append(pole_filter_y[active])
    zero_filter_pos= zero_filter_pos1
    pole_filter_pos= pole_filter_pos1 
    zero_filter_x = zero_filter_x1 
    zero_filter_y = zero_filter_y1 
    pole_filter_x = pole_filter_x1 
    pole_filter_y = pole_filter_y1

def set_conj():
    global conj
    if conj == False:
        conj =True
    else:
        conj = False

    Zeros_conj.data = {k: [] for k in Zeros_conj.data}
    Poles_conj.data = {k: [] for k in Poles_conj.data}
    Set_Coefs()

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

#batata labsa tar7a 7lwa w jeba 7lwa
def batata(attrname, old, new):
    #print(real_slider.value)
    Plot_Filter_points()
    #Plot_Filter_response()

real_slider.on_change('value', batata)
img_slider.on_change('value', batata)


####Don't touch 
AddFilter=Button(label="Add Filter",button_type="success")
def AddFilterFunc(event):
    #print("1")
    curdoc().clear()
    global Checkboxs
    global Filters
    text="Filter"+str(len(Checkboxs)+1)
    Checkboxs.append(text)
    #fil.append(len(Checkboxs)-1)
    #Filters=CheckboxGroup(labels=Checkboxs)
    Filters=CheckboxGroup(labels=Checkboxs,active=[len(Checkboxs)-1])
    Filters.js_on_click(CustomJS(code="""
    console.log('checkbox_group: active=' + this.active, this.toString())
    """))
    Add_All_pass_filter()
    UpdateGUI()
AddFilter.on_click(AddFilterFunc)
Filters.on_click(activateFilters)
##### ha2tlk ya btngana
def UpdateGUI():
    curdoc().clear()
    x=column(ResetButton,ClearPoles,ClearZeros,conj_button)
    x2 = column(fig)
    z=row(x , x2)
    x3=column(real_slider,img_slider,AddFilter,Filters)
    x4=column(all_pass)
    z2=row(x3,x4)
    x5 = column( mag_response,phase_response)
    x6 =column(filter_response)
    z3=row(column(z,z2),x5,x6)
    curdoc().add_root(row(z3))
UpdateGUI()


#fig.grid()
#show(ZeroPoleChoose)
# p = figure(x_range=(-1.5, 1.5), y_range=(-1.5, 1.5), toolbar_location=None)
# p.border_fill_color = 'white'
# p.background_fill_color = 'white'
# p.outline_line_color = None
# p.grid.grid_line_color = None

# # add a text renderer to the plot (no data yet)
# r = p.circle(0,0,radius=1,fill_color=None,line_color='OliveDrab')
# # r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="26px",
# #            text_baseline="middle", text_align="center")
# x=column(ZeroPoleChoose,ResetButton,UndoButton,SaveButton,LoadButton)