class Test(object):
    x = 123

    printer = lambda self, n: self.printer_BUBBLES_DEF(n)

    def printer_BUBBLES_DEF(self, n):
        if (n==1):
            return (1)
        return (printer(n-1))

t = Test()
t.printer(3)
