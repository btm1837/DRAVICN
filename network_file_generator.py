import pandas as pd
import numpy as np
import os
import sys
import itertools
from string import ascii_lowercase

def get_string():
    for size in itertools.count(1):
        for string in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(string)

# for s in iter_all_strings():
#     print(s)
#     if s == 'bb':
#         break

list_s = []
for s in itertools.islice(get_string(), 54):
    print(s)
    list_s.append(s)

def make_network(set_up_file)