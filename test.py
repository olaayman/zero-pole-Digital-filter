# #%reset -f
# from IPython.display import HTML, display, Markdown
# import ipywidgets as widgets

# #%reset -f
# from IPython.display import HTML, display, Markdown
# import ipywidgets as widgets

# HTML(
#     '<style>'
#         '#notebook { padding-top:0px !important; } ' 
#         '.container { width:100% !important; } '
#         '.end_space { min-height:0px !important; } '
#     '</style>'
# );
# HTML ('''<script>
#   function code_toggle() {
#     if (code_shown){
#       $('div.input').hide('500');
#       $('#toggleButton').val('Show Code')
#     } else {
#       $('div.input').show('500');
#       $('#toggleButton').val('Hide Code')
#     }
#     code_shown = !code_shown
#   }

#   $( document ).ready(function(){
#     code_shown=false;
#     $('div.input').hide()
#   });
# </script>
# <form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Show Code"></form>''')
import numpy as np
x= np.array([0,1,2])
x = 3
xx = [x]
y = np.array([3,4,5])
z = np.concatenate((xx,y))
print(z)