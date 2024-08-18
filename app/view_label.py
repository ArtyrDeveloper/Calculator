from tkinter import *
from typing import Dict, List
from calculator_model import Calculator, OperationIndex, OPERATIONS

DIGITALS = '0123456789'
OPERATORS = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    'mod': 2,
    '^': 3,
    'sin': 4,
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
    '^': OperationIndex.pow_o,
    'sin': OperationIndex.sin_o,
    'cos': OperationIndex.cos_o,
    'tg': OperationIndex.tan_o,
    'ctg': OperationIndex.ctan_o,
    'log': OperationIndex.log_o,
    'ln': OperationIndex.ln_o,
    '!': OperationIndex.factorial_o
}

class ViewLabelWritter():
    def __init__(self, label: Label) -> None:
        self.label = label
        self.components = []

    def refresh(self):
        self.label.configure(text=' '.join(self.components))

    def write_text(self, writteble_text: str) -> None:
        if len(self.components) > 0:
            if self.components[-1] in DIGITALS and writteble_text in DIGITALS:
                self.components[-1] += writteble_text   
                self.refresh()
                return
        self.components.append(writteble_text)                           
        self.refresh()

    def clear_all(self):
        self.components = []
        self.refresh()
    
    def delete_last(self):
        if len(self.components) <= 0:
            return
        del(self.components[-1])
        self.refresh()
    

class ViewLabelHandler():
    def __init__(self, writter: ViewLabelWritter):
        self.calculator = Calculator(OPERATIONS)
        self.writter = writter
    

    def solve(self):
        priority_dictionaty = {}
        calculation_dictionary ={}

        def is_number(number: str) -> bool:
            for i in number:
                if i not in DIGITALS:
                    return False
            return True

        def bracket_conditional_checker(componets: List[str]) -> bool:
            opened, closed = 0, 0
            for i in componets:
                if i == '(': opened += 1
                if i == ')': closed += 1
            
            return opened == closed
        
        
        def get_priority_dictionary(components: List[str]) -> Dict[int, int]:
            priority_dict = {}
            brackets_value = 0
            for i, value in enumerate(components):
                if value == '(': brackets_value += 1
                if value == ')': brackets_value -= 1

                if value in OPERATORS.keys():
                    priority_dict[i] = OPERATORS[value] + 100 * brackets_value
            
            return priority_dict

        def get_result_from_bracket_pars(location: int, components: List[str]) -> int | float:
            def open_case():
                i = location + 1
                bracket = 0
                prio, loc = 10000, 10000
                while True:
                    if components[i] in OPERATORS.keys():
                        if priority_dictionaty[i] <= prio:
                            if loc != min(loc, i):
                                prio =  priority_dictionaty[i]
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


            def close_case():
                i = location - 1
                bracket = 0
                prio, loc = 10000, 10000
                while True:
                    if components[i] in OPERATORS.keys():
                        if priority_dictionaty[i] <= prio:
                            if loc != min(loc, i):
                                prio =  priority_dictionaty[i]
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

            need_location = open_case() if components[location] == '(' else close_case()
            
            if need_location in calculation_dictionary:
                return calculation_dictionary[need_location]
            else:
                return get_result_for_operator(components, need_location)

        def get_result_for_operator(components: List[str], location: int) -> int | float:
            if location in calculation_dictionary.keys():
                return calculation_dictionary[location]

            nums = []
            
            operator = components[location]
            priority = priority_dictionaty[location]
            cache_component = ''
            if OPERATORS[operator] < 4: 
                i = location - 1
                while i >= 0:
                    if i == 0 and is_number(components[i]):
                        nums.append(float(components[i]))
                        break
                    else:
                        if is_number(components[i]) and cache_component == '':
                            cache_component = components[i]
                        elif components[i] == '(':
                            nums.append(float(cache_component))
                            break
                        elif components[i] == ')':
                            nums.append(get_result_from_bracket_pars(i, components))
                            break
                        else:
                            if priority_dictionaty[i] < priority:
                                nums.append(float(cache_component))
                                break
                            elif priority_dictionaty[i] >= priority:
                                nums.append(calculation_dictionary[i])
                                break
                    i -= 1
            
            i = location + 1
            cache_component = ''
            while i < len(components):
                if i == len(components) - 1 and is_number(components[i]):
                        nums.append(float(components[i]))
                        break
                else:
                    if is_number(components[i]) and cache_component == '':
                        cache_component = components[i]
                    elif components[i] == ')':
                            nums.append(float(cache_component))
                            break
                    elif components[i] == '(':
                            nums.append(get_result_from_bracket_pars(i, components))
                            break
                    else:
                        if priority_dictionaty[i] <= priority:
                                nums.append(float(cache_component))
                                break
                        elif priority_dictionaty[i] > priority:
                                nums.append(get_result_for_operator(components, i))
                                break
                i += 1
            
            
            calculation_dictionary[location] = self.calculator.go_operation(OPERATORS_KEYS[operator], nums)
            return calculation_dictionary[location]

                
            
                        

                



        components = self.writter.components
        print(components)
        priority_dictionaty = get_priority_dictionary(components)
        
        for i in priority_dictionaty.keys():
            get_result_for_operator(components, i)
        print(priority_dictionaty)
        print(calculation_dictionary)



if __name__ == '__main__':
    writter = ViewLabelWritter(Label())
    writter.components = ['3', '+', '2', '+', '7', '*', '8', '+', '9', '*', '(', '3', '+', '7', '+', '4', '*', '(', '3', '+', '2', ')', ')']
    handler = ViewLabelHandler(writter)
    handler.solve()


    
    