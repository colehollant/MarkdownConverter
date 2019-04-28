#!/usr/bin/python3

import sys

'''

    This is just a lil diddy I threw together to convert markdown to 
    both latex and html with jax!
    This is just for my ease of use, and should be used through the associated script
    If you wanna use it, feeeeeel free!

'''

htmlLines = []
texLines = []
# dirname = "test"
# mdname = dirname+"/"+dirname+".md"
# htmlname = dirname+"/"+dirname+".html"
# cssname = dirname+"/"+"markdown.css"
# texname = dirname+"/"+dirname+".tex"
inCodeBlock = False


###############################################################################
###############################################################################
########
########                 BEGIN HTML
########
###############################################################################
###############################################################################

def findAll(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def findAllStr(source, s):
    l = len(s)
    inds = []
    for i in range(0, len(source)):
        if s == source[i:i+l]:
            inds.append(i)
    return inds

def checkHeaderHTML(line):
    isHeader = False
    newLine = ""
    if line.startswith('#'):
        isHeader = True
        num = 0
        for i in range(0, len(line)):
            if line[i] is '#':
                num+=1
        newLine = "<h"+str(num)+">"+line[num:].strip()+"</h"+str(num)+">"
    return isHeader, newLine

def checkListHTML(line):
    isList = False
    newLine = ""
    if line.startswith('* '):
        isList = True
        newLine = "<ul>&bull; "+line[1:].strip()+"</ul>"
    elif line[0].isdigit():
        i = 0
        num = ""
        while i < len(line) and line[i].isdigit():
            num+=line[i]
            i+=1
        if i < len(line) and line[i] is ".":
            isList = True
            newLine = "<ul>"+str(num)+line[i:]+"</ul>"
    return isList, newLine

def processNewPageHTML(line):
    isNewLine = False
    newLine = ""
    if line.startswith("@@N"):
        isNewLine = True
        # newLine = "<div class=\"newpage\"></div>" #this gives whitespace
        newLine = "</div><div class=\"markdown\">"  #this gives break
    return isNewLine, newLine

def processStandardHTML(line):
    newLine = line

    if line.startswith("@@ "):
        newLine = "<div class=\"indent\"></div>" + newLine[3:]

    while newLine.find("**") is not -1:
        boldLoc = newLine.find("**")
        if boldLoc is not -1:    #asterisks exists
            boldLoc2 = boldLoc + 2 + newLine[boldLoc+2:].find("**")
            if boldLoc2 is not -1:
                newLine = newLine[0:boldLoc] + "<b>"+newLine[boldLoc+2 : boldLoc2] +"</b>"+ newLine[boldLoc2+2:]

    while newLine.find("*") is not -1:
        itLoc = newLine.find("*")
        if itLoc is not -1:    #asterisk exists
            itLoc2 = itLoc + 1 + newLine[itLoc+1:].find("*")
            if itLoc2 is not -1:
                newLine = newLine[0:itLoc] + "<i>"+newLine[itLoc+1 : itLoc2] +"</i>"+ newLine[itLoc2+1:]   

    lozengeInds = findAllStr(newLine, "$\\lozenge$")
    if lozengeInds:
        for i in range(len(lozengeInds), 0, -1):
            newLine = newLine[:lozengeInds[i-1]]+"<span class=\"qed\">"+newLine[lozengeInds[i-1]:].lstrip() + "</span>"
    
    squareInds = findAllStr(newLine, "$\\square$")
    if squareInds:
        for i in range(len(squareInds), 0, -1):
            newLine = newLine[:squareInds[i-1]]+"<span class=\"qed\">"+newLine[squareInds[i-1]:].lstrip() + "</span>"

    leftParen = newLine.find("(")
    rightParen = newLine.find(")")
    leftBracket = newLine.find("[")
    rightBracket = newLine.find("]")
    while leftParen is not -1 and rightParen is not -1 and leftBracket is not -1 and rightBracket is not -1 and leftBracket < rightBracket and rightBracket < leftParen and leftParen < rightParen and leftParen-1 is rightBracket: 
        leftParen = newLine.find("(")
        rightParen = newLine.find(")")
        leftBracket = newLine.find("[")
        rightBracket = newLine.find("]")
        if leftParen is not -1 and rightParen is not -1 and leftBracket is not -1 and rightBracket is not -1:
            if leftBracket < rightBracket and rightBracket < leftParen and leftParen < rightParen and leftParen-1 is rightBracket:
                text = newLine[leftBracket+1:rightBracket]
                href = newLine[leftParen+1:rightParen]
                newLine = newLine[:leftBracket]+"<a href=\""+href+"\">"+text+"</a>"+newLine[rightParen+1:]
    newLine = "<p>"+newLine+"</p>"
    return newLine

def checkCodeHTML(line):
    isCode = False
    newLine = ""
    if line.startswith('```'):
        isCode = True
        global inCodeBlock
        if inCodeBlock:
            inCodeBlock = False
        else:
            inCodeBlock = True
        if inCodeBlock:
            newLine = "<pre class=\"prettyprint\"><div class=\"codeWrap\"><code>"
        else:
            newLine = "</code></div></pre>"
    return isCode, newLine


def upperBoilerPlateHTML():
    res = ""
    res+="<!DOCTYPE html>\n"
    res+="<html lang=\"en\">\n"
    res+="<head>\n"
    res+="<meta charset=\"UTF-8\">\n"
    res+="<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
    res+="<meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">\n"
    res+="<title>"+dirname+"</title>\n"
    res+="<link rel=\"stylesheet\" href=\"markdown.css\">\n"
    res+="<script type=\"text/x-mathjax-config\">MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\\\(','\\\\)']]}});</script>\n"
    res+="<script type=\"text/javascript\" async src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML\"></script>\n"
    res+="<script src=\"https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js\"></script>\n"
    res+="</head>\n"
    res+="<body>\n"
    res+="<div class=\"markdown\">\n"
    return res

def lowerBoilerPlateHTML():
    res = "</div>"
    res+="</body>\n"
    res+="</html>\n"
    return res


def makeCSS():
    res = ""
    res+="* {font-family: Arial, Helvetica, sans-serif} \n"
    res+="body, html{margin: 0;padding: 0;max-width: 100vw;}\n"
    res+="body{margin: auto;background-color: #333;}\n"
    res+=".markdown{font-size: 1.3rem;line-height: 1.3em;padding: 0.6in;margin: 2rem auto;max-width: 900px;background-color: white; box-shadow: 0 15px 35px 0 rgba(0, 0, 0, 0.4),0 5px 25px 0 rgba(0,0,0,0.36);}\n"
    res+="ul{margin: 0.2rem 0 0.5rem;}\n"
    res+="h4{margin: 0.75rem 0;}\n"
    res+="pre, code {font-family: monospace, monospace;}\n"
    res+="pre {overflow: auto;background-color: #ddd; display: flex;}\n"
    res+=".codeWrap{margin: 2rem; display: flex;}\n"
    res+=".codeWrap:after{content: \"\";width: 2rem;}\n"
    res+="pre.prettyprint{border: none !important; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.16), 0 2px 4px 0 rgba(0,0,0,0.12);}"
    res+=".indent{display: inline-block; width: 3ch;}\n"
    res+=".newpage{display: block; height: 5em;}\n"
    res+=".qed{float: right;}\n"

    with open(cssname, "w") as f:
        f.write(res)

###############################################################################
###############################################################################
########
########                 BEGIN TEX
########
###############################################################################
###############################################################################


def checkHeaderTex(line):
    isHeader = False
    newLine = ""
    if line.startswith('#'):
        isHeader = True
        num = 0
        for i in range(0, len(line)):
            if line[i] is '#':
                num+=1
        if num is 1:
            newLine = "{\\Huge "+line[num:].strip()+"}\\\\"
        elif num is 2:
            newLine = "{\\LARGE "+line[num:].strip()+"}\\\\"
        elif num is 3:
            newLine = "{\\Large "+line[num:].strip()+"}\\\\"
        elif num >= 4:
            newLine = "{\\large "+line[num:].strip()+"}\\\\"
            
    return isHeader, newLine

def checkListTex(line):
    isList = False
    newLine = ""
    if line.startswith('* '):
        isList = True
        newLine = "\\begin{itemize} \\item "+line[1:].strip()+"\\end{itemize}"
    elif line[0].isdigit():
        i = 0
        num = ""
        while i < len(line) and line[i].isdigit():
            num+=line[i]
            i+=1
        if i < len(line) and line[i] is ".":
            isList = True
            newLine = "\\begin{enumerate} \\setcounter{enumi}{"+str(int(num)-1)+"} \\item "+line[i+2:]+"\\end{enumerate}"
    return isList, newLine

def processNewPageTex(line):
    isNewLine = False
    newLine = ""
    if line.startswith("@@N"):
        isNewLine = True
        newLine = "\\newpage"
    return isNewLine, newLine

def processStandardTex(line):
    newLine = line
    if line.startswith("@@ "):
        newLine = "\\indent " + newLine[3:]
    while newLine.find("**") is not -1:
        boldLoc = newLine.find("**")
        if boldLoc is not -1:    #asterisks exists
            boldLoc2 = boldLoc + 2 + newLine[boldLoc+2:].find("**")
            if boldLoc2 is not -1:
                newLine = newLine[0:boldLoc] + "\\textbf{"+newLine[boldLoc+2 : boldLoc2] +"}"+ newLine[boldLoc2+2:]

    while newLine.find("*") is not -1:
        itLoc = newLine.find("*")
        if itLoc is not -1:    #asterisk exists
            itLoc2 = itLoc + 1 + newLine[itLoc+1:].find("*")
            if itLoc2 is not -1:
                newLine = newLine[0:itLoc] + "\\textit{"+newLine[itLoc+1 : itLoc2] +"}"+ newLine[itLoc2+1:]    

    while newLine.find("\"") is not -1:
        itLoc = newLine.find("\"")
        if itLoc is not -1:    #quotation mark exists
            itLoc2 = itLoc + 1 + newLine[itLoc+1:].find("\"")
            if itLoc2 is not -1:
                newLine = newLine[0:itLoc] + "``"+newLine[itLoc+1 : itLoc2] +"\'\'"+ newLine[itLoc2+1:]   
    

    lozengeInds = findAllStr(newLine, "\\lozenge")
    if lozengeInds:
        for i in range(len(lozengeInds), 0, -1):
            newLine = newLine[:lozengeInds[i-1]]+" \\hfill "+newLine[lozengeInds[i-1]:].lstrip()
    
    squareInds = findAllStr(newLine, "\\square")
    if squareInds:
        for i in range(len(squareInds), 0, -1):
            newLine = newLine[:squareInds[i-1]]+" \\hfill "+newLine[squareInds[i-1]:].lstrip()


    ampInds = findAll(newLine, "&")
    if ampInds:
        for i in range(len(ampInds), 0, -1):
            newLine = newLine[:ampInds[i-1]-1]+' \\& '+newLine[ampInds[i-1]+2:].lstrip()

    leftParen = newLine.find("(")
    rightParen = newLine.find(")")
    leftBracket = newLine.find("[")
    rightBracket = newLine.find("]")
    while leftParen is not -1 and rightParen is not -1 and leftBracket is not -1 and rightBracket is not -1 and leftBracket < rightBracket and rightBracket < leftParen and leftParen < rightParen and leftParen-1 is rightBracket:         
        leftParen = newLine.find("(")
        rightParen = newLine.find(")")
        leftBracket = newLine.find("[")
        rightBracket = newLine.find("]")
        if leftParen is not -1 and rightParen is not -1 and leftBracket is not -1 and rightBracket is not -1:
            if leftBracket < rightBracket and rightBracket < leftParen and leftParen < rightParen and leftParen-1 is rightBracket:
                text = newLine[leftBracket+1:rightBracket]
                href = newLine[leftParen+1:rightParen]
                newLine = newLine[:leftBracket]+"\\href{"+href+"}{"+text+"}"+newLine[rightParen+1:]
    return newLine+"\\\\"




def upperBoilerPlateTex():
    res = ""
    res+="\\documentclass[12pt]{article}\n"
    res+="\\usepackage[margin=1in]{geometry}\n"
    res+="\\usepackage{setspace}\n"
    res+="\\usepackage[leftmargin = 1in, rightmargin = 0in, vskip = 0in]{quoting}\n"
    res+="\\usepackage{microtype}\n"
    res+="\\usepackage{amssymb, amsthm, amsmath, amsfonts}\n"
    res+="\\usepackage{ wasysym }\n"
    res+="\\usepackage{graphicx}\n"
    res+="\\usepackage{color}\n"
    res+="\\usepackage{hyperref}\n"
    res+="\\newcommand{\\blockquotespacing}{\\blockspaced}\n"
    res+="\\newcommand{\\prose}{.25in}\n"
    res+="\\newcommand{\\poetry}{0in}\n"
    res+="\\newcommand{\\singlespaced}{\\setstretch{1}\\vspace{\\baselineskip}}\n"
    res+="\\newcommand{\\blockspaced}{\\setstretch{1.3}\\vspace{\\baselineskip}}\n"
    res+="\\newcommand{\\doublespaced}{}\n"
    res+="\\newenvironment{blockquote}[1][\\prose]{\\setlength{\\parindent}{#1}\\begin{quoting}\\blockquotespacing}{\\end{quoting}}\n"
    res+="\\begin{document}\n"
    res+="\\setstretch{2}\n"
    # res+="\\raggedright\n"
    res+="\\noindent\n"
    return res

def lowerBoilerPlateTex():
    res ="\\end{document}"
    return res


###############################################################################
###############################################################################
########
########                 FILE WRITERS
########
###############################################################################
###############################################################################



def writeHTML():
    with open(mdname) as f: #read in file
        for line in f.readlines():
            ogLine = line
            line = line.strip() #remove whitespace
            if line is not '':
                newLine = line
                isCode, codeLine = checkCodeHTML(line)
                isHeader, headLine = checkHeaderHTML(line)
                isList, listLine = checkListHTML(line)
                isNewPage, newPageLine = processNewPageHTML(line)
                if isCode:
                    newLine = codeLine
                elif inCodeBlock:
                    newLine = ogLine[:-1] + "\n"
                elif isHeader:
                    newLine = headLine + "\n"
                elif isList:
                    newLine = listLine + "\n"
                elif isNewPage:
                    newLine = newPageLine + "\n"
                else:
                    standardLine = processStandardHTML(line)
                    newLine = standardLine + "\n"
                htmlLines.append(newLine)

    with open(htmlname, "w") as f:
        f.write(upperBoilerPlateHTML())
        for line in htmlLines:
            f.write(line)
        f.write(lowerBoilerPlateHTML())
    makeCSS()


def writeTex():
    with open(mdname) as f: #read in file
        for line in f.readlines():
            line = line.strip() #remove whitespace
            if line is not '':
                newLine = line
                isHeader, headLine = checkHeaderTex(line)
                isList, listLine = checkListTex(line)
                isNewPage, newPageLine = processNewPageTex(line)
                if isHeader:
                    newLine = headLine
                elif isList:
                    newLine = listLine
                elif isNewPage:
                    newLine = newPageLine
                else:
                    standardLine = processStandardTex(line)
                    newLine = standardLine
                texLines.append(newLine)

    with open(texname, "w") as f:
        f.write(upperBoilerPlateTex())
        for line in texLines:
            f.write(line+"\n")
        f.write(lowerBoilerPlateTex())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No directory provided. Directory must have file DIRNAME/DIRNAME.md\nTo run:\t\tpython mdTex.py DIRNAME")
        sys.exit()
    dirname = str(sys.argv[1])
    if dirname is "-h" or dirname is "--help":
        print("Markdown to html and latex converter!")
        print("Directory must have file DIRNAME/DIRNAME.md\nTo run:\t\tpython mdTex.py DIRNAME")
    if len(sys.argv) > 1 and sys.argv[2] == "current":
        mdname = dirname+".md"
        htmlname = dirname+".html"
        texname  = dirname+".tex"
        cssname  = "markdown.css"
    else:
        mdname = dirname+"/"+dirname+".md"
        htmlname = dirname+"/"+dirname+".html"
        texname = dirname+"/"+dirname+".tex"
        cssname = dirname+"/"+"markdown.css"
    writeHTML()
    writeTex()
    print("Converted "+ dirname+".md"+ " to " + dirname+".html and " + dirname+".tex")