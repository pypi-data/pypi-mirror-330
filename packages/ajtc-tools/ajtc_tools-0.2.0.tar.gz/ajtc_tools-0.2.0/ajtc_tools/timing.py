import time

def time_function(func):
    """
    Decorator to time the execution of a function and print the result in scientific notation.
    
    Args:
        func (callable): The function to be wrapped and timed.
    
    Returns:
        callable: A wrapped function that times execution and prints the result.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start timing
        result = func(*args, **kwargs)  # Run the function
        end_time = time.time()  # End timing

        elapsed_time = end_time - start_time  # Compute elapsed time
        print(f"{func.__name__} took {elapsed_time:.3e} seconds")
        
        return result  # Return the function's result
    return wrapper

def time_once(func, *args, **kwargs):
    """
    Times a single execution of a function without permanently wrapping it.
    
    Args:
        func (callable): The function to be timed.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
    
    Returns:
        Any: The return value of the function after execution.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"{func.__name__} took {elapsed_time:.3e} seconds")
    
    return result
