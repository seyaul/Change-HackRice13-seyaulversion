import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QWidget, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import openai

class BudgetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.age_field = QLineEdit()
        self.salary_field = QLineEdit()
        self.update_button = QPushButton("Update Chart")
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        
        self.layout.addWidget(self.age_field)
        self.layout.addWidget(self.salary_field)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.canvas)
        
        self.update_button.clicked.connect(self.update_chart)
        
        self.setLayout(self.layout)
        
    def update_chart(self):
        age = int(self.age_field.text())
        salary = int(self.salary_field.text())
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie([age, salary], labels=["Age", "Salary"])
        self.canvas.draw()

class ChatWindow(QWidget):
    current_messages = []
    current_messages.append({"role": "system", "content": 
                             "You are a talented financial assistant, answering financial literacy questions with expert ability. You can provide information on how to make smart financial decision, and information on financial institutions in general. Limit all your responses to a few paragraphs AT MOST, you want to express the information in a clear and concise way, while limiting the amount of characters used."})
    
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()

        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)

        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.update_chat)

        self.layout.addWidget(self.chat_log)
        self.layout.addWidget(self.user_input)

        self.setLayout(self.layout)

        openai.api_key = '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'

        self.chat_log.append("Meet our AI-powered financial advisor, willing to answer any and all financial questions!")
        self.chat_log.append(' ')

    def update_chat(self):

        user_message = self.user_input.text()
        self.chat_log.append(f'<strong>User:</strong> {user_message}\n\n')
        self.chat_log.append(' ')


        # creating message dict
        message_as_dict = {"role": "user", "content": user_message}

        # adding new message as dict to list of messages
        self.current_messages.append(message_as_dict)

        # creating chat model with updated list of messages
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self.current_messages
        )

        # getting model reply
        reply = completion.choices[0].message

        # updating list of messages with model's reply
        self.current_messages.append(reply)

        # returning model's reply
    
        self.chat_log.append(f'<strong>&cent;hange Advisor:</strong> {reply["content"]}\n\n')
        self.chat_log.append(' ')
        self.user_input.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #chat bot button
        self.chat_button = QPushButton("Go to Chat", self)
        self.chat_button.setStyleSheet('QPushButton {border: 1px solid black;}')
        self.chat_button.clicked.connect(self.open_chat_window)

        #Budget screen button
        self.setGeometry(100, 100, 400, 400)
        self.button = QPushButton("Go to Budget", self)
        self.button.setStyleSheet('QPushButton {border: 1px solid black;}')

        #Inserting change logo at top
        logo = QLabel(self)
        pixmap = QPixmap('logo.png')  
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)
        logo.setFixedSize(300, 300)
        logo.move(50, -100)

        self.button.clicked.connect(self.open_budget_window)
        self.button.move((self.width() - self.button.width()) // 2, self.height() - self.button.height())

    def open_budget_window(self):
        self.budget_window = BudgetWindow()
        self.budget_window.show()
    

    def open_chat_window(self):
        self.chat_window = ChatWindow()
        self.chat_window.show()

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())