def bubble_sort(array:list, descending:bool=False) -> list:
    sorted = True
    for i in range(len(array)-1):
        for j in range(len(array)-1-i):
            if (array[j] > array[j+1]) ^ descending:
                array[j], array[j+1] = array[j+1], array[j]
                sorted = False
        if sorted:
            break
    return array
  
def insertion_sort(array:list, descending:bool=False) -> list:
    for i in range(1, len(array)):
        currentValue = array[i]
        position = i
        while position > 0 and ((array[position - 1] > currentValue) ^ descending):
            array[position] = array[position - 1]
            position = position - 1
        array[position] = currentValue
    return array
  
def quick_sort(array:list, descending:bool=False) -> list:
    if len(array) <= 1: return array
    pivot = array.pop(round(len(array) / 2))
    before_list = [x for x in array if (x < pivot) ^ descending]
    after_list = [x for x in array if (x >= pivot) ^ descending]
    sorted_list = quick_sort(before_list, descending) + [pivot] + quick_sort(after_list, descending)
    return sorted_list
  
def merge_sort(array: list, descending: bool = False) -> list:
    if len(array) <= 1: return array
    left = merge_sort(array[:len(array)//2], descending)
    right = merge_sort(array[len(array)//2:], descending)
    return merge(left, right, descending)

def merge(a, b, descending):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if (a[i] < b[j]) ^ descending:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result

def bogo_sort(array):
    from random import shuffle
    while not all(array[i]<=array[i+1] for i in range(len(array)-1)):
        shuffle(array)
    return array


