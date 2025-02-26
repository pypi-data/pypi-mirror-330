def my_sum(a:int, b:int)->int:
    print("Deep dummy maths 🚀")
    return a+b


def my_diff(a: int, b: int) -> int:
    print("Deep dummy maths 🚀")
    return a-b


def my_pro(a: int, b: int) -> int:
    print("Deep dummy maths 🚀")
    return a*b


def my_div(a: int, b: int) -> float:
    print("Deep dummy maths 🚀")
    return a/b

def my_factorial(n: int) -> int:
    print("Deep dummy maths 🚀")
    if n == 0:
        return 1
    else:
        return n * my_factorial(n-1)