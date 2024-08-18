from tkinter import *
DIGITALS = '0123456789'

class ViewLabelWritter():
    def __init__(self, label: Label) -> None:
        self.label = label

    def refresh(self, content: str):
        self.label.configure(text= content)


    
    