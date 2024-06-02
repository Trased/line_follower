import _thread

#Shared variables and a lock
action = 'go'
speed = 0.003
need_to_stop = False
variable_lock = _thread.allocate_lock()

