#Lead, a markdown renderer
#Copyright Pittab 2025
#Producesyntaxed by EyeScary-Development

#imports
import producesyntaxed
from typing import List, Any


#Kinda self explanatory, makes bullet list strings and rerenders them for things like bold tags and strikethroughs
def bulletlist(item):
    splititem=item.split()
    splititem.pop(0)
    render([str("- " + ' '.join(splititem))], rerender=True)

#Processes bold text
def bold(line):
    line=line.split("*")
    bolds = [line[i] for i in range(len(line)) if i % 2 != 0]
    for item in line:
        if item not in bolds:
            render([item], rerender=True)
        else:
            producesyntaxed.producesyntaxed(item, 'aqua', True, False)

#Processes strikethroughs
def strikethrough(line):
    line=line.split("~~")
    tostrike = [line[i] for i in range(len(line)) if i % 2 != 0]
    for item in line:
        if item not in tostrike:
            render([item], rerender=True)
        else:
            producesyntaxed.producesyntaxed(item, 'grey', True, False)

#Processes headings TODO: maybe H6 and H5?
def heading(line):
    print()
    line=line.split()
    if line[0] == "#":
        line.pop(0)
        producesyntaxed.producesyntaxed(' '.join(line), 'blue2', False, True)
    if line[0] == "##":
        line.pop(0)
        producesyntaxed.producesyntaxed(' '.join(line), 'blue', False, True)
    if line[0] == "###":
        line.pop(0)
        producesyntaxed.producesyntaxed(' '.join(line), 'aqua', False, True)
    if line[0] == "####":
        line.pop(0)
        print(' '.join(line))

#Run this command to render le text
def render(input_list: List[Any], rerender=False):
    for item in input_list:
        match item:
            case x if x.startswith("#"):
                heading(item.strip("\n"))
            case x if x.startswith("*"):
                if item.startswith ("* ") != True:
                    bold(item.strip("\n"))
                else:
                    bulletlist(item.strip("\n"))
            case x if "*" in x:
                bold(item.strip("\n"))
            case x if "~~" in x:
                strikethrough(item.strip("\n"))
            case _:
                print(item.strip("\n"), end='')
        if rerender != True:
            print()

