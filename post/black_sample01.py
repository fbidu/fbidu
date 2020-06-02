"""
Módulo que oferece um fatorial iterativo
"""


def fatorial(n):
    result = 1

    for i in range(1, n + 1):
        result *= i
    return result


print(fatorial(3))
print(fatorial(2))
print(fatorial(10))
