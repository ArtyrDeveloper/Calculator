from tkinter import *
from tkinter import ttk
import sys
import view_buttons
sys.path.append('D:\\Education\\Python\\MyCalculator\\')
from General import singleton
from view_label import ViewLabelWritter, ViewLabelHandler


class ViewWindow(Tk, singleton.Singleton):
    def init(self) -> None:
        super(singleton.Singleton).__init__()
        
    
    def start(self) -> None:
        def create_label() -> None:
            self.CalculatorLabel = ttk.Frame(self, padding=10, relief=SOLID)
            self.calculator_text = Label(self.CalculatorLabel, text="", width=25, height=3,font='Times 20')
            self.calculator_text.pack(anchor=CENTER)
            self.CalculatorLabel.pack(anchor=CENTER, fill=X, padx=5, pady=5)
            self.writter = ViewLabelWritter(self.calculator_text)
            self.handler = ViewLabelHandler(self.writter)

        
        def create_buttons() -> None:
            self.CalculatorButtons = ttk.Frame(self, padding=[5, 5])
            
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

                    if button_context == 'DEL':
                        view_button = view_buttons.FunctionalButton(self.writter.delete_last)
                    elif  button_context == "AC":
                        view_button = view_buttons.FunctionalButton(self.writter.clear_all)
                    elif button_context == '=':
                        view_button = view_buttons.FunctionalButton(self.handler.solve)
                    else:
                        view_button = view_buttons.ViewButtton(self.writter, button_context)
                    self.buttons.append(view_button)

                    button = Button(self.CalculatorButtons, text=button_context, width=8, height=3, command=view_button.onClick)
                    button.grid(row=row_number, column=column_number)



            self.CalculatorButtons.pack(anchor=CENTER, fill=X, padx=5, pady=5)       

        def set_general_settings() -> None:
            self.title('Калькулятор')
            self.resizable(False, False)
            self.geometry('350x500')
        
        set_general_settings()
        create_label()
        create_buttons()
        self.mainloop()


if __name__ == '__main__':
    c_v = ViewWindow()
    c_v.start()