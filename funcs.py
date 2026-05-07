def upper_func(input, do_upper=True):
    if do_upper:
        return input.upper()
    return input

def repeat_func(input, n=2):
    return input * n

def addstr_func(input, add_str):
    return input + add_str

if __name__ == "__main__":
    a = f('alphabet')
    b = ff(a)
    c = fff(b)
    print(a)
    print(b)
    print(c)
