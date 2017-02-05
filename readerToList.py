import numpy as np
import csv

class TimeJus(object):
    month_name = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    def __init__(self, target=""):
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None
        self.millisec = None

        if target != "":
            self.setTime(target)
            
    def setTime(self, target):
        
        if target.endswith("(ICT)"):
            ##format Fri Dec 02 2016 01:47:30 GMT+0700 (ICT)
            path = target.split()
            self.day = int(path[2])
            self.month = TimeJus.month_name.index(path[1])+1
            self.year = int(path[3])
            self.hour, self.minute, self.second = [int(_) for _ in path[4].split(':')]
            self.millisec = 0
        elif target.endswith("AM") or target.endswith("PM"):
            ##Default Fotmat; '23-03-2011 10:29 PM'
            path = target.split()
            self.day, self.month, self.year = [int(_) for _ in path[0].split('-')]
            self.hour, self.minute = [int(_) for _ in path[1].split(':')]
            self.second = 0
            self.millisec = 0
            if path[2] == "AM" and self.hour==12:
                self.hour = 0
            if path[2] == "PM":
                self.hour += 12
        elif target.endswith("Z"):
            ##Format: 2016-11-09T13:55:11.000Z
            path = target.split("T")
            datepath, timepath = path
            datepath = datepath.split("-")
            timepath = timepath.split(":")
            
            self.year, self.month, self.day = [int(_) for _ in datepath]
            self.hour = int(timepath[0])
            self.minute = int(timepath[1])
            self.second = int(timepath[2].split(".")[0])
            self.millisec = int(timepath[2].split(".")[1].strip("Z"))
            
        else:
            print(target)
            print("WTF")
            input()
            

    def __str__(self):
        try:
            return "%02d:%02d:%02d %02d/%02d/%04d" \
            % (self.hour, self.minute, self.second, self.day, self.month, self.year)
        except:
            print(self.hour, self.minute, self.second, self.day, self.month, self.year)
            input()
    def getDatePath(self):
        return "%02d/%02d/%04d" \
        % (self.day, self.month, self.year)

    def getTimePath(self):
        return "%02d:%02d:%02d" \
        % (self.hour, self.minute, self.second)

    def toSecond(self):
        total_day = 0
        for _ in range(1900, self.year):
            total_day += 366 if TimeJus.isLeapYear(_) else 365
        total_day += self.getCumulativeDay()
        if self.month >= 2:
            total_day += TimeJus.isLeapYear(self.year)
        total_day += self.day

        total_sec = 0
        total_sec += total_day*24*60*60
        total_sec += self.hour*60*60
        total_sec += self.minute*60
        total_sec += self.second
        return total_sec

    def toSecondTimePath(self):
        return (self.hour*60+self.minute)*60+self.second

    def isLeapYear(target):
        if target % 4 == 0:
            if target % 100 == 0:
                if target % 400 == 0:
                    return 1
                return 0
            return 1
        return 0

    def getCumulativeDay(self):
        return sum(TimeJus.month_day[:self.month-1])

def file_reader(filename):
    fin = open(filename, encoding="UTF-8")
    spamreader = csv.reader(fin)

    dx = {}

    flag = True
    mode = None
    venue_target = "4af833a6f964a5205a0b22e3" ##For mode 0; 1;
    for line in spamreader:
        
        if flag:
            ##First Line, mark attribute position here.
            line = [word.lower() for word in line]
            line[0] = line[0].strip("\ufeff")

            if "venueid" in line:
                ##Section by venue column
                venue_position = line.index("venueid")
                datemark_position = line.index("datetime")
                if "count" in line:
                    count_position = line.index("count")
                    mode = 1
                else:
                    count_position = None
                    mode = 0
            if "text" in line:
                ##Not section, already in the same venue.
                datemark_position = line.index("created_at")
                mode = 2
                
            flag = False
            continue
        
        
        if mode in [0, 1]:
            venue_id = line[venue_position]
        elif mode == 2:
            venue_target = "None"
            venue_id = venue_target

        if venue_id not in dx:
            dx[venue_id] = []
        if mode == 1:
            dx[venue_id].append((TimeJus(line[datemark_position]), int(line[count_position])))
        elif mode == 0 or mode == 2:
            dx[venue_id].append((TimeJus(line[datemark_position]), 1))

        if venue_target == venue_id and 0:
            print(line[datemark_position], TimeJus(line[datemark_position]))

    if venue_target in dx:
        dx[venue_target].sort(key=lambda x:x[0].toSecond())
        dx2_key = []
        dx2 = {}
        
        for _ in dx[venue_target]:
            z = _[0].getDatePath()
            z2 = _[0].toSecondTimePath()//300
            
            if z not in dx2:
                dx2[z] = {}
                dx2_key.append(z)
            if z2 not in dx2[z]:
                
                if mode == 1:
                    dx2[z][z2] = []
                else:
                    dx2[z][z2] = 0
                    
            if mode == 1:
                dx2[z][z2].append(_[1])
            else:
                dx2[z][z2] += 1

        fdx = {}
        
        fout = open("%s_%s.csv" % (filename.split(".")[0], venue_target), "w")
        fout2 = open("%s_%s.txt" % (filename.split(".")[0], venue_target), "w")
        
        fout.writelines(","+",".join(dx2_key)+"\n")
        
        for _ in range(288):
            mark_ = _
            
            _ = _*300
            
            _min = _ // 60
            _ %= 60
            _hour = _min//60
            _min %= 60
            
            _text = ""
            for key in dx2_key:
                iso8601 = "%s-%s-%s" % (key.split("/")[::-1][0], key.split("/")[::-1][1], key.split("/")[::-1][2])

                if iso8601 not in fdx:
                    fdx[iso8601] = []
                if mark_ not in dx2[key]:
                    _text += "-,"
                    fdx[iso8601].append(0)
                else:
                    if isinstance(dx2[key][mark_], int):
                        _text += "%d," % (dx2[key][mark_])
                        fdx[iso8601].append(dx2[key][mark_])
                    elif isinstance(dx2[key][mark_], list):
                        _text += "%d," % (np.average(dx2[key][mark_]))
                        fdx[iso8601].append(np.floor(np.average(dx2[key][mark_])))

                
                

            fout.writelines("%02d:%02d,%s\n" % (_hour, _min, _text))

        f2dx = []
        for key in fdx:
            f2dx.append({"date": key, "dense": fdx[key]})
        fout2.writelines(str(f2dx)+"\n")
        
        fout2.close()
        fout.close()
                    
##############################################################
##Venue Target: 4b0587fdf964a52034ab22e3
file_reader("fqPhotkinFile30JAN.csv")
file_reader("fqPhotoFile30JAN.csv")


