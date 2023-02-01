#!/usr/bin/env python

'''
example program that dumps a Mavlink log file. The log file is
assumed to be in the format that qgroundcontrol uses, which consists
of a series of MAVLink packets, each with a 64 bit timestamp
header. The timestamp is in microseconds since 1970 (unix epoch)
'''

import sys, time, os, struct, json, fnmatch, os, csv

file_list=[f for f in os.listdir() if f.endswith(".BIN")]
file_list.sort()
for i in range(0,len(file_list)):
    print("{} : {}".format(i+1, file_list[i]))
file_num=int(input("選擇檔案(輸入數字) : "))

try:
    from pymavlink.mavextra import *
except:
    print("WARNING: Numpy missing, mathematical notation will not be supported..")

from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)

parser.add_argument("--no-timestamps", dest="notimestamps", action='store_true', help="Log doesn't have timestamps")
parser.add_argument("--planner", action='store_true', help="use planner file format")
parser.add_argument("--robust", action='store_true', help="Enable robust parsing (skip over bad data)")
parser.add_argument("-f", "--follow", action='store_true', help="keep waiting for more data at end of file")
parser.add_argument("--condition", default=None, help="select packets by condition")
parser.add_argument("-q", "--quiet", action='store_true', help="don't display packets")
parser.add_argument("-o", "--output", default=None, help="output matching packets to give file")
parser.add_argument("-p", "--parms", action='store_true', help="preserve parameters in output with -o")
parser.add_argument("--format", default=None, help="Change the output format between 'standard', 'json', and 'csv'. For the CSV output, you must supply types that you want.")
parser.add_argument("--csv_sep", dest="csv_sep", default=",", help="Select the delimiter between columns for the output CSV file. Use 'tab' to specify tabs. Only applies when --format=csv")
parser.add_argument("--types", default=None, help="types of messages (comma separated with wildcard)")
parser.add_argument("--nottypes", default=None, help="types of messages not to include (comma separated with wildcard)")
parser.add_argument("--dialect", default="ardupilotmega", help="MAVLink dialect")
parser.add_argument("--zero-time-base", action='store_true', help="use Z time base for DF logs")
parser.add_argument("--no-bad-data", action='store_true', help="Don't output corrupted messages")
parser.add_argument("--show-source", action='store_true', help="Show source system ID and component ID")
#parser.add_argument("log", metavar="LOG")
args = parser.parse_args()

import inspect

from pymavlink import mavutil


filename = file_list[file_num-1]
mlog = mavutil.mavlink_connection(filename, planner_format=args.planner,
                                  notimestamps=args.notimestamps,
                                  robust_parsing=args.robust,
                                  dialect=args.dialect,
                                  zero_time_base=args.zero_time_base)

output = None
if args.output:
    output = open(args.output, mode='wb')

types = args.types
if types is not None:
    types = types.split(',')

nottypes = args.nottypes
if nottypes is not None:
    nottypes = nottypes.split(',')

ext = os.path.splitext(filename)[1]
isbin = ext in ['.bin', '.BIN']
islog = ext in ['.log', '.LOG','.tlog','.TLOG']

if args.csv_sep == "tab":
    args.csv_sep = "\t"

def match_type(mtype, patterns):
    '''return True if mtype matches pattern'''
    for p in patterns:
        if fnmatch.fnmatch(mtype, p):
            return True
    return False

# Write out a header row as we're outputting in CSV format.
fields = ['timestamp']
offsets = {}
if islog and args.format == 'csv': # we know our fields from the get-go
    try:
        currentOffset = 1 # Store how many fields in we are for each message.
        for type in types:
            try:
                typeClass = "MAVLink_{0}_message".format(type.lower())
                fields += [type + '.' + x for x in inspect.getargspec(getattr(mavutil.mavlink, typeClass).__init__).args[1:]]
                offsets[type] = currentOffset
                currentOffset += len(fields)
            except IndexError:
                quit()
    except TypeError:
        print("You must specify a list of message types if outputting CSV format via the --types argument.")
        exit()

    # The first line output are names for all columns
    csv_out = ["" for x in fields]
    print(','.join(fields))

if isbin and args.format == 'csv': # need to accumulate columns from message
    if types is None or len(types) != 1:
        print("Need exactly one type when dumping CSV from bin file")
        quit()

# Track the last timestamp value. Used for compressing data for the CSV output format.
last_timestamp = None




folder_name=filename.replace(".BIN","")
if os.path.isdir(folder_name):
    ans=input(("此檔案已建檔, 是否要全部刷新取代? (y/n) : "))
    if ans=="y":
        for n in os.listdir(folder_name):
            os.remove(folder_name+"/"+n)
            print("刪除檔案 : {}".format(folder_name+"/"+n))
        print("舊檔案刪除完畢")
        
    else:
        exit()

else:
    os.mkdir(folder_name)
    print("建立資料夾 : {}".format(folder_name))


# Keep track of data from the current timestep. If the following timestep has the same data, it's stored in here as well. Output should therefore have entirely unique timesteps.
print("讀檔中")

start_time=time.time() #記錄開始時間
type_list=[]
raw_data={}
while True:
    m = mlog.recv_match(blocking=args.follow)  #讀取一個row
    
    #print(m.get_type())
    #print(type(m.get_type()))
    #print(m.to_dict())
    if m is None:  #如果沒東西就離開迴圈 
        # FIXME: Make sure to output the last CSV message before dropping out of this loop
        break

    #如果有資料
    temp_type=m.get_type() #取得資料型態
    if temp_type not in raw_data:  #如果這個資料的type還沒有被看過. 就把資料的type放進去list存起來(e.g. GPS, MAG2, MAG3 ,NKF9)
        raw_data[temp_type]=[]
    raw_data[temp_type].append(m.to_dict()) #把這筆row轉成dictionary的型態
    







    if isbin and m.get_type() == "FMT" and args.format == 'csv':
        if m.Name == types[0]:
            fields += m.Columns.split(',')
            csv_out = ["" for x in fields]
            print(','.join(fields))

    if output is not None:
        if (isbin or islog) and m.get_type() == "FMT":
            output.write(m.get_msgbuf())


            continue
        if (isbin or islog) and (m.get_type() == "PARM" and args.parms):
            output.write(m.get_msgbuf())
            continue
        if m.get_type() == 'PARAM_VALUE' and args.parms:
            timestamp = getattr(m, '_timestamp', None)
            output.write(struct.pack('>Q', timestamp*1.0e6) + m.get_msgbuf())
            continue
    if not mavutil.evaluate_condition(args.condition, mlog.messages):
        continue

    if types is not None and m.get_type() != 'BAD_DATA' and not match_type(m.get_type(), types):
        continue

    if nottypes is not None and match_type(m.get_type(), nottypes):
        continue

    # Ignore BAD_DATA messages is the user requested or if they're because of a bad prefix. The
    # latter case is normally because of a mismatched MAVLink version.
    if m.get_type() == 'BAD_DATA' and (args.no_bad_data is True or m.reason == "Bad prefix"):
        continue

    # Grab the timestamp.
    timestamp = getattr(m, '_timestamp', 0.0)

    # If we're just logging, pack in the timestamp and data into the output file.
    if output:
        if not (isbin or islog):
            output.write(struct.pack('>Q', timestamp*1.0e6))
        try:
            output.write(m.get_msgbuf())
        except Exception as ex:
            print("Failed to write msg %s" % m.get_type())
            pass

    # If quiet is specified, don't display output to the terminal.
    if args.quiet:
        continue

    # If JSON was ordered, serve it up. Split it nicely into metadata and data.
    if args.format == 'json':
        # Format our message as a Python dict, which gets us almost to proper JSON format
        data = m.to_dict()

        # Remove the mavpackettype value as we specify that later.
        del data['mavpackettype']

        # Also, if it's a BAD_DATA message, make it JSON-compatible by removing array objects
        if 'data' in data and type(data['data']) is not dict:
            data['data'] = list(data['data'])

        # Prepare the message as a single object with 'meta' and 'data' keys holding
        # the message's metadata and actual data respectively.
        outMsg = {"meta": {"type": m.get_type(), "timestamp": timestamp}, "data": data}

        # Now print out this object with stringified properly.
        print(json.dumps(outMsg))
    # CSV format outputs columnar data with a user-specified delimiter
    elif args.format == 'csv':
        data = m.to_dict()
        type = m.get_type()

        # If this message has a duplicate timestamp, copy its data into the existing data list. Also
        # do this if it's the first message encountered.
        if timestamp == last_timestamp or last_timestamp is None:
            if isbin:
                newData = [str(data[y]) if y != "timestamp" else "" for y in fields]
            else:
                newData = [str(data[y.split('.')[-1]]) if y.split('.')[0] == type and y.split('.')[-1] in data else "" for y in fields]

            for i, val in enumerate(newData):
                if val:
                    csv_out[i] = val
                    print(val)

        # Otherwise if this is a new timestamp, print out the old output data, and store the current message for later output.
        else:
            csv_out[0] = "{:.8f}".format(last_timestamp)
            #print(args.csv_sep.join(csv_out))
            if isbin:
                csv_out = [str(data[y]) if y != "timestamp" else "" for y in fields]
            else:
                csv_out = [str(data[y.split('.')[-1]]) if y.split('.')[0] == type and y.split('.')[-1] in data else "" for y in fields]
    # Otherwise we output in a standard Python dict-style format
    else:
        s = "%s.%02u: %s" % (time.strftime("%Y-%m-%d %H:%M:%S",
                                           time.localtime(timestamp)),
                             int(timestamp*100.0)%100, m)
        if args.show_source:
            s += " srcSystem=%u srcComponent=%u" % (m.get_srcSystem(), m.get_srcComponent())
        #print(s)
        #print(m)
        #print(type(s))


    # Update our last timestamp value.
    last_timestamp = timestamp


mid_time=time.time()
print("讀取完畢")
print("讀取花費時間 : {} 秒".format(mid_time-start_time))
print("總共有{}筆資料".format(len(raw_data)))
print("建立csv檔案中")

for data in raw_data: #有幾種type就建立幾個csv檔（type就是檔名）
    with open(folder_name+"/"+data+".csv", "a+", newline="") as csvfile:
        fieldnames=[]
        temp_dict = raw_data[data][0].keys()
        for temp in temp_dict:
            fieldnames.append(temp)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)#建立csv第一行的標題
        writer.writeheader()
        for record_data in raw_data[data]:
            writer.writerow(record_data)



end_time=time.time()
print("寫入花費時間 : {} 秒".format(end_time-mid_time))