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
from bokeh.plotting import figure, output_file, show, Column
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource
from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc



Choosen="Zeros"
LABELS = ["Zeros", "Poles"]
ZeroPoleChoose = RadioGroup(labels=LABELS, active=1)
ZeroPoleChoose.js_on_click(CustomJS(code="""
    console.log('ZeroPoleChoose: active=' + this.active, this.toString())
"""))
print(ZeroPoleChoose.active)
index= 0 
# def ChangeIndex(i):
#     global index
#     index = i
# ZeroPoleChoose.on_click(ChangeIndex)
ResetButton=Button(label="Reset",button_type="danger")
UndoButton=Button(label="Undo",button_type="warning")
SaveButton=Button(label="Save",button_type="success")
LoadButton=Button(label="Load",button_type="success")


fig = figure(title="Z Plane",x_range=(-1.1, 1.1), y_range=(-1.1, 1.1))  # sets size and makes it square
fig.xaxis.axis_label ="Real"
fig.yaxis.axis_label="Imaginary"
ax=fig.axis


theta = np.linspace(-np.pi, np.pi, 201)
fig.line(np.sin(theta), np.cos(theta), color = 'gray', line_width=3)

vline = Span(location=0, dimension='height', line_color='red', line_width=3)
# Horizontal line
hline = Span(location=0, dimension='width', line_color='red', line_width=3)

fig.renderers.extend([vline, hline])

# drag and drop
p = figure(x_range=(0, 10), y_range=(0, 10), tools=[],
           title='Point Draw Tool')
p.background_fill_color = 'lightgrey'

source = ColumnDataSource({
    'x': [1, 5, 9], 'y': [1, 5, 9], 'color': ['red', 'green', 'yellow']
})

if index == 0:
    renderer = p.scatter(x='x', y='y', source=source, color='color', size=10)
    draw_tool = PointDrawTool(renderers=[renderer], empty_value='black')
elif index == 1 :
    renderer = p.scatter(x='x', y='y', source=source, color='color', size=10)
    draw_tool = PointDrawTool(renderers=[renderer], empty_value='green')

columns = [TableColumn(field="x", title="x"),
           TableColumn(field="y", title="y"),
           TableColumn(field='color', title='color')]
table = DataTable(source=source, columns=columns, editable=True, height=200)

p.add_tools(draw_tool)
p.toolbar.active_tap = draw_tool



x=column(ZeroPoleChoose,ResetButton,UndoButton,SaveButton,LoadButton)
x2 = column(fig)
x3 = column(p , table)
z=row(x , x2 ,x3)
show(z)
curdoc().add_root(row(z))