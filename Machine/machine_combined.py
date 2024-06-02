from modules_receivers import run_receivers
from modules_drivers import run_machine
import modules_shared
import _thread

try:
    receivers_thread = _thread.start_new_thread(run_machine, ())
    run_receivers()
except Exception as e:
        print(f"Error: {e}")
finally:
    with modules_shared.variable_lock:
        modules_shared.need_to_stop = True
    print("Successful exit!")

