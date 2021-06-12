from bokeh.core.enums import ButtonType, SizingMode
from bokeh.core.property.numeric import Size
from bokeh.io import show
from bokeh.models import CustomJS, RadioGroup,Button
from bokeh.models.annotations import Label
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.layouts import grid

LABELS = ["Zeros", "Poles"]
ZeroPoleChoose = RadioGroup(labels=LABELS, active=0)
ZeroPoleChoose.js_on_click(CustomJS(code="""
    console.log('ZeroPoleChoose: active=' + this.active, this.toString())
"""))
ResetButton=Button(label="Reset",button_type="danger")
UndoButton=Button(label="Undo",button_type="warning")
SaveButton=Button(label="Save",button_type="success")
LoadButton=Button(label="Load",button_type="success")


x=column(ZeroPoleChoose,ResetButton,UndoButton,SaveButton,LoadButton)
z=row(x)
#show(ZeroPoleChoose)
show(z)