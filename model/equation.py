import lark
from model.util import create_residual
from model.util import EquationManagerError
from PyQt6.QtCore import QObject, pyqtSignal


class Equation:
    def __init__(self, eq_id: str, equation: str, variables: list[str], functions: list[str], tree: lark.Tree):
        self.id = eq_id
        self.input_form = equation
        self.residual_form = create_residual(equation)
        
        self.variables = variables  # Contains the variable names in the equation
        self.functions = functions  # Contains the function names in the equation
        self.tree = tree  # generated by the lark parser
        
        # set parameter status
        if len(self.variables) == 1:
            self.parameter_equation = True
        else:
            self.parameter_equation = False
        
    def __repr__(self):
        return self.input_form


class EquationManager(QObject):
    data_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.equations = {}

    def insert_equation(self, equation: Equation):
        if equation.id in self.equations:
            raise EquationManagerError(f'Failed to insert equation: Equation with id={equation.id} already exists')
        self.equations[equation.id] = equation
        
        # emit update signal
        self.data_changed.emit()

    def delete_equation(self, equation_id: id):
        if equation_id not in self.equations:
            raise EquationManagerError(f'Failed to delete equation: Equation with id={equation_id} does not exist')
        del self.equations[equation_id]

        # emit update signal
        self.data_changed.emit()
