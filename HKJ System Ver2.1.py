#-------------------------------------------------------------------------------
# Name:        Segmentation System
# Purpose:
#
# Author:      HKJ
#
# Created:     21.12.2016
# Copyright:   HKJ
# Licence:     HKJ(R)
#-------------------------------------------------------------------------------

from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import math
from PIL import Image

from PIL import ImageTk

master=Tk()
master.title('HKJ Chinese Word Segmentation System')
master.minsize(600,200)

eigenfile=open('eigenword.txt','r')
eigentext=eigenfile.readline()
eigenword = eigentext.split(',')
eigenfile.close()

puncfile=open('punc.txt','r')
punc=puncfile.readline()
puncfile.close()

instructions='''Welcome to use our segmentation system!\n
We provide two main kinds of segmentation -- file Seg & sentence Seg.\n
For file Seg, open a chosen file and edit it if you want. Click Segment a file to perform a segmentation procedure.
You are able to choose a sentence you want to see the direct result of segmenting it.\n
For sentence Seg, the difference is, you won't be able to choose a sentence of it. And for your convenience, we advice
you not to input more than one sentence in it.\n
For more information, please contact HKJ Team, we are glad to help you.'''

copyrights='''The Segmentation System is based on the new method of segmentation.\n
This version is released by HKJ Team.\n
Team members list:\n
Team leader -- Xia Hao
Code writer -- Luo Quan
UI builder -- Ding Yuchen\n
All rights reserved. Any tort will be punished by Chinese laws and related regulations'''


def sentence_seg(c):
    global punc
    u = ''
    for y in c:
        if y in punc:
            u += ' '+y+' '
        elif y == '\n' or y == ' ':
            pass
        else:
            u += y
    list_of_sentences = u.split()
    diction = {}
    i = 1
    show_seg_list = []
    for p in list_of_sentences:
        if p not in punc:
            diction[str(i)] = p
            show_seg_list.append(str(i) + ') ' + p)
            i = i + 1
    show_seg_text = '\n'.join(show_seg_list)
    return show_seg_text,diction,list_of_sentences


def seg_initialize(sent):
    global eigenword
    sent_list1 = []
    i = 0
    while i <= len(sent) - 1:
        bi_ch = sent[i:i + 2]
        if bi_ch in eigenword:
            if sent[:i] != '':
                sent_list1.append(sent[:i])
            sent_list1.append(bi_ch)
            sent = sent[i + 2:]
            i = 0
            continue
        i = i + 1
    sent_list1.append(sent)

    init_sentList = []
    sent_list2 = []
    linkword2 = ''
    for multi_word in sent_list1:
        if multi_word not in eigenword:
            for ch in multi_word:
                if ch in eigenword:
                    if linkword2 != '':
                        sent_list2.append(linkword2)
                    linkword2 = ''
                    sent_list2.append(ch)
                else:
                    linkword2 = linkword2 + ch
            if linkword2 != '':
                sent_list2.append(linkword2)
            init_sentList = init_sentList + sent_list2
            sent_list2 = []
            linkword2 = ''
        else:
            init_sentList.append(multi_word)
    return init_sentList


def digit_solved(u):
    re=''
    li=[]
    for number in range(len(u)):
        if u[number].isdigit():
            if (number < len(u) - 1 and u[number + 1].isdigit()) or (number != 0 and u[number - 1].isdigit()):
                if number!=len(u)-1:
                    if u[number+1].isdigit():
                        re+=u[number]
                    else:
                        re+=u[number]
                        li.append(re)
                        re=''
                else:
                    re += u[number]
                    li.append(re)
                    re = ''
    return li

def digit_wanted(u):
    deli=[]
    for number in range(len(u)):
        if u[number].isdigit():
            if (number<len(u)-1 and u[number+1].isdigit()) or (number!=0 and u[number-1].isdigit()):
                deli.append(number)
    return deli


def digit_wanted2(u):
    ddl=[]
    for number in range(len(u)):
        if u[number].isdigit():
            if (number<len(u)-1 and u[number+1].isdigit()) and (number!=0 and u[number-1].isdigit()==False):
                ddl.append(number)
            elif number==0:
                if u[number+1].isdigit():
                    ddl.append(number)
    return ddl


def changing(result):
    digit_lex = digit_solved(result)
    digit_want = digit_wanted(result)[::-1]
    digiting=digit_wanted2(result)
    iup = 0
    for num in digit_want:
        del result[num]
    diaosi=0
    for numb in digiting:
        numb=numb-diaosi
        result.insert(numb,digit_lex[iup])
        diaosi+=len(digit_lex[iup])-1
        iup+=1
    return result


def cut_list_former(a,c):
    coconut=[]
    for o in a:
        if o!=c:
            coconut.append(o)
        else:
            break
    return coconut


def cut_list_latter(a,c):
    coconut=[]
    for p in range(len(a)):
        if a[p]!=c:
            coconut.append(p)
        else:
            coconut.append(p)
            break
    for g in coconut:
        a[g]='0'
    a=' '.join(a)
    a=a[2*len(coconut):]
    a=a.split(" ")
    return a


def seg_main1(u):
    txt=open('Dictionary.txt','r')
    cp=''
    while True:
        x=txt.readline()
        cp+=x
        if len(x)==0:
            break
    cp=cp.split('\n')
    cp=','.join(cp)
    cp='{'+cp+'}'
    dc=eval(cp)
    lens=7
    kk=''
    while u!='':
        if len(u)<lens:
            lens=len(u)
        word=u[:lens]
        while word not in dc.keys():
            if len(word)==1:
                break
            else:
                word = word[:len(word) - 1]
        kk=kk+word+'|'
        u=u[len(word):]
    return kk


def seg_main2(u):
    txt = open('Dictionary.txt', 'r')
    cp = ''
    while True:
        x = txt.readline()
        cp += x
        if len(x) == 0:
            break
    cp = cp.split('\n')
    cp = ','.join(cp)
    cp = '{' + cp + '}'
    dc = eval(cp)
    lens = 4
    kk = ''
    while u!='':
        word=u[len(u)-1:]
        while word not in dc.keys():
            if len(word) == len(u):
                word=u[len(u)-1]
                break
            else:
                word=u[len(u)-len(word)-1:]
        kk=word+'|'+kk
        u=u[:len(u)-len(word)]
    return kk


def seg_cuts(u):                                      # this is the main seg func.
    txt = open('Dictionary.txt', 'r')
    cp = ''
    while True:
        x = txt.readline()
        cp += x
        if len(x) == 0:
            break
    cp = cp.split('\n')
    cp = ','.join(cp)
    cp = '{' + cp + '}'
    dc = eval(cp)
    rerere=[]
    if seg_main2(u)==seg_main1(u):
        rere=seg_main1(u).split('|')
        for jijiji in rere:
            if jijiji!='':
                rerere.append(jijiji)
        return rerere
    else:
        a=seg_main1(u).split('|')
        b=seg_main2(u).split('|')
        c1 = a
        c2 = b
        lili = []
        lilier = []
        for i in c2:
            if i in c1:
                if i != '':
                    p1 = ''.join(cut_list_former(c1, i))
                    p2 = ''.join(cut_list_former(c2, i))
                    if p1 == p2:
                        a1 = cut_list_former(c1, i)
                        b1 = cut_list_former(c2, i)
                        c1 = cut_list_latter(c1, i)
                        c2 = cut_list_latter(c2, i)
                        coco7 = 0
                        coco8 = 0
                        for thing in a1:
                            if thing in dc.keys():
                                coco7 += dc[thing]
                        for another_thing in b1:
                            if another_thing in dc.keys():
                                coco8 += dc[another_thing]
                        if coco7 >= coco8:
                            lili.append(a1)
                        else:
                            lili.append(b1)
                        lili.append(i)
                        # now c1 and c2 are the left things
        if c1 == c2:
            lilier = c1
        else:
            coco9 = 0
            coco0 = 0
            for thing1 in c1:
                if thing1 in dc.keys():
                    coco9 += dc[thing1]
            for another_thing1 in dc.keys():
                if another_thing1 in dc.keys():
                    coco0 += dc[another_thing1]
            if coco9 >= coco0:
                lilier=c1
            else:
                lilier=c2
        resulte=[]
        result=[]
        for ting in lili:
            if type(ting)==type([]):
                for to in ting:
                    resulte.append(to)
            else:
                resulte.append(ting)
        for jiji in lilier:
            resulte.append(jiji)
        for tv in resulte:
            if tv!='':
                result.append(tv)
        return result

f = open("dic.txt", "r")
xs = f.readlines()
dic = " ".join(xs)
f.close()

def check(s):
    return s in dic

def fq(word):
    pass

def preprocess(S):
    l = len(S)
    chunks = []
    prewords = []
    words = []

    for i in range(len(S)):
        chunk1 = S[:i+1]
        if check(chunk1) == True:
            S1 = S[i+1:]
            if i == len(S)-1:
                prewords += [[chunk1]]
            for i in range(len(S1)):
                chunk2 = S1[:i+1]
                if check(chunk2) == True:
                    S2 = S1[i+1:]
                    if i == len(S1)-1:
                        prewords += [[chunk1, chunk2]]
                    for i in range(len(S2)):
                        chunk3 = S2[:i+1]
                        if check(chunk3) == True:
                            prewords += [[chunk1, chunk2, chunk3]]
    return prewords

def pick(prewords):
    ls = []
    # calculate the sum of length(ls)
    for i in range(len(prewords)):
        ls += [0]
        for word in prewords[i]:
            ls[i] += len(word)
    #pick up the chunks with the biggest ls
    mls = max(ls)
    prewords2 = []
    for i in range(len(ls)):
        if ls[i] == mls:
            prewords2 += [prewords[i]]
    #calculate the average length
    al = []
    for i in range(len(prewords2)):
        al += [0]
        al[i] = mls/len(prewords2[i])
    #pick up the chunks with the biggest al
    mal = max(al)
    prewords3 = []
    for i in range(len(al)):
        if al[i] == mal:
            prewords3 += [prewords2[i]]
    #calculate the variance of al
    varl = []
    for i in range(len(prewords3)):
        varl += [0]
        for word in prewords3[i]:
            varl[i] += (len(word)-mal)**2/len(prewords3[i])
    #pick up the chunks with the least varl
    mvarl = min(varl)
    prewords4 = []
    for i in range(len(varl)):
        if varl[i] == mvarl:
            prewords4 += [prewords3[i]]

    return prewords4,mls

def mmseg(S):
    presegment = []
    while S != "":
        prewords = preprocess(S)
        words,l = pick(prewords)
        S = S[l:]
        presegment += words
    segment = []
    for list in presegment:
        for word in list:
            segment += [word]
    return segment


def now_method(cut):
    select_system = system.get()
    if select_system == 'Using LQ System':
        return seg_cuts(cut)
    elif select_system == 'Using MM System':
        return mmseg(cut)

def text_to_result(list_of_sentences):                           # seg file to final results.
    global eigenword
    global punc
    total_list=[]
    for sentence in list_of_sentences:
        list_of_every_sentence=seg_initialize(sentence)
        result_list=[]
        for cut in list_of_every_sentence:
            if cut in eigenword or cut in punc:
                result_list.append(cut)
            else:
                result_list += now_method(cut)
        total_list += result_list

    total_list=changing(total_list)
    total_text='|'.join(total_list)

    return total_text


def openWindow():
    open_file=filedialog.askopenfilename(title='open file', initialdir = 'C:/',filetypes=[('text', '*.txt')])
    get_file=open(open_file,'r')
    get_text=get_file.read()
    get_file.close()
    inputText.delete(1.0,END)
    inputText.insert(INSERT,get_text)


def goodbye():
    ask=messagebox.askokcancel('HKJ Seg','Do you really want to quit?')
    if ask == True:
        master.destroy()


def copy():
    cut_board=inputText.get(SEL_FIRST,SEL_LAST)
    master.clipboard_clear()
    master.clipboard_append(cut_board)


def paste():
    paste_board=master.clipboard_get()
    inputText.insert(INSERT,paste_board)


def select_all():
    inputText.tag_add(SEL,'1.0',END)
    return 'break'


def clear():
    inputText.delete(1.0,END)
    segText.delete(1.0,END)
    outputText.delete(1.0,END)


def segFile():                                                      # main entry 1
    get_text=inputText.get(1.0,END)
    if get_text == '':
        messagebox.showinfo('Seg Text','Empty input!')
        return

    ask0=messagebox.askyesno('Seg Text','Do you want to see the sentences of the text?')
    show_seg_text, diction, list_of_sentences = sentence_seg(get_text)  # Cut the whole text into a list of sentences.
    if ask0 == True:
        segText.delete(1.0, END)
        segText.insert(INSERT, show_seg_text)

        line_choose = simpledialog.askstring('Choose a sentence', 'Choose a sentence(0 to skip)',initialvalue='Enter here')

        if line_choose == '0':
            outputText.delete(1.0, END)
            outputText.insert(INSERT, 'You skipped the result.\n')
        else:
            sent = diction[line_choose]
            result_of_sentseg = text_to_result([sent])
            outputText.delete(1.0, END)
            outputText.insert(INSERT, result_of_sentseg+'\n')  # seg the chosen sentence.

    ask=messagebox.askyesno('Seg Text','Do you want to output the results into a new text?')
    if ask == True:
        new_built=open('output.txt','w')
        new_built.write(text_to_result(list_of_sentences))
        new_built.close()
        segText.delete(1.0,END)
        outputText.delete(1.0,END)
        messagebox.showinfo('Seg Text','The text has been segmented successfully')


def segSentence():                                                  # main entry 2
    get_sentence=inputText.get(1.0,END)
    if get_sentence == '':
        messagebox.showinfo('Seg Sentence','Empty input!')
        return
    a,b,cut_it=sentence_seg(get_sentence)
    sentence_result=text_to_result(cut_it)
    segText.delete(1.0,END)
    segText.insert(INSERT,'To see the result of sentences segmentation, click Seg -- Segment a text Menu.')
    outputText.delete(1.0,END)
    outputText.insert(INSERT,sentence_result)


def loadLexicon():
    open_lexicon = filedialog.askopenfilename(title='open lexicon', initialdir='C:/', filetypes=[('text', '*.txt')])
    text2=open(open_lexicon,'r')
    text1 = open('Dictionary.txt', 'r')
    p1 = ''
    p2 = ''
    while True:
        x = text2.readline()
        p1 += x
        if len(x) == 0:
            break
    while True:
        y = text1.readline()
        p2 += y
        if len(y) == 0:
            break
    poupou = p1 + '\n' + p2
    text2.close()
    text3 = open('Dictionary.txt', 'w')
    text3.write(poupou)
    text3.close()
    messagebox.showinfo('Import Lexicon','The new lexicon has been imported now.')


def addLexicon():
    add_word = simpledialog.askstring('Add a word', 'Add:', initialvalue='Enter your word here')
    if add_word == None:
        return
    y=add_word
    text = open('Dictionary.txt', 'r')
    x = ''
    while True:
        p = text.readline()
        x += p
        if len(p) == 0:
            break
    x = x.split('\n')
    x = ','.join(x)
    x = '{' + x + '}'
    cp = eval(x)
    text.close()
    if y not in cp.keys():
        cp[y] = 100
        textb = open('Dictionary.txt', 'w')
        cp = str(cp).split(',')
        cp = '\n'.join(cp)
        cp_p = ''
        for i in cp:
            if i != '{':
                if i != '}':
                    cp_p += i
        textb.write(cp_p)
        textb.close()
        messagebox.showinfo('Add Word','The word has been added successfully!')
    else:
        messagebox.showinfo('Add Word','The word is already in the lexicon!')


def editLexicon():
    delete_word = simpledialog.askstring('Delete a word', 'Delete:', initialvalue='Enter your word here')
    if delete_word == None:
        return
    y=delete_word
    text = open('Dictionary.txt', 'r')
    x = ''
    while True:
        p = text.readline()
        x += p
        if len(p) == 0:
            break
    x = x.split('\n')
    x = ','.join(x)
    x = '{' + x + '}'
    cp = eval(x)
    text.close()
    if y in cp.keys():
        del cp[y]
        textb = open('Dictionary.txt', 'w')
        cp = str(cp).split(',')
        cp = '\n'.join(cp)
        cp_p = ''
        for i in cp:
            if i != '{':
                if i != '}':
                    cp_p += i
        textb.write(cp_p)
        textb.close()
        messagebox.showinfo('Delete Word','The word has been deleted successfully!')
    else:
        messagebox.showinfo('Delete Word','The word is not in the lexicon!')


def instruction():
    messagebox.showinfo('Instruction',instructions)


def copyright():
    messagebox.showinfo('Copyright',copyrights)


menubar=Menu(master)
Filemenu=Menu(menubar, tearoff=0)
Filemenu.add_command(label='Open',command=openWindow)
Filemenu.add_separator()
Filemenu.add_command(label='Exit',command=goodbye)
menubar.add_cascade(label="     File     ", menu=Filemenu)

Editmenu=Menu(menubar, tearoff=0)
Editmenu.add_command(label="Copy", command=copy)
Editmenu.add_command(label="Paste",command=paste)
Editmenu.add_command(label="Select all",command=select_all)
Editmenu.add_command(label="Clear all",command=clear)
menubar.add_cascade(label="     Edit     ", menu=Editmenu)

Segmenu=Menu(menubar, tearoff=0)
Segmenu.add_command(label="Segment a text", command=segFile)
Segmenu.add_command(label="Segment a sentence", command=segSentence)
menubar.add_cascade(label="     Segmentation     ", menu=Segmenu)

Leximenu=Menu(menubar, tearoff=0)
Leximenu.add_command(label="Load", command=loadLexicon)
Leximenu.add_command(label="Add a word", command=addLexicon)
Leximenu.add_command(label="Delete a word", command=editLexicon)
menubar.add_cascade(label="     Lexicon     ", menu=Leximenu)

Helpmenu=Menu(menubar, tearoff=0)
Helpmenu.add_command(label="Instructions", command=instruction)
Helpmenu.add_command(label="Copyright", command=copyright)
menubar.add_cascade(label="     Help     ", menu=Helpmenu)
master.config(menu=menubar)


img = Image.open('./148163508354863c.png')
img = ImageTk.PhotoImage(img)
img=PhotoImage(img)

try:
    Label(master,image=img).grid(row=0,column=0,columnspan=3)
except TypeError,e:
    Label(master).grid(row=0, column=0, columnspan=3)
system=StringVar(master)
system.set('Using LQ System')
OptionMenu(master,system,'Using LQ System','Using MM System').grid(row=0,column=0,sticky=SW)
select_system=system.get()
Label(master,text='Version 1.0',height=1,relief=RIDGE).grid(row=1,column=2,sticky=E,padx=10)
Label(master,text='Input:',height=1,width=14,font=('Times',12)).grid(row=2,column=0,sticky=N)
Label(master,text='Sentences Segmentation:',height=1,width=23,font=('Times',12)).grid(row=2,column=1,sticky=N)
Label(master,text='Output:',height=1,width=10,font=('Times',12)).grid(row=2,column=2,sticky=N)
Label(master,text='HKJ Production -- All rights reserved',height=2,width=25,font=('Times',12)).grid(row=4,column=0,columnspan=3,sticky=N)


inputText=Text(master,width=35,height=15,wrap=WORD)
inputText.grid(row=3,column=0,padx=8)

segText=Text(master,width=35,height=15,wrap=WORD)
segText.grid(row=3,column=1,padx=2)

outputText=Text(master,width=35,height=15,wrap=WORD)
outputText.grid(row=3,column=2,padx=8)


master.mainloop()
