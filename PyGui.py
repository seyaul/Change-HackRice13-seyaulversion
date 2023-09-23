import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QWidget, QLabel, QTextEdit, QFormLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import openai
import allocation

#ChNGED
class BudgetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        plt.rcParams["figure.figsize"] = (8, 4)
        
        self.update_button = QPushButton("Update Chart")
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.canvas)
        
        self.update_button.clicked.connect(self.update_chart)
        
        self.setLayout(self.layout)
        
    def update_chart(self):
        allocation.allocate(allocation.balance, allocation.deposit, allocation.user)

        balance_data = list(allocation.balance.values())
        balance_labels = list(allocation.balance.keys())

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(balance_labels, balance_data)
        ax.set_xlabel('Balance Types')
        ax.set_ylabel('Amount')
        ax.set_title('Current Balance Distribution')
        ax.set_xticklabels(balance_labels, rotation=10)

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

        openai.api_key = ''

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

        self.setGeometry(400, 400 ,400, 600)

        # Create a horizontal layout for the logo and other widgets
        self.top_layout = QHBoxLayout()

        # Inserting change logo at top
        self.logo_label = QLabel(self)
        pixmap = QPixmap('logo.png')
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(300, 300)
        self.top_layout.addWidget(self.logo_label)

        # Create a vertical layout for the input fields and buttons
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)


        # Age input field
        self.age_layout = QFormLayout()
        self.age_label = QLabel("Age:")
        self.age_field = QLineEdit()
        self.age_field.editingFinished.connect(self.update_age)
        self.age_layout.addRow(self.age_label, self.age_field)
        self.layout.addLayout(self.age_layout)

        # Deposit Balance input field
        self.deposit_layout = QFormLayout()
        self.deposit_label = QLabel("Balance Deposit:")
        self.deposit_field = QLineEdit()
        self.deposit_field.editingFinished.connect(self.update_deposit)
        self.deposit_layout.addRow(self.deposit_label, self.deposit_field)
        self.layout.addLayout(self.deposit_layout)

        # Salary input field
        self.salary_layout = QFormLayout()
        self.salary_label = QLabel("Salary:")
        self.salary_field = QLineEdit()
        self.salary_field.editingFinished.connect(self.update_salary)
        self.salary_layout.addRow(self.salary_label, self.salary_field)
        self.layout.addLayout(self.salary_layout)

        #Plan option drop down
        # Plan option drop down
        self.plan_layout = QFormLayout()
        self.plan_label = QLabel("Plan:")
        self.risk_level_combobox = QComboBox()
        self.risk_level_combobox.addItem("Default")
        self.risk_level_combobox.addItem("High Risk Long Term")
        self.risk_level_combobox.addItem("Low Risk Long Term")
        self.risk_level_combobox.addItem("High Risk Short Term")
        self.risk_level_combobox.addItem("Low Risk Short Term")
        self.risk_level_combobox.currentIndexChanged.connect(self.update_risk)
        self.plan_layout.addRow(self.plan_label, self.risk_level_combobox)
        self.layout.addLayout(self.plan_layout)

        

        # Chat bot button
        self.chat_button = QPushButton("Go to Chat", self)
        self.chat_button.setStyleSheet('QPushButton {border: 1px solid black;}')
        self.chat_button.clicked.connect(self.open_chat_window)

        # Budget screen button
        self.button = QPushButton("Go to Budget", self)
        self.button.setStyleSheet('QPushButton {border: 1px solid black;}')
        self.button.clicked.connect(self.open_budget_window)

        # Add buttons to the layout
        self.layout.addWidget(self.chat_button)
        self.layout.addWidget(self.button)

        # Add the top_layout and layout to a QVBoxLayout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.layout)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)


    def update_deposit(self):
        deposit = int(self.deposit_field.text())
        allocation.deposit = deposit

    def update_risk(self, index):
        selected_option = self.risk_level_combobox.itemText(index)
        allocation.user['Plan'] = selected_option

    def update_age(self):
        age = int(self.age_field.text())
        allocation.user['Age'] = age

    def update_salary(self):
        salary = int(self.salary_field.text())
        allocation.user['Salary'] = salary


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