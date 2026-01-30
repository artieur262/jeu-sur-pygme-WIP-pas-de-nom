import sys

a = range(1000)

list_list = [[j, j] for j in a]
list_tuple = [(j, j) for j in a]
set_tuple = {(j, j) for j in a}
dict_ = {i: i for i in a}
print("list_list", sys.getsizeof(list_list))
print("list_tuple", sys.getsizeof(list_tuple))
print("set_tuple", sys.getsizeof(set_tuple))
print("dict_tuple", sys.getsizeof(dict_))
