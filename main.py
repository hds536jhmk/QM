
# IMPORTING LIBRARIES
import tkinter as tk
import json

# GLOBAL VARIABLES
settings = {}
with open('./settings.json') as json_data:
    settings = json.load(json_data)

questions = {}
with open('./questions.json') as json_data:
    questions = json.load(json_data)

# FUNCTIONS

def map(value, minValue, maxValue, min, max):
    return (value - minValue) / (maxValue - minValue) * (max - min) + min


# CREATING APPLICATION


class Question:
    def __init__(self, question):
        self.question = question
        self.answers = []

    def addAnswer(self, answer, rb):
        self.answers.append([answer, rb])

    def check(self):
        i = 0
        for answer in self.answers:
            if answer[0]['isCorrect']:
                if answer[1].get() == i:
                    return True
                    pass
            i += 1

class App:

    def checkAnswers(self):
        self.points = 0
        for question in self.questions:
            if question.check():
                self.points += settings['questConfig']['points']['trueAnswer']
            else:
                self.points += settings['questConfig']['points']['falseAnswer']
        if self.points < 0:
            self.points = 0
        childWinSettings = settings['mainWindow']['children']
        vote = map(self.points, 0, settings['questConfig']['points']['trueAnswer'] * self.questions.__len__(), 1, 10)
        vote = "{0:.1f}".format(vote)
        self.lPoints.config(text=childWinSettings['lPoints']['caption'] + str(self.points) + ' - ' + str(vote))
        self.lPoints.pack(side=tk.RIGHT)

    def configWidget(self, widget, configObject):
        if 'colors' in configObject:
            _colors = configObject['colors']
            widget.config(background=_colors['bg'], foreground=_colors['fg'])
        if 'font' in configObject:
            _font = configObject['font']
            widget.config(font=(_font['name'], _font['size'], _font['style']))


    def createWidgets(self):
        childWinSettings = settings['mainWindow']['children']

        # CREATING TITLE
        self.lTitle = tk.Label(self.root, text=childWinSettings['lTitle']['caption'])
        self.configWidget(self.lTitle, childWinSettings['lTitle'])
        self.lTitle.pack()

        for question in questions['quest']:
            _question = Question(question)

            _qTitleLabel = tk.Label(self.root, text=question['caption'])
            self.configWidget(_qTitleLabel, question)
            _qTitleLabel.pack(fill=tk.X)

            i = 0
            var = tk.IntVar()
            for answer in question['answers']:
                _qRadioButton = tk.Radiobutton(self.root, text=answer['caption'], variable=var, value=i)
                self.configWidget(_qRadioButton, answer)
                _qRadioButton.pack(fill=tk.X)

                _question.addAnswer(answer, var)
                i += 1

            self.questions.append(_question)

        self.bConfirm = tk.Button(self.root, text=childWinSettings['bConfirm']['caption'], command=self.checkAnswers)
        self.configWidget(self.bConfirm, childWinSettings['bConfirm'])
        self.bConfirm.pack(side=tk.LEFT)

        self.lPoints = tk.Label(self.root, text=childWinSettings['lPoints']['caption'] + '0 - 1.0')
        self.configWidget(self.lPoints, childWinSettings['lPoints'])

    def __init__(self, root):
        self.root = root
        self.points = 0
        self.questions = []
        self.createWidgets()


# CREATING MAIN WINDOW
mainWindow = tk.Tk()
mainWindow.title(settings['mainWindow']['title'])
mainWindow.iconbitmap('./logo.ico')
mainWindow.resizable(settings['mainWindow']['resizeable']['width'], settings['mainWindow']['resizeable']['height'])
mainWindow.minsize(settings['mainWindow']['size']['width'], settings['mainWindow']['size']['height'])

# INITIALIZING APP
app = App(root=mainWindow)

# MAINLOOP
mainWindow.mainloop()

