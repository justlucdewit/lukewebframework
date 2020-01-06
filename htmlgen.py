import webbrowser
import os

class HTML:
    def __init__(self, string = ""):
        self.children = []
        self.haschildren = False

        if not string == "":
            string = string.splitlines()
            for tag in string:
                content = tag.strip()
                if content[0] == "<" and content[1] != "/" and content[1] != "!":
                    print(content[1:-1])
                    
def renderString(string, output):
    with open(output, "w+") as File:
        File.write(string)

    webbrowser.open(f'file://{os.path.realpath(output)}')