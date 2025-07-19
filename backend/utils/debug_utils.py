import inspect


def get_func_call():
    frame = inspect.currentframe().f_back
    func_name = frame.f_code.co_name
    args, _, _, values = inspect.getargvalues(frame)
    args_str = ", ".join(f"{arg}={repr(values[arg])}" for arg in args)
    return f"{func_name}({args_str})"
