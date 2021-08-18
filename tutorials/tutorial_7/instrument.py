from functools import wraps
import sys

SHOW_CALLS = True
TRIM_ARGS = 55 #None if no trimming
TRIM_RET = 60  #None if no trimming

def instrument(f):
    """ wrapper to instrument a function to show the
        call entry and exit from that function
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        call_depth = wrapper.call_count
        wrapper.call_count += 1
        arg_str = ', '.join([str(args[i]) for i in range(len(args))])
        if TRIM_ARGS is not None and len(arg_str) > TRIM_ARGS:
            arg_str = arg_str[:TRIM_ARGS] + " ..."
        if SHOW_CALLS:
            sys.stderr.write("   "*call_depth + "call to " + f.__name__ + ": " + arg_str + "\n")
        result = f(*args, **kwargs)
        res_str = str(result)
        if TRIM_RET is not None and len(res_str) > TRIM_RET:
            res_str = res_str[:TRIM_RET] + " ..."
        if SHOW_CALLS:
            sys.stderr.write("   "*call_depth + f.__name__ + " returns: " +  res_str + "\n")
        wrapper.call_count -= 1
        return result
    wrapper.call_count = 0
    return wrapper
