import numpy as np
from typing import Any
from array import ArrayType


def appendArray(array: ArrayType[Any], value: Any) -> ArrayType[Any]:
    arrayAux = np.array([None for _ in range(len(array) + 1)])
    for i in range(len(array)):
        arrayAux[i] = array[i]
    arrayAux[len(array)] = value
    return arrayAux


def containsArray(array: ArrayType[Any], value: Any) -> bool:
    for i in range(len(array)):
        if array[i] == value:
            return True
    return False


def splitInPairs(text: str) -> ArrayType[str]:
    pairs = np.array([])
    operatorsCount = 0
    for char in text:
        if char == "+":
            operatorsCount += 1
        elif char == "-":
            operatorsCount += 1
        elif char == "*":
            operatorsCount += 1
        elif char == "/":
            operatorsCount += 1

    while len(pairs) < operatorsCount:
        pairs = appendArray(pairs, f"{text[0]}{text[1]}{text[2]}")
        text = text[2:]
    return pairs
