from functools import cache
from typing import Mapping,AbstractSet
from syntax import is_variable,Formula,is_unary,is_binary
from itertools import product
import tabulate 


Model = Mapping[str,bool]
def is_model(model: Model) -> bool:
    """Checks if the given dictionray is a model over some set of variable names.

        Parameters :
            model: dictionray to check

        Returns:
            ``True`` if the given dict is a model over some set of variable names, ``False`` otherwise
     """
    for key in model:
        if not is_variable(key):
            return False
    return True

def variables(model: Model) -> AbstractSet[str]:
    """Finds all varaibles names over which the given model is defined

    Parameters:
        model: model to check

    Returns:
        A set of all variable  names over wich the given model is defined
    """
    assert is_model(model)
    return model.keys()

def evaluate(formula : Formula,model: Model) -> bool:
    """Calculutes the truth value of the given formula in the given model.

        Parameters:
            formula: formula to calculate the truth value of.
            model : model over  (possibly of superset) the variable names 
            of the given formula , to calculte the truth value in

            Returns:
                the truth value of the given formula in the model.
     """
    if is_unary(formula.root):
        if not is_variable(formula.first.__repr__()):
            first_vaule = evaluate(formula.first,model)
        else:
            first_vaule = model[formula.first.__repr__()]
        if first_vaule:
            return False
        else:
            return True

    elif is_binary(formula.root):
        if not is_variable(formula.first.__repr__()):
            first_vaule = evaluate(formula.first,model)
        else:
            first_vaule = model[formula.first.__repr__()]
        if not is_variable(formula.second.__repr__()):
            second_value = evaluate(formula.second,model)
        else:
            second_value = model[formula.second.__repr__()]
        if formula.root == "&":
            if first_vaule and second_value:
                return True
            else:
                return False
        elif formula.root == "->":
            if first_vaule and not second_value:
                return False
            else:
                return True
        elif formula.root == "|":
            if first_vaule or second_value:
                return True
            else:
                return False
    elif is_constant(formula.root):
        if formula.root == "T":
            return True
        else:
            return False
    else:
        return model[formula.root]


def all_models(variables: Sequence[srt]) -> Iterable[Model]:
    """Clculates all possible models over the given variables names

        Parameteres:
                variables: varaiable names overt wich to calculate the models.

        Returns:
            An iterable over all possible models over the given variables names. The
            order of the models is lexicographic according to the order of the given 
            varaible names,ehre False precedes True

        Examples:
            >>> list(all_models(['p', 'q']))
            [{'p': False, 'q': False}, {'p': False, 'q': True},
            {'p': True, 'q': False}, {'p': True, 'q': True}]
            >>> list(all_models(['q', 'p']))
            [{'q': False, 'p': False}, {'q': False, 'p': True},
            {'q': True, 'p': False},{'q':True,'p':True}]

    """
    for combo in product([False,True],repeat=len(variables)):
        yield dict(zip(variables,combo))

def truth_values(formula: Formula, models:Iterable[Model]) -> Iterable[bool]:
    """Calculates the truth value of the given formula in each of the given
        models.
        Parameters:
            formula: formula to calculate the truth value of.
        models: iterable over models to calculate the truth value in.
        Returns:
            An iterable over the respective truth values of the given formula in
        each of the given models, in the order of the given models.
        Examples:
            >>> list(truth_values(Formula.parse('˜(p&q76)'),
                ... all_models(['p', 'q76'])))
                    [True, True, True, False]

    """
    truth_value = []

    for truth in models:
        truth_value.append(evaluate(formula,truth))

    return truth_value


def main():
    meow = Formula.parse(input("syntax:"))
    total_list = []
    for model,result in zip(all_models(meow.variables()),truth_values(meow,all_models(meow.variables()))):
        total_list.append(list(model.values()) + [result])
        head = list(model.keys()) + [meow.__repr__()]
    print(tabulate.tabulate(total_list,headers=head,tablefmt="grid"))
if __name__ == "__main__":
    main()
