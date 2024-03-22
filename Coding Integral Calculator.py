from dataclasses import dataclass
from drafter import *
import math

@dataclass
class State:
    integrand: str
    variable: str
    def_or_indef: bool
    lower_limit: str
    upper_limit: str
    technique: str
    result: str
    
@route
def index(state: State) -> Page:
    return Page(state, [
        "Integral Calculator",
        "What is your integrand?",
        TextBox("Integrand", state.integrand),
        "With what variable are taking the integral with respect to?",
        TextBox("Variable", state.variable),
        "Are you taking a definite integral? Check the box and provide limits if so.",
        CheckBox("DefiniteBox", state.def_or_indef),
        "Lower Limit",
        TextBox("LowerLimit", state.lower_limit),
        "Upper Limit",
        TextBox("UpperLimit", state.upper_limit),
        "Please select a integration technique to use.",
        SelectBox("Technique", ["Power Function", "Substitution", "By Parts", "Powers of Trig Functions",
                                "Trig Substitution", "Partial Fractions", "Improper Integrals",
                                "Approximation"], state.technique),
        Button("Integrate", start_integration)
        ])

@route
def start_integration(state: State, Integrand: str, Variable: str, DefiniteBox: bool, LowerLimit: str, UpperLimit: str, Technique: str) -> Page:
    state.integrand = Integrand
    state.variable = Variable
    state.def_or_indef = DefiniteBox
    state.lower_limit = LowerLimit
    state.upper_limit = UpperLimit
    state.technique = Technique
    if state.integrand:
        if state.technique == "Power Function":
            state.result = power_funct_integration(state)
        elif state.technique == "Substitution":
            state.result = substi_integration(state)
        elif state.technique == "By Parts":
            state.result = parts_integration(state)
        elif state.technique == "Powers of Trig Functions":
            state.result = power_of_trig_integration(state)
        elif state.technique == "Trig Substitution":
            state.result = trig_substi_integration(state)
        elif state.technique == "Partial Fractions":
            state.result = partial_frac_integration(state)
        elif state.technique == "Improper Integral":
            state.result = improper_integration(state)
    else:
        return error_page(state, "Missing Integrand")
    return Page(state, [
        "Type of Integration: " + state.technique,
        "Integrand: " + state.integrand,
        "Result: " + state.result
        ])

@route
def error_page(state: State, msg: str) -> Page:
    return Page(state, [
        "Error! Could Not Compute",
        msg,
        Button("Return To Calculator", index)
        ])

def power_funct_integration(state: State) -> str:
        '''
        i_end_para_position_list = []
        adj_var_ex_position_list = []
        new_exponent_list = []
        for var_position in var_position_list:
            for ex_position in ex_position_list:
                if var_position == (ex_position - 1):
                    adj_var_ex_position.append(ex_position)
        for adj_position in adj_var_ex_position_list:
            i = 0
            for para_position in end_para_position_list:
                if (para_position > adj_position) and (i == 0):
                    i_end_para_position_list.append(para_position)
                    i = 1
        num = 0
        for adj_position in adj_var_ex_position_list:
            new_exponent = state.integrand[adj_position:i_end_para_position_list[num]]
            new_exponent_list.append(new_exponent)
            num += 1
        #first_adj_pos = adj_var_ex_position_list[0]
        #first_new_ex = new_exponent_list[0]
        result = state.integrand[0:1] + "^" + str(int(2) + 1)
        #except:
            #return "error"
        #if state.def_or_indef: 
        #else:
            return result
        '''
    #try:
        integrand_list = []
        var_position_list = []
        ex_position_list = []
        end_para_position_list = []
        for character in state.integrand:
            integrand_list.append(character)
        position = 0
        for character in integrand_list:
            if character == state.variable:
                var_position_list.append(position)
            position += 1
        position = 0
        for character in integrand_list:
            if character == "^":
                ex_position_list.append(position)
            position += 1
        position = 0
        for character in integrand_list:
            if character == ")":
                end_para_position_list.append(position)
            position += 1
        ex_position_list_count = 0
        for number in ex_position_list:
            ex_position_list_count += 1
        end_para_position_list_count = 0
        for number in end_para_position_list:
            end_para_position_list_count += 1
        count = 0
        result = ""
        for number in var_position_list:
            old_ex = ""
            if ((ex_position_list_count-1) == count) and ((end_para_position_list_count-1) == count):
                for number in integrand_list[(ex_position_list[count]+2):end_para_position_list[count]]:
                    old_ex = old_ex + str(number)
            if not old_ex:
                old_ex = "1"
            new_ex = int(old_ex) + 1
            if count == 0:
                result = result + state.integrand[0:(var_position_list[count])] + "(1/" + str(new_ex) + ")" + state.variable + "^(" + str(new_ex) + ")"
            else:
                result = result + state.integrand[((var_position_list[count])-1):(var_position_list[count])] + "(1/" + str(new_ex) + ")" + state.variable + "^(" + str(new_ex) + ")"
            count += 1
        if state.def_or_indef:
            beginning = float(state.integrand[0:(var_position_list[count])])
            fraction = 1/float(new_ex)
            upper_limit = float(state.upper_limit)**new_ex
            lower_limit = float(state.lower_limit)**new_ex
            return str((beginning*fraction)*(upper_limit-lower_limit))
        else:
            return result + " + C"
    #except:
        return "ERROR"

#Test Case 1: x -> (1/2)x^2 + C
#Test Case 2: 3x^2 -> x^3 + C

start_server(State("","",False,"","","Power Function",""))