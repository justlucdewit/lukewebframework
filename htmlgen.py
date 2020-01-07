import webbrowser
import os

errorCodes = [
    "No errors have been detected while parsing",                           #0
    "[ERROR] found an element of type {} closed with an {} tag on line {}"  #1
]

class Component:
    def __init__(self):
        pass

    def render():
        pass

class HTML:
    def __init__(self, type="dom"):
        #set elemental properties
        self.type = type
        self.istext = False
        self.textContent = ""
        
        self.children = []
        self.haschildren = False
        
        self.arguments = []
        

def HTMLparse(string):
    DOM = HTML()
    DOMHIST = []
    head = DOM
    errors = []
    if not string == "":
        string = string.splitlines()
        for lineNumber, tag in enumerate(string):
            content = tag.strip()
            if content[1] != "!":#if content is a tag and isnt doctype
                if content[0] == "<":
                    tagname = content[1:-1]
                else:
                    tagname = content
                    head.haschildren = True
                    txt = HTML("text")
                    txt.istext = True
                    txt.textContent = tagname
                    head.children.append(txt)
                    continue
                if tagname[0] != "/":#if its not a closing tag
                    head.haschildren = True
                    head.children.append(HTML(tagname))
                    DOMHIST.append(head)
                    head = head.children[-1]
                else:#a closing tag has been found
                    if tagname[1:] != head.type:
                        print(head.istext)
                        errors.append(errorCodes[1].format(head.type, tagname[1:], lineNumber))
                        return DOM, errors
                    head = DOMHIST.pop()
    return DOM, [errorCodes[0]]

def printHTMLTree(DOM, indent=0):
    if DOM.haschildren:
        for element in DOM.children:
            indentation = ""
            for i in range(indent):
                indentation+="| "
            if not element.type == "text":
                print(f"{indentation}<{element.type}>")
            else:
                print(f"{indentation}{element.textContent}")
            if element.haschildren:
                printHTMLTree(element, indent+1)

def renderString(string, output):
    with open(output, "w+") as File:
        File.write(string)

    webbrowser.open(f'file://{os.path.realpath(output)}')

def renderDOM(DOM, outputfile):
    pass