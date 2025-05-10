import os
import sys


def get_root():
    frame = sys._getframe(1)
    caller_file = frame.f_globals['__file__']
    current_dir = os.path.dirname(os.path.abspath(caller_file))
    root = os.path.dirname(os.path.dirname(current_dir))
    return root
