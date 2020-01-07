from htmlgen import *

#define source code
website = loadSource("./source")

#get dom object and errors
DOM, errors = HTMLparse(website)

#error handling
for err in errors:
    print(err)
print()

#render the page
printHTMLTree(DOM)
renderDOM(DOM, "test.html")