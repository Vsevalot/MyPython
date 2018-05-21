# -*- coding: utf-8 -*-
token = "428046149:AAH1uatlUpP5BFr_0ct8cV2RoyQggwaN_CU"

if __name__ == '__main__':
    import pickle
    import datetime

    schedule = pickle.load(open("schedule.pickle", "rb"))

    def closestBus(bus_number=108, current_time=datetime.datetime.now()):
        h = current_time.hour
        m = current_time.minute
        s = current_time.second

        now = datetime.timedelta(hours = h, minutes = m, seconds = s)
        closest_bus = None
        time_remaining = None

        for time in schedule[bus_number]:
            if time > now:
                closest_bus = time
                time_remaining = str(time - now)
                break
        if closest_bus is None:
            closest_bus = schedule[bus_number][0]
            time_remaining = str(schedule[bus_number][0] - now + datetime.timedelta(days = 1))

        closest_bus = ':'.join(str(closest_bus).split(':')[:2])
        time_remaining = time_remaining.split(':')
        if time_remaining[0] == '0':
            remaining_string = "{} minutes {} seconds".format(time_remaining[1], time_remaining[2])
        else:
            remaining_string = "{} hours {} minutes {} seconds".format(time_remaining[0], time_remaining[1], time_remaining[2])



        message = "The closest bus at {} \U0001f86b\n" \
                  "Time remaining: {}".format(closest_bus, remaining_string)
        return message



    print(closestBus())



