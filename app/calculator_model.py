from typing import List
from abc import ABC, abstractmethod
import math
import enum

MAX_FACTORIAL_DEPTH = 20


class Operation(ABC):
    @abstractmethod
    def go(self, numbers: List[float | int]) -> float | int:
        pass

class OperationIndex(enum.IntEnum):
    sum_o = 0
    multiply_o = 1
    pow_o = 2
    factorial_o = 5
    ln_o = 4
    log_o = 3


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


class Singleton(object):
    def __new__(cls, *args, **kwargds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it

        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwargds)
        return it
    
    def init(self, *args, **kwargds):
        pass


OPERATIONS = [
    SumOperation(),
    MultiplyOperation(),
    PowOperation(),
    DecimalLogarithmOperation(),
    NaturalLogarithmOperation(),
    FactorialOperation()
]


class Calculator(Singleton):
    def init(self, operations : List[Operation]) -> None:
        super().__init__()
        self._operations = operations

    
    def go_operation(self, index: int, numbers: List[float | int]) -> float | int:
        return self._operations[index].go(numbers)


    