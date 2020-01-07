import webbrowser
import os

errorCodes = [
    "No errors have been detected while parsing",                           #0
    "[ERROR] found an element of type {} closed with an {} tag on line {}"  #1
    "[ERROR] found an unknown tag type {} on line {}"                       #2
]

htmltags = [
    "html", "head", "body", "title", "p", "b", "i", "h2", "h3", "h4", "h5", "h6",
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
                    args = content[1:-1].split(" ", 1)
                    tagname = args.pop(0)
                    #parse args
                    for i, arg in enumerate(args):
                        arg = arg.split("=")
                        arg[0] = arg[0].strip()
                        arg[1] = arg[1].strip()
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

def printHTMLTree(DOM):
    print(stringifyDOM(DOM))

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

        argstring = ""
        for i in range(len(element.arguments)):
            arg = element.arguments[i]
            argstring += f" {arg[0]} = \"{arg[1]}\""

        if element.isSelfClosing:#self closing tag
            htmlstring+=f"{indentation}<{element.type}{argstring} />\n"

        elif not element.istext:#non self closing tag
            htmlstring+=f"{indentation}<{element.type}{argstring}>\n"
            htmlstring+=stringifyDOM(element, indent+1)
            htmlstring+=f"{indentation}</{element.type}>\n"
        else:#text
            htmlstring+=f"{indentation}{element.textContent}\n"
    if indent==0:
        return htmlstring.strip()
    else:
        return htmlstring

def renderDOM(DOM, outputfile):
    htmlstring = stringifyDOM(DOM)
    renderString(htmlstring, outputfile)

def loadSource(url):
    with open(f"{url}.html", "r+") as File:
        return File.read()

def allowTag(*tagnames):
    for tag in tagnames:
        htmltags.append(tag)