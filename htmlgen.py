import webbrowser
import os

errorCodes = [
    "No errors have been detected while parsing",                           #0
    "[ERROR] found an element of type {} closed with an {} tag on line {}"  #1
]

htmltags = [
    "html",
    "head",
    "body",
    "title",
    "p",
    "b",
    "i"
]

class Component:
    def __init__(self):
        pass

    def render(self):
        pass

class HTML:
    def __init__(self, type="dom"):
        #set elemental properties
        self.type = type
        self.istext = False
        self.textContent = ""
        self.isSelfClosing = False
        
        self.children = []
        self.haschildren = False
        
        self.arguments = {}
        

def HTMLparse(string):
    DOM = HTML()
    DOMHIST = []
    head = DOM
    errors = []
    if not string == "":
        string = string.splitlines()
        for lineNumber, tag in enumerate(string):
            content = tag.strip()
            if content[1] != "!":#isnt doctype
                if content[0] == "<":
                    #sepperate args from tag name
                    args = content[1:-1].split(" ")
                    tagname = args.pop(0)

                    #parse args
                    for i, arg in enumerate(args):
                        arg = arg.split("=")
                        arg[1] = arg[1][1:-1]
                        args[i] = [arg[0], arg[1]]

                else:#handeling strings
                    tagname = content
                    head.haschildren = True
                    txt = HTML("text")
                    txt.istext = True
                    txt.textContent = tagname
                    head.children.append(txt)
                    continue
                if tagname[-1] == "/": #self closing tags
                    head.haschildren = True
                    tag = HTML(tagname[0:-1])
                    for arg in args:
                        tag.arguments[arg[0]] = arg[1]
                    tag.isSelfClosing = True
                    head.children.append(tag)
                elif tagname[0] != "/":#non self closing tags
                    head.haschildren = True
                    tag = HTML(tagname)
                    for i, arg in enumerate(args):
                        tag.arguments[i] = arg
                    head.children.append(tag)
                    DOMHIST.append(head)
                    head = head.children[-1]
                else:#closing tag
                    if tagname[1:] != head.type:
                        errors.append(errorCodes[1].format(head.type, tagname[1:], lineNumber))
                        return DOM, errors
                    head = DOMHIST.pop()
    return DOM, [errorCodes[0]]




def printHTMLTree(DOM, indent=0):
    if DOM.haschildren:
        for element in DOM.children:
            argstring = ""
            print(element.arguments)

            indentation = ""
            for i in range(indent):
                indentation+="  "
            
            if element.isSelfClosing:
                print(f"{indentation}<{element.type} />\n")
            elif not element.type == "text":#non self closing tag
                print(f"{indentation}<{element.type}>")
            else:#text
                print(f"{indentation}{element.textContent}")
            if element.haschildren:
                printHTMLTree(element, indent+1)

def renderString(string, output):
    with open(output, "w+") as File:
        File.write(string)

    webbrowser.open(f'file://{os.path.realpath(output)}')

def stringifyDOM(DOM, indent=0):
    htmlstring = ""
    for element in DOM.children:
        indentation = ""
        for i in range(indent):
            indentation+="\t"
        if element.isSelfClosing:
            htmlstring+=f"{indentation}<{element.type} />\n"

        elif not element.istext:#non self closing tag
            htmlstring+=f"{indentation}<{element.type}>\n"
            htmlstring+=stringifyDOM(element, indent+1)
            htmlstring+=f"{indentation}</{element.type}>\n"
        else:#text
            htmlstring+=f"{indentation}{element.textContent}\n"
    return htmlstring

def renderDOM(DOM, outputfile):
    htmlstring = stringifyDOM(DOM)
    renderString(htmlstring, outputfile)

def loadSource(url):
    with open(f"{url}.html", "r+") as File:
        return File.read()