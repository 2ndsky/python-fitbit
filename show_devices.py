#!/usr/bin/env python

import fitbit
import sys

if __name__ == '__main__':

    if not (len(sys.argv) == 5):
        print "Arguments 'consumer key', 'consumer secret', 'user key', 'user secret' are required"
        sys.exit(1)

    CONSUMER_KEY = sys.argv[1]
    CONSUMER_SECRET = sys.argv[2]
    USER_KEY = sys.argv[3]
    USER_SECRET = sys.argv[4]

    client = fitbit.Fitbit(CONSUMER_KEY, CONSUMER_SECRET, user_key=USER_KEY, user_secret=USER_SECRET)

    '''
    [
        {
            u'battery': u'Medium', 
            u'lastSyncTime': u'2014-01-20T18:44:54.000', 
            u'mac': u'ABCDEF012345', 
            u'type': u'TRACKER', 
            u'id': u'1234567', 
            u'deviceVersion': u'Force'
        }
    ]
    '''

    i = 1;
    devices = client.get_devices()
    for device in devices:
        print '--- {0}. device ---'.format(i)
        i += 1
        for key in device:
            print key.decode() + ': ' + device[key].decode()
        print ''
    
    print 'Done.'
