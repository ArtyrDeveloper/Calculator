from tkinter import *

class ViewLabelWritter():
    def __init__(self, label: Label) -> None:
        self.label = label

    def refresh(self, content: str) -> None:
        self.label.configure(text= content)   
    