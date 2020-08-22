import os, json, re
from flask import *

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/commonkeywords")
def commonkeywords():
    return render_template("commonkeywords.html")

@app.route("/compare", methods=['POST'])
def compare():
    inc = request.form['include']
    exc = request.form['exclude']

    v = {"result" : commonelements(inc,exc)}
    return json.dumps(v)

def commonelements(inc,exc):
    commonItems = []
    inc = clearNot(inc)
    exc = clearNot(exc)

    incwords = []
    excwords = []
    for i in inc:
        i=i.strip()
        if 'AttributesContain' in i:
            ind = i.index(':')
            temp = i[ind+1:len(i)-1]
            temp = temp.split('|')
            incwords = [*incwords, *temp]

    for i in exc:
        i=i.strip()
        if 'AttributesContain' in i:
            ind = i.index(':')
            temp = i[ind+1:len(i)-1]
            temp = temp.split('|')
            excwords = [*excwords, *temp]

    for i in incwords:
        for j in excwords:
#             if re.sub('[^a-zA-Z0-9]','',i).casefold() in re.sub('[^a-zA-Z0-9]','',j).casefold() and re.sub('[^a-zA-Z0-9]','',i).casefold() == re.sub('[^a-zA-Z0-9]','',j).casefold():
#                 commonItems.append(j)
#             elif re.sub('[^a-zA-Z0-9]','',i).casefold() in re.sub('[^a-zA-Z0-9]','',j).casefold()+'s' and re.sub('[^a-zA-Z0-9]','',i).casefold() == re.sub('[^a-zA-Z0-9]','',j).casefold()+'s':
#                 commonItems.append(j)
#             elif re.sub('[^a-zA-Z0-9]','',i).casefold()+'s' in re.sub('[^a-zA-Z0-9]','',j).casefold() and re.sub('[^a-zA-Z0-9]','',i).casefold()+'s' == re.sub('[^a-zA-Z0-9]','',j).casefold():
#                 commonItems.append(j)
            if re.sub('[^a-zA-Z0-9]','',i).casefold() == re.sub('[^a-zA-Z0-9]','',j).casefold() and re.sub('[^a-zA-Z0-9]','',i).casefold() == re.sub('[^a-zA-Z0-9]','',j).casefold():
                commonItems.append(j)
            elif re.sub('[^a-zA-Z0-9]','',i).casefold() == re.sub('[^a-zA-Z0-9]','',j).casefold()+'s' and re.sub('[^a-zA-Z0-9]','',i).casefold() == re.sub('[^a-zA-Z0-9]','',j).casefold()+'s':
                commonItems.append(j)
            elif re.sub('[^a-zA-Z0-9]','',i).casefold()+'s' == re.sub('[^a-zA-Z0-9]','',j).casefold() and re.sub('[^a-zA-Z0-9]','',i).casefold()+'s' == re.sub('[^a-zA-Z0-9]','',j).casefold():
                commonItems.append(j)
            elif re.sub('[^a-zA-Z0-9]','',i).casefold()[:len(re.sub('[^a-zA-Z0-9]','',j).casefold())-1]+'s' == re.sub('[^a-zA-Z0-9]','',j).casefold():
                commonItems.append(j)
              
 
    #print(list(set(commonItems)))
    return(list(set(commonItems)))

def clearNot(syntax):
    notindex =[]
    lines = syntax.splitlines()
    for i in range(0,len(lines)):
        lines[i]=lines[i].strip()
    startIndex = 0
    notFlag = False
    endIndex = 0
    for i in range(0,len(lines)):
        if lines[i]== '{NOT':
            for j in range(i,len(lines)):
                if lines[j] == '}':
                    notindex.append((i,j+1))
                    break

    for i in notindex:
        for j in range(i[0],i[1]):
            lines[j] = ''

    lines = [x for x in lines if x != '']
    return lines

@app.route('/missingkeywords')
def missingkeywords():
    return render_template('missingkeywords.html')

@app.route('/getmissingkeys', methods=['POST'])
def sendmissingkeys():
    dockeys = request.form['dockeys']
    modelsyx = request.form['modelsyx']
    res = {"result" : getmissingkeywords(dockeys, modelsyx)}
    return json.dumps(res)

def getmissingkeywords(dockeys, modelsyx):
    missing = []
    dockeys = dockeys.split(',')
    dockeys = [ i.strip() for i in dockeys ]

    word_list = []
    for line in modelsyx.splitlines():
        if 'AttributesContain' in line:
                ln = line[line.index(':')+1:len(line)-1]
                temp = re.split(r'[|:]',ln)
                word_list = [*word_list, *temp]

    for i in range(len(dockeys)):
        flag= False
        for j in range(len(word_list)):
            if dockeys[i].casefold() in word_list[j].casefold() and dockeys[i].casefold() == word_list[j].casefold():
                flag = True
                break
            elif dockeys[i].casefold() in word_list[j].casefold().replace(".","-") and dockeys[i].casefold() == word_list[j].casefold().replace(".","-"):
                flag = True
                break
            elif dockeys[i].casefold() in word_list[j].casefold().replace("."," ") and dockeys[i].casefold() == word_list[j].casefold().replace("."," "):
                flag = True
                break
            elif dockeys[i].casefold() in word_list[j].casefold().replace(".","'") and dockeys[i].casefold() == word_list[j].casefold().replace(".","'"):
                flag = True
                break
            elif dockeys[i].casefold() in word_list[j].casefold().replace(".","/") and dockeys[i].casefold() == word_list[j].casefold().replace(".","/"):
                flag = True
                break
            elif dockeys[i].casefold() in word_list[j].casefold().replace(".","&") and dockeys[i].casefold() == word_list[j].casefold().replace(".","&"):
                flag = True
                break
            elif dockeys[i].casefold() in word_list[j].casefold().replace(".","s") and dockeys[i].casefold() == word_list[j].casefold().replace(".","s"):
                flag = True
                break
            elif (dockeys[i].casefold()).replace("*",".") in word_list[j].casefold() and (dockeys[i].casefold()).replace("*",".") == word_list[j].casefold():
                flag = True
                break
            elif (dockeys[i].casefold()+'.') in word_list[j].casefold() and (dockeys[i].casefold()+'.') == word_list[j].casefold():
                flag = True
                break

        if flag == False:
            missing.append(dockeys[i])
    return missing

@app.route('/asin')
def asin():
    return render_template('asin.html')

@app.route('/findasin',methods=['POST'])
def findMissingAsin():
    doc = request.form['doc'].splitlines()
    mod = request.form['mod'].splitlines()
    words = []
    for d in doc:
          if d not in mod:
            words.append(d)
    for m in mod:
        if m not in doc:
            words.append(m)
    res = {"result" : words}
    return json.dumps(res)

@app.route('/spelling')
def spelling():
    return render_template('spelling.html')

@app.route('/spellcheck',methods = ['POST'])
def spellcheck():
    attrs = request.form['attributes']
    attrSyx = request.form['attrsyx']

    attrs = attrs.splitlines()
    attrSyx = attrSyx.splitlines()
    spellings = []
    for line in attrSyx:
        if 'AttributesContain' in line:
            arr = line[line.index('[')+1:line.index(':')].split('|')
            for a in arr:
                if a not in attrs:
                    tag="<mark>"+a+"</mark>"
                    spellings.append({tag:line})

    res = {"result" : spellings}
    return json.dumps(res)

@app.route('/loadattrs',methods = ['GET'])
def attribLoad():
    str='''item_name
bullet_point
product_description
brand
product_type
item_description
material
material_composition
batteries_required
batteries_included
manufacturer_minimum_age
includes_rechargable_battery
included_components
fabric_type
includes_ac_adapter
power_plug_type
power_source_type
website_suppressed
index_suppressed'''

    return str

@app.route('/syntax')
def syntax():
    return render_template('syntax.html')

@app.route('/syntaxcheck',methods = ['POST'])
def syntaxcheck():
    syntax = request.form['syntax']
    indexList =[]
    try:
        for i in range(len(syntax)):
            if syntax[i] == '[' or syntax[i] == ']':
                if syntax[i-1]==' ':
                    indexList.append(i-1)
                if syntax[i+1]==' ':
                    indexList.append(i+1)
            if syntax[i] == ':':
                if syntax[i-1] == ' ':
                    indexList.append(i-1)
                if syntax[i+1] == ' ':
                    indexList.append(i+1)
            if syntax[i] == '|':
                if syntax[i-1] == ' ':
                    indexList.append(i-1)
                if syntax[i+1] == ' ':
                    indexList.append(i+1)
            if syntax[i] == ' ':
                if syntax[i-1] == ' ':
                    indexList.append(i-1)
                if syntax[i+1] == ' ':
                    indexList.append(i+1)
            if syntax[i] == '|':
                if syntax[i-1] == '|':
                    indexList.append(i-1)
                if syntax[i+1] == '|':
                    indexList.append(i+1)
            if syntax[i] == ':':
                if syntax[i-1] == '|':
                    indexList.append(i-1)
                if syntax[i+1] == '|':
                    indexList.append(i+1)
            if syntax[i] == ':':
                if syntax[i-1] == ':':
                    indexList.append(i-1)
                if syntax[i+1] == ':':
                    indexList.append(i+1)
            if syntax[i-1] == '|':
                if syntax[i] == '.':
                    if syntax[i+1] == "|":
                        indexList.append(i)
            if syntax[i] == '{' or syntax[i] == '}':
                if syntax[i-1]==' ':
                    indexList.append(i-1)
                if syntax[i+1]==' ':
                    indexList.append(i+1)
    except:
        pass
    print(indexList)
    scorrect=''''''
    for i in range(len(syntax)):
        if i in indexList:
            scorrect += "<mark style='background-color:yellow'> </mark>"
        else:
            scorrect += syntax[i]
    res = {'result' : scorrect}
    return json.dumps(res)

@app.route('/replacesyx')
def replacesyx():
    return render_template("replace.html")

@app.route('/getreplaceres',methods=['POST'])
def replacesyxdata():
    clicked = request.form['clicked']
    syntax = request.form['syntax']
    resstr=''
    if clicked == 'replace':
        syntaxlines = syntax.splitlines()
        chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '\\', ';', "\'", '\"' , '<', '>', '/','?', ',',' ']
        for line in syntaxlines:
            try:
                colonIndex = line.index(':')
                resstr += line[0:colonIndex]
                for c in range(colonIndex,len(line)):
                    if line[c] in chars:
                        resstr += '.'
                    elif line[c]== '|' and (line[c-1] == '.'):
                        resstr += '|'
                    elif line[c] == ']' and (line[c-1] == '.'):
                        resstr += ']'
                    else:
                        resstr += line[c]
            except:
                for c in line:
                    resstr += c
            resstr += "\n"

    if clicked == 'create':
        for i in range (len(syntax)):
            if (syntax[i] == ','):
                resstr += '.|'
            elif(syntax[i] == ' ' and syntax[i-1] == ','):
                continue
            elif syntax[i] in ['!', '@', '#', '$', '%', '^', '*', '(', ')', '-', '=', '+', '\\', ';', "\'", '\"' , '<', '>', '/', '?', ' ']:
                resstr += '.'
            else:
                resstr += syntax[i]


    return json.dumps({'result': resstr+'.'})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8970)
