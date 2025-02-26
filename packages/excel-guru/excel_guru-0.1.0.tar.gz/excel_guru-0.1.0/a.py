import excel_guru


print(excel_guru.__all__)
print(excel_guru.__doc__)

if "sum_as_string" in excel_guru.__all__:
    res = excel_guru.sum_as_string(2, 6)
    print(res)
    print(excel_guru.sum_as_string)

if "diy" in excel_guru.__all__:
    res = excel_guru.diy("a", "b")
    print(res)
    res = excel_guru.diy("a", 1)


# def aaa(a: int, b: int) -> str:
#     print("aaa")
#     return a + b

# print(aaa)
# print(aaa.__annotations__)

# print("===============+>")
# print(open)
# print(open.__annotations__)
# print(__builtins__.__dict__)