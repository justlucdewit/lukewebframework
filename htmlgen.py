import webbrowser
import os

errorCodes = [
    "No errors have been detected while parsing",                           #0
    "[ERROR] found an element of type {} closed with an {} tag on line {}"  #1
]

class HTML:
    def __init__(self, type="dom"):
        #set elemental properties
        self.type = type
        self.children = []
        self.haschildren = False

def HTMLparse(string):
    DOM = HTML()
    DOMHIST = []
    head = DOM
    errors = []
    if not string == "":
        string = string.splitlines()
        for lineNumber, tag in enumerate(string):
            content = tag.strip()
            if content[0] == "<" and content[1] != "!":#if content is a tag and isnt doctype
                tagname = content[1:-1]
                if tagname[0] != "/":#if its not a closing tag
                    head.haschildren = True
                    head.children.append(HTML(tagname))
                    DOMHIST.append(head)
                    head = head.children[-1]
                else:#a closing tag has been found
                    if tagname[1:] != head.type:
                        errors.append(errorCodes[1].format(head.type, tagname[1:], lineNumber))
                        return DOM, errors
                    head = DOMHIST.pop()
    return DOM, [errorCodes[0]]

def printHTMLTree(DOM, indent=0):
    if DOM.haschildren:
        for element in DOM.children:
            indentation = ""
            for i in range(indent):
                indentation+="  "
            print(f"{indentation}{element.type}")
            if element.haschildren:
                printHTMLTree(element, indent+1)

def renderString(string, output):
    with open(output, "w+") as File:
        File.write(string)

    webbrowser.open(f'file://{os.path.realpath(output)}')