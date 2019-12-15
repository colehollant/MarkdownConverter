#!/usr/local/bin/python3

import sys

'''

    This is just a lil diddy I threw together to convert markdown to 
    both latex and html with jax!
    This is just for my ease of use, and should be used through the associated script
    If you wanna use it, feeeeeel free!

'''

htmlLines = []
texLines = []
inCodeBlock = False
inCommentBlock = False
mustFinishComment = False

markdownToTexLangs= {
"apache": "sh",
"applescript": "C++",
"c": "C",
"cmake": "make",
"cpp": "C++",
"c++": "C++",
"cs": "C++",
"csharp": "C++",
"css": "XML",
"bash": "bash",
"http": "XML",
"html": "HTML",
"java": "Java",
"javascript": "Java",
"json": "Python",
"go": "Go",
"jsx": "XML",
"less": "bash",
"make": "make",
"matlab": "Matlab",
"objectivec": "C++",
"pascal": "Pascal",
"php": "XML",
"perl": "Perl",
"python": "Python",
"py": "Python",
"sh": "sh",
"sql": "SQL",
"scss": "XML",
"svg": "XML",
"swift": "C++",
"rb": "Ruby",
"ruby": "Ruby",
"vue": "XML",
"xml": "XML"
}


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

def checkBlockQuoteHTML(line):
    isBlockQuote = False
    newLine = ""
    if line.startswith('> '):
        isBlockQuote = True
        newLine = "<blockquote>"+line[1:].strip()+"</blockquote>"
    return isBlockQuote, newLine

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
        processed = processStandardTex(line[num:].strip()).strip()
        if num is 1:
            newLine = "\n\\chapter{"+processed+"}"
        elif num is 2:
            newLine = "\n\\section{"+processed+"}"
        elif num is 3:
            newLine = "\n\\subsection{"+processed+"}"
        elif num >= 4:
            newLine = "\n\\label{"+processed+"}"
            
    return isHeader, newLine

def checkBlockQuoteTex(line):
    isBlockQuote = False
    newLine = ""
    if line.startswith('> '):
        isBlockQuote = True
        processed = processStandardTex(line[1:].strip()).strip()
        newLine = "\n\\begin{quote}\n" + processed + "\n\\end{quote}"
    return isBlockQuote, newLine

def checkListTex(line):
    isList = False
    newLine = ""
    if line.startswith('* '):
        isList = True
        processed = processStandardTex(line[1:].strip()).strip()
        newLine = "\\begin{itemize} \\item "+ processed +"\\end{itemize}"
    elif line[0].isdigit():
        i = 0
        num = ""
        while i < len(line) and line[i].isdigit():
            num+=line[i]
            i+=1
        if i < len(line) and line[i] is ".":
            isList = True
            processed = processStandardTex(line[i+2:]).strip()
            newLine = "\\begin{enumerate} \\setcounter{enumi}{"+str(int(num)-1)+"} \\item "+ processed +"\\end{enumerate}"
    return isList, newLine

def checkCodeTex(line):
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
            lang = line[3:].strip().lower()
            if lang in markdownToTexLangs.keys():
                newLine = "\\begin{lstlisting}[language=" + markdownToTexLangs[lang] + "]"
            else:
                newLine = "\\begin{lstlisting}[language=C]"
        else:
            newLine = "\\end{lstlisting}"
    return isCode, newLine

def checkMultilineComment(line):
    global inCommentBlock
    global mustFinishComment
    isComment = False
    newLine = ""
    if line.startswith('<!--'):
        isComment = True
        inCommentBlock = True
    if inCommentBlock:
        newLine = "% " + line
        if line.find("-->") is not -1:
            inCommentBlock = False
            mustFinishComment = True
            newLine = "% " + line[0:line.find("-->") + 3] + "\n" +  line[line.find("-->")+3:]
    return isComment, newLine

def processNewPageTex(line):
    isNewLine = False
    newLine = ""
    if line.startswith("@@N"):
        isNewLine = True
        newLine = "\\newpage"
    return isNewLine, newLine

def processStandardTex(line):
    global inCommentBlock
    newLine = line

    if line.startswith("___"):
        return "\n"

    if line.startswith("@@ "):
        newLine = "\\indent " + newLine[3:]

    if line.find("<!--") is not -1 and line.find("-->") > line.find("<!--"):
        if inCommentBlock:
            inCommentBlock = False
        newLine = newLine[0:line.find("<!--")] + newLine[line.find("-->") + 3:]

    linkInd = newLine.find("](")
    while linkInd != -1:
        leftBracket = newLine.rfind("[", 0, linkInd + 1)
        rightParen = newLine.find(")", linkInd)
        text = newLine[leftBracket+1:linkInd]
        href = newLine[linkInd+2:rightParen].replace("_", "<HREFUNDER>").replace("*", "<HREFAST>")
        newLine = newLine[:leftBracket]+"\\href{"+href+"}{"+text+"}"+newLine[rightParen+1:]
        linkInd = newLine.find("](")

    while newLine.find("`") is not -1:
        codeLoc = newLine.find("`")
        if codeLoc is not -1:    #backtick exists
            codeLoc2 = codeLoc + 1 + newLine[codeLoc+1:].find("`")
            if codeLoc2 is not -1:
                newLine = newLine[0:codeLoc] + "\\texttt{"+newLine[codeLoc+1 : codeLoc2].replace('\\', '\\textbackslash ').replace("$", "\$").replace("_", "<CODEUNDER>").replace("*", "<CODEAST>") +"}"+ newLine[codeLoc2+1:]   

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
    
    while newLine.find("_") is not -1:
        itLoc = newLine.find("_")
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

    return "\n" + newLine.replace("<CODEAST>", "*").replace("<CODEUNDER>", "\\_").replace("<HREFUNDER>", "_").replace("<HREFAST>", "*")




def upperBoilerPlateTex():
    res = ""
    res += "\\documentclass[11pt, twoside, reqno]{book}\n"
    res += "\\usepackage{amssymb, amsthm, amsmath, amsfonts}\n"
    res += "\\usepackage[htt]{hyphenat}\n"
    res += "\\usepackage{graphicx}\n"
    res += "\\usepackage{color}\n"
    res += "\\usepackage{hyperref}\n"
    res += "\\usepackage{verbatim}\n"
    res += "\\usepackage{ wasysym }\n"
    res += "\\usepackage[toc,page]{appendix}\n"
    res += "\\appendixpageoff\n"
    res += "\\usepackage[leftmargin = 1in, rightmargin = 0in, vskip = 0in]{quoting}\n"
    res += "\\usepackage{microtype}\n"
    res += "\\usepackage{bardtex}\n"
    res += "\\biboption{amsrefs}\n"
    res += "\\styleoption{seniorproject}\n"
    res+="\\usepackage{listings}\n"
    res+="\\definecolor{codegreen}{rgb}{0,0.6,0}\n"
    res+="\\definecolor{codegray}{rgb}{0.5,0.5,0.5}\n"
    res+="\\definecolor{codepurple}{rgb}{0.58,0,0.82}\n"
    res+="\\definecolor{backcolour}{rgb}{0.95,0.95,0.98}\n"
    res+="\\lstdefinestyle{mystyle}{\n"
    res+="    commentstyle=\\color{codegreen},\n"
    res+="    keywordstyle=\\color{magenta},\n"
    res+="    stringstyle=\\color{codepurple},\n"
    res+="    basicstyle=\\ttfamily\\footnotesize,\n"
    res+="    backgroundcolor=\\color{backcolour},\n"
    res+="    frame=lrbt,\n"
    res+="    breakatwhitespace=false,      \n"
    res+="    framexleftmargin=8pt, \n"
    res+="    framexrightmargin=8pt,   \n"
    res+="    framextopmargin=6pt,\n"
    res+="    framexbottommargin=6pt,\n"
    res+="    breaklines=true,                 \n"
    res+="    keepspaces=false,                 \n"
    res+="    numbersep=0pt,                  \n"
    res+="    showspaces=false,                \n"
    res+="    showstringspaces=false,\n"
    res+="    showtabs=false,                  \n"
    res+="    tabsize=1\n"
    res+="}\n"
    res+="\\lstset{style=mystyle}\n"
    res += "\\newcommand{\\blockquotespacing}{\\blockspaced}\n"
    res += "\\newcommand{\\prose}{.25in}\n"
    res += "\\newcommand{\\poetry}{0in}\n"
    res += "\\newcommand{\\singlespaced}{\\setstretch{1}\\vspace{\\baselineskip}}\n"
    res += "\\newcommand{\\blockspaced}{\\setstretch{1.3}\\vspace{\\baselineskip}}\n"
    res += "\\newcommand{\\doublespaced}{}\n"
    res += "\\newenvironment{blockquote}[1][\\prose]{\\setlength{\\parindent}{#1}\\begin{quoting}\\blockquotespacing}{\\end{quoting}}\n"
    res += "\\begin{document}\n"
    res += "\\startmain"
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
                isBlockQuote, blockQuoteLine = checkBlockQuoteHTML(line)
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
                elif isBlockQuote:
                    newLine = blockQuoteLine + "\n"
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
    global mustFinishComment
    with open(mdname) as f: #read in file
        for line in f.readlines():
            originalLine = line
            line = line.strip() #remove whitespace
            if line is not '':
                newLine = line
                isCode, codeLine = checkCodeTex(line)
                _, commentLine = checkMultilineComment(line)
                isHeader, headLine = checkHeaderTex(line)
                isList, listLine = checkListTex(line)
                isBlockQuote, blockQuoteLine = checkBlockQuoteTex(line)
                isNewPage, newPageLine = processNewPageTex(line)
                if isCode:
                    newLine = codeLine
                elif inCodeBlock:
                    newLine = originalLine[:-1]
                    newLine = newLine
                elif inCommentBlock:
                    newLine = commentLine
                elif mustFinishComment:
                    mustFinishComment = False
                    newLine = commentLine
                elif isHeader:
                    newLine = headLine
                elif isList:
                    newLine = listLine
                elif isNewPage:
                    newLine = newPageLine
                elif isBlockQuote:
                    newLine = blockQuoteLine
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
