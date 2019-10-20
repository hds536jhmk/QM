
# IMPORTING LIBRARIES
import tkinter as tk
import tkinter.font as tkf
import json
import math

# GLOBAL VARIABLES
settings = {}
with open('./settings.json') as json_data:
    settings = json.load(json_data)

questions = {}
with open('./questions/' + settings['questionGroup']) as json_data:
    questions = json.load(json_data)

# FUNCTIONS

def map(value, minValue, maxValue, min, max):
    return (value - minValue) / (maxValue - minValue) * (max - min) + min

def betterRound(x, precision, base):
  return round(base * round(float(x)/base), precision)

# GLOBAL CLASSES


# QUESTION CLASS:
#  it holds a question and all the answers to it and manages them
class Question:
    # Creates question
    def __init__(self, question):
        self.question = question
        self.answers = []

    # Adds an answer to the answers array
    def addAnswer(self, answer, rb):
        self.answers.append([answer, rb])

    # Checks if the answer is correct
    def check(self):
        i = 0
        # Loops through all the answers
        for answer in self.answers:
            # Checks if answer is correct
            if answer[0]['isCorrect']:
                # Checks if the pressed radiobutton is the correct one
                if answer[1].get() == i:
                    # If so it return true
                    return True
            i += 1


class App:
    # Checks through all questions and calculates points
    def checkAnswers(self):
        # Reset current points
        self.points = 0

        # Loop through every question
        for question in self.questions:
            # Check if question is correct and add points accordingly
            if question.check():
                self.points += self.questionsConfig['points']['trueAnswer']
            else:
                self.points += self.questionsConfig['points']['falseAnswer']

        # If the points are less than 0 set them to 0
        if self.points < 0:
            self.points = 0

        # Calculate vote based on Questions Config
        worstVote = self.questionsConfig['points']['worstVote']
        bestVote = self.questionsConfig['points']['bestVote']
        vote = map(self.points, 0, self.questionsConfig['points']['trueAnswer'] * len(self.questions), 1, bestVote)
        vote = betterRound(vote, 1, .5)

        # If vote is less than the worst one set the vote to it
        if vote < worstVote:
            vote = worstVote

        # Change points label
        self.lPoints.config(text=self.childFBottomSettings['lPoints']['text'] + str(self.points) + ' - ' + str(vote))
        self.lPoints.pack(side=tk.RIGHT, anchor=tk.S)

    # Utility function that sets object options based on a config
    def configWidget(self, widget, objectConfig):
        if 'text' in objectConfig:
            widget.config(text=objectConfig['text'])

        if 'colors' in objectConfig:
            _colors = objectConfig['colors']
            if 'bg' in _colors:
                widget.config(background=_colors['bg'])

            if 'fg' in _colors:
                widget.config(foreground=_colors['fg'])

        if 'font' in objectConfig:
            _font = objectConfig['font']
            newFont = tkf.Font()
            if 'family' in _font:
                newFont.config(family=_font['family'])
            if 'size' in _font:
                newFont.config(size=_font['size'])
            if 'weight' in _font:
                newFont.config(weight=_font['weight'])
            if 'slant' in _font:
                newFont.config(slant=_font['slant'])
            if 'underline' in _font:
                newFont.config(underline=_font['underline'])
            if 'overstrike' in _font:
                newFont.config(overstrike=_font['overstrike'])
            widget.config(font=newFont)

        if 'pad' in objectConfig:
            _pad = objectConfig['pad']
            if 'x' in _pad:
                widget.config(padx=_pad['x'])
            if 'y' in _pad:
                widget.config(pady=_pad['y'])

    # Creates every widget
    def createWidgets(self):

        # Create a frame that stays on the top of the application
        self.fTop = tk.Frame(self.root)
        self.configWidget(self.fTop, self.childMainWindowSettings['fTop'])
        self.fTop.pack(side=tk.TOP, fill=tk.X)

        # Create a frame that stays in the middle of the application
        self.fMiddle = tk.Frame(self.root)
        self.configWidget(self.fMiddle, self.childMainWindowSettings['fMiddle'])
        self.fMiddle.pack(fill=tk.X)

        # Create a frame that stays on the bottom of the application
        self.fBottom = tk.Frame(self.root)
        self.configWidget(self.fBottom, self.childMainWindowSettings['fBottom'])
        self.fBottom.pack(side=tk.BOTTOM, fill=tk.X)

        # Create Application Title
        self.lTitle = tk.Label(self.fTop)
        self.configWidget(self.lTitle, self.childFTopSettings['lTitle'])
        self.lTitle.pack()

        # Create Questions Title
        self.lQuestionsTitle = tk.Label(self.fTop)
        self.configWidget(self.lQuestionsTitle, questions['title'])
        self.lQuestionsTitle.pack()

        # Loop through every question in the questions json
        qI = 0
        for question in questions['questions']:
            # Create new question
            _question = Question(question)

            # Calculate position of questions
            _questionsPerColumn = self.questionsConfig['questionsPerColumn']
            _questionRow = 0
            _questionColumn = math.ceil((len(self.questions) + 1) / _questionsPerColumn) - 1

            if len(self.questions) - _questionsPerColumn * _questionColumn > 0:
                for key in range(_questionsPerColumn * _questionColumn, qI):
                    _questionRow += len(self.questions[key].answers) + 1

            # Create Question label
            _qTitleLabel = tk.Label(self.fMiddle)
            self.configWidget(_qTitleLabel, question)
            self.configWidget(_qTitleLabel, self.questionsConfig)
            _qTitleLabel.grid(row=_questionRow, column=_questionColumn)

            # Loop through every answer
            aI = 0
            var = tk.IntVar()
            for answer in question['answers']:
                # Create a radiobutton for every answer
                _qRadioButton = tk.Radiobutton(self.fMiddle, variable=var, value=aI)
                self.configWidget(_qRadioButton, answer)
                self.configWidget(_qRadioButton, self.questionsConfig)
                _qRadioButton.grid(row=aI + _questionRow + 1, column=_questionColumn)

                # Add answer to the question
                _question.addAnswer(answer, var)
                aI += 1

            # Append question to the questions array
            self.questions.append(_question)
            qI += 1



        # Create confirm button
        self.bConfirm = tk.Button(self.fBottom, command=self.checkAnswers)
        self.configWidget(self.bConfirm, self.childFBottomSettings['bConfirm'])
        self.bConfirm.pack(side=tk.LEFT, anchor=tk.S)

        # Create points label
        self.lPoints = tk.Label(self.fBottom)
        self.configWidget(self.lPoints, self.childFBottomSettings['lPoints'])

    def __init__(self, root):
        self.root = root
        self.points = 0
        self.questions = []
        self.questionsConfig = questions['settings']
        self.childMainWindowSettings = settings['mainWindow']['children']
        self.childFTopSettings = self.childMainWindowSettings['fTop']['children']
        self.childFMiddleSettings = self.childMainWindowSettings['fMiddle']['children']
        self.childFBottomSettings = self.childMainWindowSettings['fBottom']['children']
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

