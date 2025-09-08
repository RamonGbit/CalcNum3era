import numpy as np
from typing import Any

def appendArray(array: np.ndarray, value: Any) -> np.ndarray:
    arrayAux = np.array([None for _ in range(len(array) + 1)])
    for i in range(len(array)):
        arrayAux[i] = array[i]
    arrayAux[len(array)] = value
    return arrayAux


def containsArray(array: np.ndarray, value: Any) -> bool:
    for i in range(len(array)):
        if array[i] == value:
            return True
    return False


def splitInPairs(text: str) -> np.ndarray:
    pairs = np.array([])
    operatorsCount = 0
    for char in text:
        if char in "+-*/":  
            operatorsCount += 1

    i = 0
    while i < len(text) - 1:
        if text[i+1] in "+-*/":
            pairs = np.append(pairs, text[i:i+3])
            i += 3
        else:
            i += 1
    return pairs
