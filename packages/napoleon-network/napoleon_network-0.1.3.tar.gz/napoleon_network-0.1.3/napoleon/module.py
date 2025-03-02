# Copyright (c) 2025 Matheo
# Licensed under the MIT License (see LICENSE.txt for details)


import math
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derive(x):
    return x * (1 - x)