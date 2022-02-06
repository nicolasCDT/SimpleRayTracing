import numpy as np


##########################################
# TD3 : PASCAL
def pascal(x: int, y: int) -> int:
	if x == 1 or y == 1:
		return 1
	return pascal(x, y - 1) + pascal(x - 1, y)


for i in range(1, 10):
	for j in range(1, 10 - i):
		print(str(pascal(i, j)).ljust(4), end=" ")
	print("")


# TD3 : PASCAL FIN
##########################################


##########################################
# TD3 : COMPOSITION
def comp(n, k, pile):
	if k == 0:
		return pile + " "
	if k == 1:
		return pile + str(n)
	return [comp(n - x, k - 1, str(x) + pile) for x in range(0, n + 1)]


# TD3 : COMPOSITION FIN
##########################################


##########################################
# TD4 : STIRLING
def s(n, k):
	if n == k or k == 1:
		return 1
	return s(n - 1, k - 1) + k * s(n - 1, k)


# TD4 : STIRLING FIN
##########################################


##########################################
# TD4 : EXPONENTIATION RAPIDE
def expo(x: int, n: int) -> int:
	if not n:
		return 1
	current: int = expo(x, round(n / 2))
	if n % 2 == 0:
		return current * current
	return x * current * current


# TD4 : EXPONENTIATION RAPIDE FIN
##########################################


##########################################
# TD4 : EXPONENTIATION FIBONACCI
def f(n: int):
	if n == 0:
		return 0
	if n == 1:
		return 1
	return np.array([1, 0]).dot(np.array([[1, 1], [1, 0]]).__pow__(n - 1))


# TD4 : EXPONENTIATION FIBONACCI FIN
##########################################

print(f(30))
