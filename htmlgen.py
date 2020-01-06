import webbrowser
import os

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
    if not string == "":
        string = string.splitlines()
        for tag in string:
            content = tag.strip()
            if content[0] == "<" and content[1] != "!":#if content is a tag and isnt doctype
                tagname = content[1:-1]
                if tagname[0] != "/":#if its not a closing tag
                    head.haschildren = True
                    head.children.append(HTML(tagname))
                    DOMHIST.append(head)
                    head = head.children[-1]
                else:
                    head = DOMHIST.pop()

    return DOM

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