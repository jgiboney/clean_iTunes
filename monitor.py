import Foundation
import time
from AppKit import *
from PyObjCTools import AppHelper
import subprocess
import threading
import csv
import os.path

TIME_RANGE = 1
threads = []


class StartMonitor(NSObject):
    def getDetails_(self, song):
        song_details = {}
        ui = song.userInfo()
        for x in ui:
            song_details[x] = ui.objectForKey_(x)
        #print song_details
        media_name = song_details['Name']
        media_year = song_details['Year']
        file_path = 'movie_scripts/'+media_name+' _'+str(media_year)+'.csv'
        for t in threads:
            t.stop()
        if os.path.isfile(file_path):
            print "Filtering "+media_name+' '+str(media_year)
            with open(file_path, 'rb') as f:
                reader = csv.reader(f)
                commands_array = list(reader)
                #print commands_array
            if song_details['Player State'] == 'Playing':
                t = MonitorThread(commands_array)
                threads.append(t)
                t.start()
        else:
            print 'No cleaning file found.'

class MonitorThread(threading.Thread):
    def __init__(self, command_array):
        super(MonitorThread, self).__init__()
        self.commands_array = command_array
        self._stopped = False
        
    def stop(self):
        self._stopped = True
        
    def run (self):
        while not self._stopped:
            x = subprocess.Popen(["osascript", "applescripts/get_position.scpt"], stdout=subprocess.PIPE).communicate()[0]
            #print x
            for command in self.commands_array:
                if float(command[1])-float(x) <= TIME_RANGE and float(command[1])-float(x) >= 0-TIME_RANGE:
                    if command[0] == 'skip':
                        subprocess.Popen(["osascript", "applescripts/skip.scpt", str(command[2])])
                    elif command[0] == 'mute':
                        subprocess.Popen(["osascript", "applescripts/mute.scpt", str(command[2])])
            time.sleep(1)
            


nc = Foundation.NSDistributedNotificationCenter.defaultCenter()
StartMonitor = StartMonitor.new()
nc.addObserver_selector_name_object_(StartMonitor, 'getDetails:', 'com.apple.iTunes.playerInfo',None)

NSLog("Listening for new media....")
AppHelper.runConsoleEventLoop()