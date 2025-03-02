def binary_search(item, array, check_repeats=False, not_found=None):
    """
    Performs a binary search to find the index of an item in a sorted array.

    Args:
        item: The element to search for in the array.
        array (list): A sorted list of elements. The array can be sorted in either
                      ascending or descending order.
        check_repeats (bool): If True, the function will return the range of indices 
                               where the item appears in the array (if it occurs more 
                               than once). Default is False, in which case only the first 
                               occurrence of the item is returned.
        not_found: The value to return if the item is not found in the array. 
                   Default is None.

    Raises:
        IndexError: If the array is empty.

    Returns:
        int, tuple, or None: 
            - If `check_repeats` is False, the index of the item is returned.
            - If `check_repeats` is True and the item is found multiple times, 
              a tuple of the first and last index of the item is returned.
            - If the item is not found, `not_found` is returned (default is None).
            
    Example:
        >>> binary_search(5, [1, 3, 5, 7, 9])
        2

        >>> binary_search(5, [9, 7, 5, 3, 1], check_repeats=True)
        2

        >>> binary_search(5, [1, 3, 5, 5, 5, 7, 9], check_repeats=True)
        (2, 4)

        >>> binary_search(10, [1, 3, 5, 7, 9])
        None
    """

  if not array:raise IndexError("Array must not be empty.")
  descending = array[0] > array[-1]
  first = 0
  last = len(array)-1
  while first <= last:
    current = (first+last)//2
    if item == array[current]: 
      if not check_repeats: return current
      else:
        low = high = current
        while array[low] == array[current]: low -= 1
        while array[high] == array[current]: high += 1
        return current if high == low else (low+1, high-1)
        
    if (item > array[current]) ^ descending:
      first = current+1
    else:
      last = current-1
  return not_found
