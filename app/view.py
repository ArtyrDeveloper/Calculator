from tkinter import *
from tkinter import ttk
import sys
from typing import Tuple
import view_buttons
sys.path.append('D:\\Education\\Python\\MyCalculator\\')
from General import singleton
from view_label import ViewLabelWritter
from controller import ExpressionCreater
import accessify

class ViewWindow(Tk, singleton.Singleton):
    def init(self) -> None:
        super(singleton.Singleton).__init__()


    def start(self) -> None:
        self.title('Калькулятор')
        self.resizable(False, False)
        self.geometry('350x500') 

        self.create_label()
        self.create_buttons()
        self.mainloop()

    
    @accessify.protected
    def create_label(self) -> None:
            self.CalculatorLabel = ttk.Frame(self, padding=10, relief=SOLID)
            self.calculator_text = Label(self.CalculatorLabel, text="", font='Times 20')
            self.calculator_text.pack(anchor=E)
            self.CalculatorLabel.pack(anchor=S, fill=X, padx=5, pady=5)
            self.writter = ViewLabelWritter(self.calculator_text)
            self.creator = ExpressionCreater(self.writter)
    

    @accessify.protected
    def create_buttons(self) -> None:
            self.CalculatorButtons = ttk.Frame(self, padding=[5, 35])
            
            symbols = [['SIN', 'COS', 'TG', 'CTG', 'AC'],
                       ['log', '(', ')', '+', 'DEL'],
                       ['ln', '1', '2', '3', '-'],
                       ['!', '4', '5', '6', '*'],
                       ['mod', '7', '8', '9', '/'],
                       ['^', '.', '0', 'neg', '=']]
            
            self.buttons = []
            for row_number, row_context in enumerate(symbols):
                for column_number, button_context in enumerate(row_context):
                    if button_context == '':
                        continue

                    self.init_button(button_context, (row_number, column_number))

            self.CalculatorButtons.pack(anchor=CENTER, fill=X, padx=5, pady=5)  
        
    
    @accessify.protected
    def init_button(self, button_context: str, coordinate: Tuple[int, int]) -> None:
        if button_context == 'DEL':
            view_button = view_buttons.FunctionalButton(self.creator.delete_last)
        elif  button_context == "AC":
            view_button = view_buttons.FunctionalButton(self.creator.clear_all)
        elif button_context == '=':
            view_button = view_buttons.FunctionalButton(self.creator.get_answer)
        else:
            view_button = view_buttons.ViewButtton(self.creator.add_one, button_context)
        self.buttons.append(view_button)

        button = Button(self.CalculatorButtons, text=button_context, width=8, height=3, command=view_button.onClick)
        button.grid(row=coordinate[0], column=coordinate[1])
        
    
    


if __name__ == '__main__':
    app = ViewWindow()
    app.start()