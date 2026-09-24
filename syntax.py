from dataclasses import dataclass
from functools import cache
from typing import Optional



@dataclass(frozen=True,repr=False,init=False)
class Formula:
    """AN immutable propositional formula in tree representation, composed from varaible name, 
    and operator applied to them. 
    
    Attributes:
        root: the constant , variable name , or operator at the root of the formula tree
        first: the first operand (المعامل الاول) , if the root is a unary or binary operator
        second: the second operand of the root , if the root is a binary operator
    """
    root: str
    first: Optional[Formula]
    second: Optional[Formula]

    def __init__(self, root: str,first: Optional[Formula] = None, second: Optional[Formula] = None):
        """ Initialize a `Formula` from its root and root operands.

        Parameters:
            root: the root for the formula tree
            first: the first operand (المعامل الاول) , if the root is a unary or binary operator
            second: the second operand of the root , if the root is a binary operator
         """
        if is_variable(root) or is_constant(root):
            assert first is None and second is None
            object.__setattr__(self,'root',root)
            object.__setattr__(self,"first",None)
            object.__setattr__(self,"second",None)
        elif is_unary(root):
            assert first is not None and second is None
            object.__setattr__(self,'root',root) 
            object.__setattr__(self,'first',first)
            object.__setattr__(self,"second",None)
        else:
            assert is_binary(root)
            assert first is not None and second is not None
            object.__setattr__(self,'root',root) 
            object.__setattr__(self,'first',first)
            object.__setattr__(self,'second',second)
    
    def __repr__(self) -> str:
        """Compute the string representation of the current formula.

           Returns:
                the standrad string representation of the current formula
         """
        if is_unary(self.root):
                return self.root + '(' +  self.first.__repr__() + ')'
        elif is_binary(self.root):
            if self.first.checker():
                return '(' + self.first.__repr__() + ')' + self.root + self.second.__repr__() 
            elif self.second.checker():
                return self.first.__repr__() + self.root + '(' + self.second.__repr__() + ')'
            else:
                return self.first.__repr__() + self.root + self.second.__repr__()

        else:
            return self.root      

    def variables(self):
        """ find all variable names in the current formula
            Returns:
                A set of all varible names used in the current formula
        """
    

        if is_variable(self.root):
            return {self.root}
        else:
            if is_unary(self.root):
                return self.first.variables()
            elif is_binary(self.root):
                return self.first.variables().union(self.second.variables())
    
    
    def operators(self) -> Set[str]:
        """Find all opertaors in our formula
            Returns:
                return all operators which used in the formula including 'T' and 'F'
        """
        if is_unary(self.root):
            return {self.root}.union(self.first.operators())
        elif is_binary(self.root):
            return {self.root}.union(self.first.operators(),self.second.operators())
        elif is_constant(self.root):
            return {self.root}
        else:
            return set()
    @staticmethod
    def _parse_prefix(string: str) -> Tuple[Optional[Formula],str]:
        """ Parse a prefix of the given string into formula.
        Parameters:
            string: strng to parse

            Returns:
                A pair of the pared formula and the unparsed suffix of the string.
                If the given string has as a prefix a variable name (e.g.,'x12') or
                a unary operator followed by a variable name , then the parsed prefix
                will include that entire variable name (and not just a part of it , such as 'x1')
                If no prefix of the given string is a valid standrad string representation
                of a formula returned pair should be of ``None`` and an error message, where the error message
                is a string with some human-readable content 
        """
        if string == "":
            return None,"Invalid syntax"
        
        if is_variable(string[0]):
            i = 1
            while i < len(string)  and string[i].isdigit():
                i +=1
            return Formula(string[:i]) , string[i:] 
        elif is_unary(string[0]):
            sub , rest = Formula._parse_prefix(string[1:])
            if sub is not None:
                return Formula(string[0],sub),rest
            else:
                return None,"Invalid syntax"
        elif is_constant(string[0]):
            return Formula(string[0]) , string[1:]
        
        elif string[0] == '(':
            try:
                left , rest = Formula._parse_prefix(string[1:])
                if rest[0] in ["&","|"]:
                    right,rest2 = Formula._parse_prefix(rest[1:])
                    if rest2.startswith(")"):
                        return Formula(rest[0],left,right),rest2[1:]
                    else:
                        return None,"Invalid syntax"
                elif rest[0] == '-' and rest[1] == '>':
                    right,rest2 = Formula._parse_prefix(rest[2:])
                    if rest2.startswith(")"):
                        return Formula(rest[0]+rest[1],left,right),rest2[1:]
                    else:
                        return None,"Invalid syntax"
                else:
                    return None,"Invalid syntax"
            except IndexError:
                return None,"Invalid syntax"
        else:
            return None,"Invalid syntax"

    def checker(self) -> bool:
        """ this function show for you if this resoultion formula or not
                
            Returns:
                ``True`` if it is resoultion formula , and ``False`` if not
        """
        return is_binary(self.root) or is_unary(self.root)

    @staticmethod
    def is_formula(string: str) -> bool:
        """Check if the given string is a valid representation of a formula.
            
            Parameters:
                string : string to check

            Returns:
                ``True`` if the given string is a valid standrad string representation 
                of a formula. ``False`` otherwise
        """
        left,right = Formula._parse_prefix(string)
        if not right and left is not None:
            return True
        return False

    @staticmethod
    def parse(string: str) -> Formula:
        """Parse the given valid string representation into a formula
        
            Parameters: String to parse

            Returns:
                A formula whose standrad standrad string representation is the given string
        """
        assert Formula.is_formula(string)
        left , right = Formula._parse_prefix(string)
        return left

@cache
def is_variable(string: str) -> bool:
    """
    Checks if the given string is a variable name.
    Parameters:
        string: string to check.
    Returns:
        ``True`` if the given string is a variable name, ``False`` otherwise.
    """
    return  'a' <= string[0] <= 'z' and \
        (len(string) == 1 or string[1:].isdigit())


@cache
def is_constant(string: str) -> bool:
    """
    checks if the given string is a constant.
    parameter:
        string: string to check

    Returns:
        ``True`` if the given string is constant , ``False`` otherwise
    """
    return string == 'T' or string == 'F'

@cache
def is_unary(string: str) -> bool:
    """Checks if the given string is an unary operator

    Parameters:
        string: string to check

    Returns:
        ``True`` if the given string is an unary operator, ``False`` otherwise
    """

    return string == '~'

@cache
def is_binary(string: str) -> bool:
    """Checks if the given string is a binary operator.

    Parameters:
        string: string to check
    Returns:
        ``True`` if the given string is a binary operator , ``False`` otherwise
    """
    return string == '&' or string == '|' or string == '->'


if __name__ == "__main__":
    main()
