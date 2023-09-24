# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
from gui.uis.windows.main_window.setup_main_window import *

import sys
import os


#Test imports
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QTextEdit, QFormLayout, QHBoxLayout, QComboBox
from PySide6.QtGui import QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import openai
from gui.uis.windows.main_window import allocation

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN s
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
#os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
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
    
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()
        #All the Input Fields

        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Please Enter Your Age...")
        self.input_box.setFont(QFont("Arial", 12))  # Set font and size
        self.input_box.setStyleSheet("background-color: #FFFFFF; border: 2px solid #CCCCCC; border-radius: 8px; font-size: 20px")
        self.input_box.setFixedWidth(800)  # Set the desired width
        self.input_box.setFixedHeight(50) 
        try:
            self.input_box.editingFinished.connect(self.update_age)
        except:
            print("empty")

        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("Please Enter Your Salary...")
        self.input_box2.setFont(QFont("Arial", 20))  # Set font and size
        self.input_box2.setStyleSheet("background-color: #FFFFFF; border: 2px solid #CCCCCC; border-radius: 8px; font-size: 20px")
        self.input_box2.setFixedWidth(800)  # Set the desired width
        self.input_box2.setFixedHeight(50) 
        try: 
            self.input_box2.editingFinished.connect(self.update_salary)
        except:
            print("empty")
        

        self.input_box3 = QLineEdit(self)
        self.input_box3.setPlaceholderText("Please Enter How Much You Will Deposit...")
        self.input_box3.setFont(QFont("Arial", 20))  # Set font and size
        self.input_box3.setStyleSheet("background-color: #FFFFFF; border: 2px solid #CCCCCC; border-radius: 8px; font-size: 20px")
        self.input_box3.setFixedWidth(800)  # Set the desired width
        self.input_box3.setFixedHeight(50) 
        try:    
            self.input_box3.editingFinished.connect(self.update_deposit)
        except:
            print("empty")


        self.combo_box = QComboBox()
        self.combo_box.addItems(["Default", "High-Risk Longterm", "High-Risk Shortterm", "Low-Risk Longterm", "Low-Risk Shortterm"])
        self.combo_box.setFont(QFont("Arial", 20))
        self.combo_box.setStyleSheet("background-color: #FFFFFF; border: 2px solid #CCCCCC; border-radius: 8px;font-size: 20px")
        self.combo_box.setFixedWidth(800)
        self.combo_box.setFixedHeight(50)
        try:
            self.combo_box.currentIndexChanged.connect(self.update_risk)
        except:
            print("empty")
        
        # PUSH BUTTON 2
        self.push_button_2 = PyPushButton(
            text = "Calculate!", 
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
            
        )
        self.push_button_2.clicked.connect(self.open_budget_window)
        
         
        #self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.push_button_2.setMinimumHeight(40)
        #self.push_button_2.setIcon(self.icon_2)

        self.ui.load_pages.row_1_layout.addWidget(self.input_box)
        self.ui.load_pages.row_1_layout.setAlignment(self.input_box, Qt.AlignmentFlag.AlignLeft)
        self.ui.load_pages.row_2_layout.addWidget(self.input_box2)
        self.ui.load_pages.row_2_layout.setAlignment(self.input_box2, Qt.AlignmentFlag.AlignLeft)
        self.ui.load_pages.row_3_layout.addWidget(self.input_box3)
        self.ui.load_pages.row_3_layout.setAlignment(self.input_box3, Qt.AlignmentFlag.AlignLeft)
        self.ui.load_pages.row_4_layout.addWidget(self.combo_box)
        self.ui.load_pages.row_4_layout.setAlignment(self.combo_box, Qt.AlignmentFlag.AlignLeft)
        self.ui.load_pages.row_5_layout.addWidget(self.push_button_2)


    def update_age(self):
        #age = int(self.input_box.text())
        age_text = self.input_box.text()
        print("aaaa")
        if age_text:
            try:
                age = int(age_text)
                allocation.user['Age'] = age
                print(age)
            except ValueError:
                # Handle the case where the input is not a valid integer
                print(age)
        else:
            # Handle the case where the input is empty
            print("Empty")
        
        

    def update_salary(self):
        #salary = int(self.input_box2.text())
        sal_text = self.input_box2.text()
        if sal_text:
            try:
                salary = int(sal_text)
                allocation.user['Salary'] = salary
                print(salary)
            except ValueError:
                # Handle the case where the input is not a valid integer
                print(salary)
        else:
            # Handle the case where the input is empty
            print("Empty")
        #allocation.user['Salary'] = salary
    
    def update_deposit(self):
        #deposit = int(self.input_box3.text())
        dep_text = self.input_box3.text()
        if dep_text:
            try:
                deposit = int(dep_text)
                allocation.deposit = deposit
                print(deposit)
            except ValueError:
                # Handle the case where the input is not a valid integer
                print(deposit)
        else:
            # Handle the case where the input is empty
            print("Empty")
        #allocation.deposit = deposit

    def update_risk(self, index):
        sel_opt = self.combo_box.text()
        if sel_opt:
            try:
                selected_option = self.combo_box.itemText(index)
                allocation.user['Plan'] = selected_option
                print(selected_option)
            except ValueError:
                # Handle the case where the input is not a valid integer
                print(selected_option)
        else:
            # Handle the case where the input is empty
            print("Empty")
        #allocation.user['Plan'] = selected_option

    

    # def update_age(self):
    #     age = int(setup_main_window.input_box.text())
    #     allocation.user['Age'] = age

    # def update_salary(self):
    #     salary = int(setup_main_window.input_box2.text())
    #     allocation.user['Salary'] = salary
    
    # def update_deposit(self):
    #     deposit = int(setup_main_window.input_box3.text())
    #     allocation.deposit = deposit

    # def update_risk(self, index):
    #     selected_option = self.risk_level_combobox.itemText(index)
    #     allocation.user['Plan'] = selected_option





    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active         
        #top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        #top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////
        
        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)
        
        # if btn.objectName() == "calculate":



        # WIDGETS BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # LOAD USER PAGE
        if btn.objectName() == "btn_add_user":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_3)


        #TEST BUTTON 4
        if btn.objectName() == "btn_test":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 4 
            MainFunctions.set_page(self, self.ui.load_pages.page_4)


        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)            

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    def open_budget_window(self):
        self.budget_window = BudgetWindow()
        self.budget_window.show()
    

    def open_chat_window(self):
        self.chat_window = ChatWindow()
        self.chat_window.show()
    









# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()



    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec())