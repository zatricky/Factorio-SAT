from typing import *
from util import *

# AMO - At Most One

def quadratic_amo(variables: List[VariableType], _: Optional[AllocatorType]=None) -> ClauseList:
    clauses = []
    for i, var_a in enumerate(variables):
        for var_b in variables[:i]:
            clauses.append([-var_a, -var_b])
    return clauses

def logarithmic_amo(variables: List[VariableType], allocator: AllocatorType) -> ClauseList:
    location_variables = [allocator() for _ in range(bin_length(len(variables)))]
    clauses = [list(variables)]
    for i, var in enumerate(variables):
        clauses += implies([var], set_number(i, location_variables))
    return clauses

def heule_amo(variables: List[VariableType], allocator: AllocatorType, recursive_cutoff: int=3) -> ClauseList:
    assert recursive_cutoff >= 3
    if len(variables) <= recursive_cutoff:
        return quadratic_amo(variables)
    else:
        auxilary = allocator()
        middle = len(variables) // 2
        return heule_amo(variables[:middle] + [ auxilary], allocator, recursive_cutoff) + \
               heule_amo(variables[middle:] + [-auxilary], allocator, recursive_cutoff) 


def quadratic_one(variables: List[VariableType], _: Optional[AllocatorType]=None) -> ClauseList:
    return quadratic_amo(variables) + [list(variables)]

def logarithmic_one(variables: List[VariableType], allocator: AllocatorType) -> ClauseList:
    return logarithmic_amo(variables, allocator) + [list(variables)]

def heule_one(variables: List[VariableType], allocator: AllocatorType, recursive_cutoff: int=3) -> ClauseList:
    return heule_amo(variables, allocator, recursive_cutoff) + [list(variables)]


def naive_less_than(variables: List[VariableType], n: int, _: Optional[AllocatorType]=None) -> ClauseList:
    clauses = []
    for combination in combinations(variables, n):
        clauses.append(invert_components(combination))
    return clauses

def adder_less_than(variables: List[VariableType], n: int, allocator: AllocatorType) -> ClauseList:
    bits = [allocator() for _ in range(bin_length(len(variables) + 1))]
    
    clauses = get_popcount(variables, bits, allocator)
    for i in range(n, 2**len(bits)):
        clauses.append(set_not_number(i, bits))
    return clauses


def adder_greater_equal(variables: List[VariableType], n: int, allocator: AllocatorType) -> ClauseList:
    bits = [allocator() for _ in range(bin_length(len(variables) + 1))]
    
    clauses = get_popcount(variables, bits, allocator)
    for i in range(n):
        clauses.append(set_not_number(i, bits))
    return clauses

def naive_greater_equal(variables: List[VariableType], n: int, _: Optional[AllocatorType]=None) -> ClauseList:
    return naive_less_than(invert_components(variables), len(variables) - n + 1)