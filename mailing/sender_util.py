from django.utils.timezone import now

def check_current_time(time_start, time_end):
    if time_start < now() and now() < time_end:
        starter = now()
    else:
        starter = time_start
    return starter