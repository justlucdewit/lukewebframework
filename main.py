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

html = HTML(website)

#renderString(website, "test.html")