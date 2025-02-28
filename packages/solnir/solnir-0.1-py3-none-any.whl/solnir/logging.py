from datetime import datetime
import inspect

def log(msg):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    stack = inspect.stack()
    caller = stack[1]
    caller_name = caller.function
    caller_line = caller.lineno

    print(f"[INFO-{caller_name}:{caller_line}] ({formatted_time}) {msg}")