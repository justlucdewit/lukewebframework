from htmlgen import *

website = '''<!DOCTYPE html>
<html>
    <head>
        <title>
            htmlgen test
        </title>
    </head>
    <body>
        single tag test
        <br/>
    </body>
</html>
'''

DOM, errors = HTMLparse(website)

#error handling
for err in errors:
    print(err)
print()

#renderthe page
renderDOM(DOM, "test.html")

#renderString(website, "test.html")
