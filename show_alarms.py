#!/usr/bin/env python

import fitbit
import sys
import locale
import datetime

if __name__ == '__main__':

    weekdays = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

    if not (len(sys.argv) == 5):
        print "Arguments 'consumer key', 'consumer secret', 'user key', 'user secret', are required"
        sys.exit(1)

    CONSUMER_KEY = sys.argv[1]
    CONSUMER_SECRET = sys.argv[2]
    USER_KEY = sys.argv[3]
    USER_SECRET = sys.argv[4]

    client = fitbit.Fitbit(CONSUMER_KEY, CONSUMER_SECRET, user_key=USER_KEY, user_secret=USER_SECRET)

    now = datetime.datetime.now()
    print 'now = {0}'.format(now)

    next_alarm = None
    devices = client.get_devices()
    for device in devices:
        print '--- device {0} ---'.format(device['id'].decode())
        alarms = client.get_alarms(device['id'])
        i = 1;
        for alarm in alarms['trackerAlarms']:
            print '- {0}. alarm'.format(i)
            i += 1
            for key in alarm:
                print '{0}: {1}'.format(key, alarm[key])
            print ''

            if not alarm['enabled']:
                continue

            alarm_dt = None
            if alarm['recurring']:
                for weekday in alarm['weekDays']:
                    d = weekdays.index(weekday)
                    if d > now.weekday():
                        alarm_dt = now + datetime.timedelta(days=d-now.weekday())
                        alarm_dt = alarm_dt.replace(hour=int(alarm['time'].decode()[:2]), minute=int(alarm['time'].decode()[3:5]), second=0, microsecond=0)
                    elif d < now.weekday():
                        alarm_dt = now + datetime.timedelta(days=7-now.weekday()+d)
                        alarm_dt = alarm_dt.replace(hour=int(alarm['time'].decode()[:2]), minute=int(alarm['time'].decode()[3:5]), second=0, microsecond=0)
                    else:
                        alarm_dt = now.replace(hour=int(alarm['time'].decode()[:2]), minute=int(alarm['time'].decode()[3:5]), second=0, microsecond=0)
                        if now > alarm_dt:
                            alarm_dt = alarm_dt + datetime.timedelta(days=7)
                    if next_alarm:
                        if alarm_dt < next_alarm:
                            next_alarm = alarm_dt
                    else:
                        next_alarm = alarm_dt
            else:
                alarm_dt = now.replace(hour=int(alarm['time'].decode()[:2]), minute=int(alarm['time'].decode()[3:5]), second=0, microsecond=0)
                if now > alarm_dt:
                    alarm_dt = alarm_dt + datetime.timedelta(days=1)
                if next_alarm:
                    if alarm_dt < next_alarm:
                        next_alarm = alarm_dt
                else:
                    next_alarm = alarm_dt

    print 'next alarm = {0}'.format(next_alarm)
