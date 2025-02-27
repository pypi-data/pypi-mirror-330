

x = 0
def counter(message: str):
    global  x
    x += 1
    print(x, message)


while x < 5:
    print('Setting lambda')
    f = lambda : counter('hello')
    print('Calling lambda')
    f()

