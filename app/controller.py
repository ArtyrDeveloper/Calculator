from typing import List, Tuple
from app.calculator_model import OPERATIONS, Calculator, OperationIndex
from view_label import ViewLabelWritter
import accessify

DIGITALS = '0123456789'
OPERATORS = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    'mod': 2,
    '^': 3,
    'sin': 4,
    'neg': 4,
    'cos': 4,
    'tg': 4,
    'ctg': 4,
    'log': 4,
    'ln': 4,
    '!': 5
}
OPERATORS_KEYS = {
    '+': OperationIndex.sum_o,
    '-': OperationIndex.sum_o,
    '*': OperationIndex.multiply_o,
    '/': OperationIndex.multiply_o,
    'mod': OperationIndex.mod_o,
    'neg': OperationIndex.neg_o,
    '^': OperationIndex.pow_o,
    'sin': OperationIndex.sin_o,
    'cos': OperationIndex.cos_o,
    'tg': OperationIndex.tan_o,
    'ctg': OperationIndex.ctan_o,
    'log': OperationIndex.log_o,
    'ln': OperationIndex.ln_o,
    '!': OperationIndex.factorial_o
}


class ExpressionContainer:
    def __init__(self) -> None:
        self.components = []
    

    def delete_last_component(self) -> None:
        if len(self.components) <= 0:
            return
        del(self.components[-1])
    

    def delete_all(self) -> None:
        self.components = []


    def add_item(self, item: str) -> None:
        if len(self.components) > 0:
            if self.components[-1][0] in DIGITALS and (item in DIGITALS or item == '.'):
                self.components[-1] += item 
                return
        self.components.append(item.lower())  


class ExpressonSolver:
    def __init__(self) -> None:
        self.calculator = Calculator(OPERATIONS)


    def solve_expression(self, components: List[str]) -> float | int:
        self.calculation_history = dict()
        if self.is_valid(components) == False:
            raise ValueError
        
        self.calculate_operators_priority(components)

        for i in self.priority_dictionary.keys():
            self.calculate_operator(components, i)
        
        return self.find_answer_in_history()


    @accessify.protected       
    def is_number(self, number: str) -> bool:
        for i in number:
            if i not in DIGITALS and i != '.':
                 return False
        return True


    @accessify.protected
    def is_valid(self, components: List[str]) -> bool:
        opened, closed = 0, 0
        for i in components:
            if i == '(': opened += 1
            if i == ')': closed += 1
            
        return opened == closed  


    @accessify.protected
    def calculate_operators_priority(self, components: List[str]) ->  None:
        priority_dict = {}
        brackets_value = 0
        for i, value in enumerate(components):
            if value == '(': brackets_value += 1
            if value == ')': brackets_value -= 1

            if value in OPERATORS.keys():
                priority_dict[i] = OPERATORS[value] + 100 * brackets_value
        
        self.priority_dictionary = priority_dict


    @accessify.protected
    def calculate_operator(self, components: List[str], location: int) -> int | float:
        if location in self.calculation_history .keys():
            return self.calculation_history [location]
        nums = []
        
        operator = components[location]
        loc1, loc2 = -1, -1
        if OPERATORS[operator] < 4 or operator == '!': 
            left_result = self.handle_left_part(components, location)
            nums.append(float(left_result[1]))
            loc1 = left_result[0]

        if operator != '!':
            right_result = self.handle_rigth_part(components,  location)
            nums.append(float(right_result[1]))  
            loc2 = right_result[0]             
        
        if operator == '-':
            nums[1] *= -1

        if operator == '/':
            nums[1] = 1 / nums[1]

        self.calculation_history [location] = self.calculator.go_operation(OPERATORS_KEYS[operator], nums)

        if loc1 != -1:
            self.calculation_history [loc1] =  self.calculation_history [location]

        if loc2 != -1:
            self.calculation_history [loc2] =  self.calculation_history [location]

        return self.calculation_history [location]


    @accessify.protected
    def handle_left_part(self, components: List[str], location: int) -> Tuple[int, str]:
        cache_component = ''
        loc1 = 0
        priority = self.priority_dictionary[location]
        if self.is_number(components[location - 1]):
            cache_component = components[location - 1]
        elif components[location - 1] == ')':
            cache_component = self.solve_bracket_pars_from_left(components, location - 1)
        if location - 2 >= 0:
            if components[location - 2] in OPERATORS.keys():
                if self.priority_dictionary[location - 2] >= priority:
                    loc1 = location - 2
                    cache_component = self.calculate_operator(components, location - 2)
        
        return (loc1, cache_component)
    

    @accessify.protected
    def handle_rigth_part(self, components: List[str], location: int) -> Tuple[int, str]:
        cache_component = ''
        loc2 = 0
        priority = self.priority_dictionary[location]
        if self.is_number(components[location + 1]):
            cache_component = components[location + 1]
        elif components[location + 1] == '(':
                cache_component = self.solve_brackets_part_from_rigth(components, location + 1)
        
        if location + 2 < len(components):
            if components[location + 2] in OPERATORS.keys():
                if self.priority_dictionary[location + 2] > priority:
                    loc2 = location + 2
                    cache_component = self.calculate_operator(components, location + 2)

        return (loc2, cache_component)
    
    
    @accessify.protected
    def solve_bracket_pars_from_left(self, components: List[str], location: int) -> int:
        i = location - 1
        bracket = 0
        prio, loc = 10000, 10000
        while i >= 0:
            if components[i] in OPERATORS.keys():
                if self.priority_dictionary[i] <= prio:
                    if loc != min(loc, i):
                        prio =  self.priority_dictionary[i]
                        loc = i
                                
            if components[i] == '(':
                if bracket == 0:
                    break
                else:
                    bracket -= 1
        
            if components[i] == ')':
                bracket += 1
            
            i -= 1
        return loc
    
    
    @accessify.protected
    def solve_brackets_part_from_rigth(self, components: List[str], location: int) -> int:
        i = location + 1
        bracket = 0
        prio, loc = 10000, -10000
        while i < len(components):
            if components[i] in OPERATORS.keys():
                if self.priority_dictionary[i] <= prio:
                    if loc != max(loc, i):
                        prio =  self.priority_dictionary[i]
                        loc = i            
            if components[i] == ')':
                if bracket == 0:
                    break
                else:
                    bracket -= 1
            if components[i] == '(':
                bracket += 1
            i += 1
        
        return loc


    @accessify.protected
    def find_answer_in_history(self) -> int | float:
            min_prior, min_key = 100000, 0
            for key, value in self.priority_dictionary.items():
                print(key, value)
                if min_prior != min(min_prior, value):
                    min_prior = value
                    min_key = key
                
            
            return self.calculation_history[min_key]


class ExpressionCreater:
    def __init__(self, view_writter: ViewLabelWritter) -> None:
        self.view_writter = view_writter
        self.container = ExpressionContainer()


    def add_one(self, item: str) -> None:
        self.container.add_item(item)                          
        self.view_writter.refresh(' '.join(self.container.components))


    def clear_all(self) -> None:
        self.container.delete_all
        self.view_writter.refresh(' '.join(self.container.components))
    

    def delete_last(self) -> None:
        self.container.delete_last_component()
        self.view_writter.refresh(' '.join(self.container.components))
    

    def get_answer(self) -> float|int:
        solver = ExpressonSolver()
        self.view_writter.refresh(str(solver.solve_expression(self.container.components)))
        self.container.delete_all()
