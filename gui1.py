from bokeh.core.enums import ButtonType, SizingMode
from bokeh.core.property.numeric import Size
from bokeh.io import show
from bokeh.models import CustomJS, RadioGroup,Button,Span
from bokeh.models.annotations import Label
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.layouts import grid
import numpy as np
import matplotlib.pyplot as plt


Choosen="Zeros"
LABELS = ["Zeros", "Poles"]
ZeroPoleChoose = RadioGroup(labels=LABELS, active=0)
ZeroPoleChoose.js_on_click(CustomJS(code="""
    console.log('ZeroPoleChoose: active=' + this.active, this.toString())
"""))
ResetButton=Button(label="Reset",button_type="danger")
UndoButton=Button(label="Undo",button_type="warning")
SaveButton=Button(label="Save",button_type="success")
LoadButton=Button(label="Load",button_type="success")
fig = figure(title="Z Plane",x_range=(-1.1, 1.1), y_range=(-1.1, 1.1))  # sets size and makes it square
fig.xaxis.axis_label ="Real"
fig.yaxis.axis_label="Imaginary"
ax=fig.axis
#fig.legend(loc='upper left')
#ax = fig.axes()
# plot unit circle
#axis=fig.add_subplot(1,1,1)
theta = np.linspace(-np.pi, np.pi, 201)
fig.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

vline = Span(location=0, dimension='height', line_color='red', line_width=3)
# Horizontal line
hline = Span(location=0, dimension='width', line_color='red', line_width=3)

fig.renderers.extend([vline, hline])
#axis.add_patch(x)
# plot x-y axis
#ax.axhline(y=0, color='gray', linewidth=1)
#ax.axvline(x=0, color='gray', linewidth=1)
#r = fig.circle(0,0,radius=1,fill_color=None,line_color='OliveDrab')
#plt.title("Z Plane")

#fig.grid()
x=column(ZeroPoleChoose,ResetButton,UndoButton,SaveButton,LoadButton)

x2 = column(fig)
z=row(x , x2)
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
show(z)