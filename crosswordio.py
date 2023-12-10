from tkinter import *
from tkinter import font
from tkinter import filedialog as fd
import json


EditMode = False

rows = 10 #Размеры пустого поля
columns = 13
CellLayout ={} # {(x,y):Cell}
Words = [] #[{}]
Clues = [] # [Clue]





#Фунция для расстановки id словам
def makeWordsId():
    global Words,Clues
    #Сброс
    for i in CellLayout.values():
        i.setVId(-1)
        i.setHId(-1)
    tempWords = []
    counter = 0 #Отвечает за id
    wordLen = 0 #Длина найденого слова
    wordStart=(-1,-1) #Старотовая точка для слова
    #Горизонтальная проверка
    for y in range(rows):
        #Проверка если с предыдущей линии было слово
        if wordLen>2: #Если слово больше 2 букв
            word=""
            for i in range(wordLen):
                CellLayout[wordStart[0]+i,wordStart[1]].setHId(counter,i==0) #Расставляем id
                word+=CellLayout[wordStart[0]+i,wordStart[1]].char #Добавляем в найденное слово букву
                #добавляем в временный массив слово
            tempWords.append({"text":word,"x":wordStart[0],"y":wordStart[1],"vertical":False,"clue":""})
            counter+=1
        wordLen = 0
        #Сканируем по горизонтали 
        for x in range(columns):
            c = CellLayout[(x,y)]
            if c.char: #Если найдена буква
                wordLen+=1
                if wordLen == 1:
                    wordStart = (x,y) #Устанавливаем стартовую точку для найденого слова
            elif wordLen>2:#Если слово больше 2 букв
                word=""
                for i in range(wordLen):
                    CellLayout[wordStart[0]+i,wordStart[1]].setHId(counter,i==0) #Расставляем id
                    word=word+CellLayout[wordStart[0]+i,wordStart[1]].char #Добавляем в найденное слово букву
                    #добавляем в временный массив слово
                tempWords.append({"text":word,"x":wordStart[0],"y":wordStart[1],"vertical":False,"clue":""})
                counter+=1
                wordLen=0
            else:
                wordLen=0
    wordLen=0
    #Сканируем по вертикали 
    for x in range(columns):
        #Проверка если с предыдущей линии было слово
        if wordLen>2: #Если слово больше 2 букв
            word=""
            for i in range(wordLen):
                CellLayout[wordStart[0],wordStart[1]+i].setHId(counter,i==0)#Расставляем id
                word+=CellLayout[wordStart[0],wordStart[1]+i].char #Добавляем в найденное слово букву
            #добавляем в временный массив слово
            tempWords.append({"text":word,"x":wordStart[0],"y":wordStart[1],"vertical":True,"clue":""})
            counter+=1
        wordLen = 0
        for y in range(rows):
            c = CellLayout[(x,y)]
            if c.char: #Если найдена буква
                wordLen+=1
                if wordLen == 1:
                    wordStart = (x,y) #Устанавливаем стартовую точку для найденого слова
            elif wordLen>2: #Если слово больше 2 букв
                word=""
                for i in range(wordLen):
                    CellLayout[wordStart[0],wordStart[1]+i].setVId(counter,i==0)#Расставляем id
                    word=word+CellLayout[wordStart[0],wordStart[1]+i].char #Добавляем в найденное слово букву
                #добавляем в временный массив слово
                tempWords.append({"text":word,"x":wordStart[0],"y":wordStart[1],"vertical":True,"clue":""})
                counter+=1
                wordLen=0
            else:
                wordLen=0
    wordLen=0
    
    #Если полей для подсказок больше чем найденый слов
    if len(tempWords)>len( CluesFrame.winfo_children()):
        for i in range(len( CluesFrame.winfo_children()),len(tempWords)):
            Clue(i+1,tempWords[i]["text"]) #Добавляем недостающие поля
    #Если полей для подсказок меньше чем найденый слов
    if len(tempWords)< len( CluesFrame.winfo_children()):
        for i in range(len(tempWords)+1,len( CluesFrame.winfo_children())+1):
            CluesFrame.winfo_children()[-1].destroy() #Удаляем поле из панели

    #Обновляем массив ссылок на подсказки
    Clues=[]
    for n,i in enumerate(CluesFrame.winfo_children()):
        i.setLabelText(tempWords[n]["text"]) #Выставляем текст для подсказки
        Clues.append(i) #Добавляем ссылку
    Words=tempWords #Обновляем список слов

#Фунция для преобразования строки в строку с переводом строки
def createMultiLine(text):
    res = ""
    nextLineSeparator = 30 #Порог по длинне строки
    for i in text.split(" "): #Раздеяем на слова
        res+=i+" "
        if len(res)>nextLineSeparator: #Проверка на длинну строки
            res+="\n" # Добавляем разделитель
            nextLineSeparator=len(res)+30 #Увеличиваем порог
    return res.rstrip() # Возвращаем очищенный результат

#Класс виджета подсказки
class Clue(Frame):
    l=None
    e=None
    id=-1
    clue=""

    def setLabelText(self,text):
        self.l.configure(text=str(self.id)+". "+text)

    #Фунция для получения текста из введёного текста
    def getEntryText(self):
        if self.e is not None:
            return self.e.get()
    #Функция чтобы отметить подсказку для решённого слова
    def setSolved(self):
        self.l.configure(background="green")
    #Конструктор объекта
    def __init__(self,id,word="",clue="", **kw):
        super().__init__(CluesFrame, **kw)
        self.pack()
        self.id=id
        self.clue = createMultiLine(clue)
        if EditMode:
            self.l= Label(self,text=str(id)+". "+word,font=CrossFont)
            self.l.pack()
            entry_text = StringVar()
            self.e = Entry(self,textvariable=entry_text,font=CrossFont)
            entry_text.set(clue)
            self.e.pack()
        else:
            self.l= Label(self,text=str(id)+". "+self.clue,font=CrossFont)
            self.l.pack()

#Класс виджета для ячеек
class Cell(Canvas):
    locked=0 # 0-слово не решено, 1 - слово решено
    hId = -1 #id слова по горизонтали
    vId = -1 #id слова по вертикали
    focus = False #есть ли фокус на ячейке
    char = "" # символ вписанный в ячейку
    drawHId = False #рисовать ли id слова
    drawVId = False
    x = -1 # координаты ячейки
    y = -1
    def draw(self): #Функция для отрисовки
        self.delete("all") #Очищаем
        self.configure(height=60,width=60)#Ставим размер

        if self.focus: #Если есть фокус то делаем зелёным
            self.configure(bg="green")
        elif EditMode: 
            self.configure(bg="lightgreen" if (self.vId!=-1 or self.hId!=-1) else "gray")
        else:
            self.configure(bg="lightgreen")
        if self.locked: #Если ячейка заблокирована то делаем жёлтым
            self.configure(bg="yellow")
        if self.drawHId: #Блок отрисовки номеров
            self.create_text(15,8,text=str(self.hId+1))
        if self.drawVId:
            self.create_text(10,20,text=str(self.vId+1))
        #Отрисовка введённой буквы
        self.create_text(30,30,text=self.char.capitalize(), justify="center", font=CrossFont,width=2)
        
        
    #Заблокировать ячейку
    def lock(self):
        self.locked = 1
        self.draw()
    #Поставить цифру и перисовать ячейку
    def setChar(self,c):
        self.char = c
        self.draw()
    #Поставить id горизонтального слова
    def setHId(self,id,draw=False):
        self.hId=id
        self.drawHId=draw
        self.draw()
    #Поставить id вертикального слова
    def setVId(self,id,draw=False):
        self.vId=id
        self.drawVId=draw
        self.draw()
    #Когда фокус
    def OnFocus(self,isFocused):
        self.focus = isFocused
        self.draw()

    #Конструктор объекта
    def __init__(self,x,y,char="", **kw):
        super().__init__(CrossWordFrame, **kw)
        self.char = char
        self.x=x
        self.y=y
        self.bind('<Key>', lambda event:self.InputFunc(event))
        self.bind('<Button-1>', lambda event:self.focus_set())
        self.bind('<FocusIn>', lambda event:self.OnFocus(True))
        self.bind('<FocusOut>', lambda event:self.OnFocus(False))
        self.draw()
    #Фунция обработки клавиш
    def InputFunc(self,event:Event):
        
        if event.char.isalpha(): #Если кнопка это буква
            if not self.locked:
                self.char = event.char.capitalize()
            if EditMode:
                makeWordsId()
            else:
                CheckWord(self)
        elif event.keysym=="Up": #Блок проверки для перемещения по стрелочкам
            try:
                CellLayout[(self.x,self.y-1)].focus_set()
            except KeyError:
                pass
        elif event.keysym=="Right":
            try:
                CellLayout[(self.x+1,self.y)].focus_set()
            except KeyError:
                pass
        elif event.keysym=="Left":
            try:
                CellLayout[(self.x-1,self.y)].focus_set()
            except KeyError:
                pass
        elif event.keysym=="Down":
            try:
                CellLayout[(self.x,self.y+1)].focus_set()
            except KeyError:
                pass
            #Блок для удаления буквы из ячейки
        elif event.keysym=="Delete" or event.keysym=="BackSpace":
            if EditMode:
                self.char = ""
                self.setVId(-1)
                self.setHId(-1)
                makeWordsId()
            elif not self.locked:
                self.char = ""
        self.draw()




def CheckWord(c:Cell):
    v,h = c.vId, c.hId #Получаем id слов
    correctWord = True #Изначально предполагаем что слово верное
    #Проверяем вертикально
    x = Words[v]["x"] #Получаем координаты ячеек для проверки
    y = Words[v]["y"]
    length =len( Words[v]["text"])
    if (v!=-1):
        for i in range(length): #В цикле по направлению проверяем что буквы в ячейках
            if Words[v]["text"][i] != CellLayout[(x,y+i)].char:
                correctWord = False
                break
        if correctWord:#Если слово правильное
            for i in range(len(Words[v]["text"])):
                CellLayout[(x,y+i)].lock() #Блокируем ячейку
                Clues[v].setSolved() #Отмечаем что слово решено

    #Проверяем горизонтально
    if(h!=-1):
        correctWord = True
        x = Words[h]["x"] #Получаем координаты ячеек для проверки
        y = Words[h]["y"]
        length =len( Words[h]["text"] )
        for i in range(length): #В цикле по направлению проверяем что буквы в ячейках
            if Words[h]["text"][i] != CellLayout[(x+i,y)].char:
                correctWord = False
                break
        if correctWord:#Если слово правильное
            for i in range(len(Words[h]["text"])):
                    CellLayout[(x+i,y)].lock() #Блокируем ячейку
                    Clues[h].setSolved() #Отмечаем что слово решено


def loadCrossword():
    global Words
    file = fd.askopenfilename()
    Words = json.load(open(file,"r"))
    createField()
def saveCrossword():
    global Words
    file = fd.asksaveasfilename()
    print(Words,Clues)
    for n, i in enumerate(Clues):
        Words[n]["clue"] = i.getEntryText()
    json.dump(Words,open(file,"w"))

def loadCrosswordForEdit():
    global EditMode
    EditMode =True
    hideStartUpButtons()
    clearCross()
    createEmpty()
    loadCrossword()
    

def loadCrosswordForPlay():
    global EditMode
    EditMode = False
    hideStartUpButtons()
    clearCross()
    loadCrossword()
    
def createEmpty():
    global EditMode,CellLayout
    EditMode = True
    hideStartUpButtons()
    clearCross()
    #Создаём поле пустых ячеек
    for y in range(rows):
            for x in range(columns):
                c=CellLayout[(x,y)]= Cell(x,y,char="")
                c.grid(row = y,column=x)
    

def clearCross():
    global CellLayout,Words,Clues

    for child in CluesFrame.winfo_children():
            child.destroy()
    for child in CrossWordFrame.winfo_children():
            child.destroy()
    CellLayout={}
    Words=[]
    Clues=[]


#Фукнция для загрузки поля
def createField():

    for n,i in enumerate(Words):
        Clues.append(Clue(n+1,i["text"],i["clue"]))

    for n, i in enumerate(Words):
        if i["vertical"]:
            for y,char in enumerate(i["text"]):
                if (i["x"],i["y"]+y) in CellLayout:
                    CellLayout[(i["x"],i["y"]+y)].setVId(n,draw= True if y==0 else False)
                    CellLayout[(i["x"],i["y"]+y)].setChar(char if EditMode else "")
                else:
                    c = Cell(i["x"],i["y"]+y,char= char if EditMode else "")
                    c.setVId(n,draw= True if y==0 else False)
                    c.grid(column =i["x"],row = i["y"]+y)
                    CellLayout[(i["x"],i["y"]+y)] =c
        else:
            for x,char in enumerate(i["text"]):
                if  (i["x"]+x,i["y"]) in CellLayout:
                    CellLayout[(i["x"]+x,i["y"])].setHId(n,draw= True if x==0 else False)
                    CellLayout[(i["x"]+x,i["y"])].setChar(char if EditMode else "")
                else:
                    c = Cell(i["x"]+x,i["y"],char=char if EditMode else "")
                    c.setHId(n,draw= True if x==0 else False)
                    c.grid(column =i["x"]+x,row = i["y"])
                    CellLayout[(i["x"]+x,i["y"])] =c



root = Tk()
CrossFont = font.Font(size=25) #Создаём шрифт который используется в большинстве элементов
root.geometry("1700x890+0+0") #Ставим размер окна

photo =PhotoImage(file="fon.png") #Ставим фоновое изображение
bg = Label(root,image=photo)
bg.place(x=0,y=0)

ButtonFrame = Frame(root)
ButtonFrame.pack(side="top")

loadButtonEmptyPhoto =PhotoImage(file="button1.png")
loadButtonEmpty = Button(root,background="#322951",image=loadButtonEmptyPhoto,command=createEmpty)
loadButtonEmpty.place(x=600,y=270)

loadButtonEditPhoto =PhotoImage(file="button2.png")
loadButtonEdit = Button(root,background="#322951",image=loadButtonEditPhoto,command=loadCrosswordForEdit)
loadButtonEdit.place(x=630,y=400)

loadButtonPlayPhoto =PhotoImage(file="button3.png")
loadButtonPlay = Button(root,background="#322951",image=loadButtonPlayPhoto,command=loadCrosswordForPlay)
loadButtonPlay.place(x=700,y=500)

loadButtonEditTop = Button(ButtonFrame,background="#988cc5",font=font.Font(size=20),text="Открыть для редактирования",command=loadCrosswordForEdit)
loadButtonEmptyTop = Button(ButtonFrame,background="#988cc5",font=font.Font(size=20),text="Создать пустой для редактирования",command=createEmpty)
loadButtonPlayTop = Button(ButtonFrame,background="#988cc5",font=font.Font(size=20),text="Открыть для игры",command=loadCrosswordForPlay)
saveButtonTop = Button(ButtonFrame,background="#988cc5",font=font.Font(size=20),text="Сохранить",command=saveCrossword)
hasTopButtons=False #Показана ли верхеяя панель кнопок
#Фунция для сокрытия центральных кнопок и показа верхних
def hideStartUpButtons():
    global hasTopButtons
    loadButtonEmpty.destroy()
    loadButtonEdit.destroy()
    loadButtonPlay.destroy()
    if not hasTopButtons:
        hasTopButtons=True
        loadButtonEmptyTop.pack(side="left")
        loadButtonEditTop.pack(side="left")
        loadButtonPlayTop.pack(side="left")
        saveButtonTop.pack(side="left")

CrossWordFrame = Frame(root, bg = 'gray')
CrossWordFrame.pack(side="left",padx=100)
CluesFrame = Frame(root)
CluesFrame.pack(side="right",padx=100)

root.mainloop()