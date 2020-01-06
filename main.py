from htmlgen import *

website = '''<!DOCTYPE html>
<html>
    <head>
        <title>
            htmlgen test
        </title>
    </head>
    <body>
        this is a website generated with my own framework
    </nav>
</html>
'''

DOM, errors = HTMLparse(website)

for err in errors:
    print(err)

print()
printHTMLTree(DOM)

#renderString(website, "test.html")


class Women:
    def __init__(self, age):
        self.inside = []

    def cook(self):
        pass
    
    def insertObject(self, obj):
        self.inside.append(obj)

    def pleasureOther(self, other):
        self.insertObject(self, other.dick())