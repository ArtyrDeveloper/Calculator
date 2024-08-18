from typing import List
from abc import ABC, abstractmethod
from errors import ViewInputError
import math
import enum

import sys
sys.path.append('D:\\Education\\Python\\MyCalculator\\')
from General import singleton

MAX_FACTORIAL_DEPTH = 20


class Operation(ABC):
    @abstractmethod
    def go(self, numbers: List[float | int]) -> float | int:
        pass


class SumOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        return sum(numbers)


class MultiplyOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        result = 1
        for i in numbers:
            result *= i
        
        return result

class PowOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        if len(numbers) > 2:
            raise ValueError

        return numbers[0] ** numbers[1]

class FactorialOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:      
        if len(numbers) > 1:
            raise ValueError
        
        number = numbers[0]
        
        if number < 0:
            raise ArithmeticError
        
        if number > MAX_FACTORIAL_DEPTH:
            raise ArithmeticError
        
        result = 1
        for i in range(1, number + 1):
            result *= i
        
        return result

class NaturalLogarithmOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        if len(numbers) > 1:
            raise ValueError
        
        if numbers[0] <= 0:
            raise ArithmeticError
        
        return math.log1p(numbers[0])


class DecimalLogarithmOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        if len(numbers) > 1:
            raise ValueError
        
        if numbers[0] <= 0:
            raise ArithmeticError
        
        return math.log10(numbers[0])
    

class NegativeOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        if len(numbers) > 1:
            raise ViewInputError
        
        return numbers[0] * -1


class SinOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        if len(numbers) > 1:
            raise ViewInputError

        return round(math.sin(numbers[0]), 5)


class CosOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        if len(numbers) > 1:
            raise ViewInputError

        return round(math.cos(numbers[0]), 5)
    

class TanOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        if len(numbers) > 1:
            raise ViewInputError

        return round(math.tan(numbers[0]), 5)
    

class CtanOperation(Operation):
    def go(self, numbers: List[float | int]) -> float | int:
        if len(numbers) > 1:
            raise ViewInputError

        return round(1 / math.tan(numbers[0]), 5)


class OperationIndex(enum.IntEnum):
    sum_o = 0
    multiply_o = 1
    pow_o = 2
    factorial_o = 5
    ln_o = 4
    log_o = 3
    neg_o = 6
    sin_o = 7
    cos_o = 8
    tan_o = 9
    ctan_o = 10
    mod_o = 11

OPERATIONS = [
    SumOperation(),
    MultiplyOperation(),
    PowOperation(),
    DecimalLogarithmOperation(),
    NaturalLogarithmOperation(),
    FactorialOperation(),
    NegativeOperation(),
    SinOperation(),
    CosOperation(),
    TanOperation(),
    CtanOperation()
]



class Calculator(singleton.Singleton):
    def init(self, operations : List[Operation]) -> None:
        super().__init__()
        self._operations = operations

    
    def go_operation(self, index: int, numbers: List[float | int]) -> float | int:
        return self._operations[index].go(numbers)