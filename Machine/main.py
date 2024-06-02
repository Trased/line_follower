from modules_receivers import run_receivers
from modules_drivers import run_machine
import _thread

receivers_thread = _thread.start_new_thread(run_machine, ())

run_receivers() 

