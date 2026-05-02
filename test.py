def b(b,c):
    print(b)
    print(c)

def a(**kwargs):
    kwargs["c"] = kwargs["a"]
    del kwargs["a"]
    return b(**kwargs)

a(a = 1,b = 2)