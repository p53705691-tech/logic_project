from syntax import Formula,is_variable,is_constant,is_unary

def test_parse():
    assert Formula.is_formula("a(") == False
    assert Formula.is_formula("(p&q22)") == True
    assert Formula.is_formula("(((a->z)&p)|z)") == True
    assert Formula.is_formula("p") == True



def test_is_variable():
    assert is_variable("p21") == True
    assert is_variable("q") == True
    assert is_variable("pp") == False
    assert is_variable("p_") == False


def test_is_constant():
    assert is_constant("T") == True
    assert is_constant("F") == True
    assert is_constant("A") == False
    assert is_constant("M") == False

def test_is_unary():
    assert is_unary("~") == True
    assert is_unary("p") == False
    assert is_unary("&") == False


