##Run as a script in Notepad++ using PythonScript plugin!##

##Simple counter, used to attach page numbers to pagebreaks.##

from Npp import *

counter = 0

def repl_with_counter(m):
    global counter
    counter += 1
    return "<pb n='{}'/>".format(counter)

editor.rereplace(r'<pb/>', repl_with_counter)