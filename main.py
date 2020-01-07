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
    </body>
</html>
'''

DOM, errors = HTMLparse(website)

for err in errors:
    print(err)

print()
printHTMLTree(DOM)
#renderString(website, "test.html")