
def factorial(n):
    if(n == 1):
        return 1
    return n * factorial(n-1)

factorial2 n
    | n == 1 = 1
    | otherwise = n * factorial2 (n-1)

z = factorial2(7)
print(z)
