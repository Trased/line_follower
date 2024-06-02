from modules_follower import follow_line
import modules_shared
def run_machine():
    try:
        while not modules_shared.need_to_stop:
            if modules_shared.action == 'go':
                follow_line(modules_shared.speed)
            elif modules_shared.action == 'stop':
                pass
    except Exception as e:
        print("Exception:", e)
    finally:
        for pin in phasesRight + phasesLeft:
            pin.value(0)
        print("Application exited cleanly")

