#
# add this to ~/.profile
#
import os, atexit
try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")
__history_location__ = os.path.expanduser("~/.python_history")
if os.path.exists(__history_location__):
    readline.read_history_file(__historty_location__)
def save_hist(file_path=__history_location__):
    import readline
    readline.write_history_file(file_path)
atexit.register(save_hist)
del os, atexit
