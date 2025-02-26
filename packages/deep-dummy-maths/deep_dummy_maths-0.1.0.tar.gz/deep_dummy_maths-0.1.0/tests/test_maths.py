from deep_dummy_maths import my_sum, my_diff, my_pro, my_div, my_factorial

def test_my_sum():
    assert my_sum(1,2) == 3

def test_my_diff():
    assert my_diff(1,2) == -1

def test_my_pro():
    assert my_pro(1,2) == 2

def test_my_div():
    assert my_div(1,2) == 0.5

def test_my_factorial():
    assert my_factorial(5) == 120