from typing import Callable
from view_label import ViewLabelWritter
from abc import ABC, abstractmethod

class CalculatorButton(ABC):
    @abstractmethod
    def onClick(self):
        pass

class ViewButtton(CalculatorButton):
    def __init__(self, function: Callable, text: str) -> None:
        self.function = function
        self.text = text
    
    def onClick(self):
        self.function(self.text)


class FunctionalButton(CalculatorButton):
    def __init__(self, function: Callable) -> None:
        self.funtion = function
    
    def onClick(self):
        self.funtion()

