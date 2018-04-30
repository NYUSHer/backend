from time import localtime
global WORKDAYS, FRIDAYS, WEEKEND

WORKDAYS = {'D2A': [("07:00", 5), ("08:30", 8), ("10:30", 5), ("11:45", 1), ("12:45", 1), ("14:15", 1), ("15:15", 1),
                   ("16:15", 1), ("19:15", 1)],

            'A2D': [("09:45", 1), ("11:45", 1), ("12:45", 1), ("13:45", 1), ("14:45", 1), ("15:15", 1), ("16:15", 1),
                   ("16:45", 1), ("17:15", 1), ("17:45", 1), ("18:15", 2), ("18:45", 1), ("19:15", 1), ("19:45", 1),
                   ("20:15", 2), ("20:45", 1), ("21:15", 1), ("21:45", 1), ("22:15", 1), ("22:45", 1), ("23:45", 1)]}

FRIDAYS = {'D2A': [("07:00", 5), ("08:30", 8), ("10:30", 5), ("11:45", 1), ("12:45", 1),
                   ("14:15", 1), ("15:15", 1), ("16:15", 1)],

           'A2D': [("9:45", 1), ("11:45", 1), ("12:45", 1), ("13:45", 1), ("14:45", 1), ("15:15", 1), ("16:15", 1),
                   ("16:45", 1), ("17:15", 1), ("17:45", 1), ("18:15", 1), ("18:45", 1), ("19:45", 1), ("20:45", 1),
                   ("21:45", 1), ("22:45", 1)]}

WEEKEND = {'D2A':[("09:00", 1), ("11:00", 1), ("14:30", 1), ("16:30", 1)],

            'A2D':[("13:30", 1), ("15:30", 1), ("17:30", 1), ("19:30", 1), ("21:00", 1), ("22:00", 1)]}


def timestr(hour, minute):
    hour = str(hour)
    minute = str(minute)
    if len(hour) < 2:
        hour = '0' + hour
    if len(minute) < 2:
        minute = '0' + minute
    return hour + ':' + minute


def get_recent_shuttles(direction=0, howmany=2):
    """
    0 for dorm to campus
    1 for campus to dorm
    """
    now = localtime()
    if direction:
        dirc = 'A2D'
    else:
        dirc = 'D2A'
    day = now[6]%6
    time = timestr(now[3], now[4])
    data = []
    is_today = True
    while len(data) < howmany:
        if day==0 or day==5:
            schedule = WEEKEND
        elif day==5:
            schedule = FRIDAYS
        else:
            schedule = WORKDAYS

        for i in range(len(schedule[dirc])):
            if len(data) >= howmany:
                break

            if not is_today:
                data.append(schedule[dirc][i])
            elif schedule[dirc][i][0] >= time:
                data.append(schedule[dirc][i])

        is_today = False
        day = (day+1) % 6

    return data
