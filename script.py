#калькулятор
import numpy as np
from colorama import init
from colorama import Fore, Back, Style
init()

print(Fore.YELLOW)

expr = input("Введите математическое выражение:")
result = np.array(eval(expr))

print(Fore.RED)

print(Fore.GREEN)
print(f"Результат: {result}")
print(Fore.BLUE)
input("Нажмите интер чтобы закрыть...")

