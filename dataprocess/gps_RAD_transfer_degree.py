import haversine as hs
from haversine import Unit
import pandas as pd
import math

#input file: RAD.csv & GPS.csv
folder=""
df_GPS = pd.read_csv(folder+'GPS.csv')
df_RAD = pd.read_csv(folder+'RAD.csv')
GPS_frequency=5
RAD_frequency=1
print("GPS.csv shape:", df_GPS.shape)
print("RAD.csv shape:", df_RAD.shape)

GCS_location=(24.7868648, 120.9933247)
GCS_alt=df_GPS["Alt"].min()+1





#------------find start index and end index--------------------
print("find start index and end index")

GPS_time_min=df_GPS["TimeUS"].min()
GPS_time_max=df_GPS["TimeUS"].max()
RAD_time_min=df_RAD["TimeUS"].min()
RAD_time_max=df_RAD["TimeUS"].max()
GPS_start_idx=""
GPS_end_idx=""
RAD_start_idx=""
RAD_end_idx=""

#synchronize the start time
if GPS_time_min>RAD_time_min:
    GPS_start_idx=0
    diff=RAD_time_max   
    for i in range(0,len(df_RAD)):
        if abs(GPS_time_min-df_RAD["TimeUS"][i])<diff:
            diff=abs(GPS_time_min-df_RAD["TimeUS"][i])
            RAD_start_idx=i
    print("start time diff:",diff)
else:
    RAD_start_idx=0
    diff=GPS_time_max  
    for i in range(0,len(df_GPS)):
        if abs(RAD_time_min-df_GPS["TimeUS"][i])<diff:
            diff=abs(RAD_time_min-df_GPS["TimeUS"][i])
            GPS_start_idx=i
    print("start time diff:",diff)

#synchronize the end time
if GPS_time_max>RAD_time_max:
    RAD_end_idx=len(df_RAD)-1
    diff=GPS_time_max   
    for i in range(0,len(df_GPS)):
        if abs(RAD_time_max-df_GPS["TimeUS"][i])<diff:
            diff=abs(RAD_time_max-df_GPS["TimeUS"][i])
            GPS_end_idx=i
    print("end time diff:",diff)
else:
    GPS_end_idx=len(df_GPS)-1
    diff=RAD_time_max   
    for i in range(0,len(df_RAD)):
        if abs(GPS_time_max-df_RAD["TimeUS"][i])<diff:
            diff=abs(GPS_time_max-df_RAD["TimeUS"][i])
            RAD_end_idx=i
    print("end time diff:",diff)


print("GPS_start_idx:",GPS_start_idx)
print("GPS_end_idx:",GPS_end_idx)
print("RAD_start_idx:",RAD_start_idx)
print("RAD_end_idx:",RAD_end_idx)


#--------------------------------------------------------------


#----------------process distance、degree、motion----------------------------

distance_list=[]
degree_list=[]
motion_list=[]  #0:stop, 1:go far, -1:go near
velocity_list=[]
for i in range(0,len(df_GPS)):
    UAV_location=(df_GPS["Lat"][i], df_GPS["Lng"][i])
    horizon_distance=hs.haversine(GCS_location, UAV_location, unit=Unit.METERS)
    height=df_GPS["Alt"][i]-GCS_alt
    distance=math.sqrt( horizon_distance**2+ height**2)
    distance_list.append(distance)
    degree_list.append(math.degrees(math.atan(height/horizon_distance)))
    if i==0:
        velocity=0
        velocity_list.append(velocity)
        motion_list.append(0)
    else:
        if i>=5:
            velocity=distance_list[i]-distance_list[i-5]
            velocity_list.append(velocity)
        else:
            velocity=distance_list[i]-distance_list[i-1]
            velocity_list.append(velocity)

        #print(velocity)
        if velocity>0.05:
            motion_list.append(1)
        elif velocity<-0.05:
            motion_list.append(-1)
        else:
            motion_list.append(0)






#--------------------------------------------------------------

#---------------------define find projection index-------------
# def find_project_idx(origin_time, df_target):
#     diff=abs(origin_time-df_target["TimeUS"][0])
#     index=""
#     for i in range(0,len(df_target)):
#         if abs(origin_time-df_target["TimeUS"][i]) < diff:
#             diff=abs(origin_time-df_target["TimeUS"][i])
#             index=i
#     return index

def find_project_idx(origin_time, df_target, current_idx):
    diff=abs(origin_time-df_target["TimeUS"][0])
    index=""
    for i in range(current_idx,len(df_target)):
        if abs(origin_time-df_target["TimeUS"][i]) < diff:
            diff=abs(origin_time-df_target["TimeUS"][i])
            index=i
        if origin_time-df_target["TimeUS"][i]<=0:
            break
    return index
#--------------------------------------------------------------



#-------------------create processed dataset-------------------

#distance、arctangent、motion、velocity、RSSI
new_distance_list=[]
new_degree_list=[]
new_motion_list=[]
new_velocity_list=[]
new_RSSI_list=[]
current_j=0
for i in range(RAD_start_idx,RAD_end_idx,2):
    #j=find_project_idx(df_RAD["TimeUS"][i], df_GPS)
    j=find_project_idx(df_RAD["TimeUS"][i], df_GPS, current_j)
    current_j=j
    #j= int((i-RAD_start_idx)*(GPS_end_idx-GPS_start_idx)/(RAD_end_idx-RAD_start_idx) + GPS_start_idx)

    #print("time difference between i({}) and j({}): {}".format(i-2, j-2, abs(df_GPS["TimeUS"][j]-df_RAD["TimeUS"][i])))
    new_distance_list.append(distance_list[j])
    new_degree_list.append(degree_list[j])
    new_motion_list.append(motion_list[j])
    new_velocity_list.append(velocity_list[j])
    new_RSSI_list.append(df_RAD["RSSI"][i])
    

new_df=pd.DataFrame()
new_df["date"]=[i+1 for i in range(len(new_distance_list))]
new_df["Distance"]=new_distance_list
# new_df["RSSI"]=new_RSSI_list
new_df["OT"]=new_RSSI_list
new_df.to_csv("processed_data_dis.csv", index=False)
print(new_df)

new_df=pd.DataFrame()
new_df["date"]=[i+1 for i in range(len(new_distance_list))]
new_df["Distance"]=new_distance_list
new_df["Angle"]=new_degree_list
# new_df["RSSI"]=new_RSSI_list
new_df["OT"]=new_RSSI_list
new_df.to_csv("processed_data_dis_ang.csv", index=False)
print(new_df)

new_df=pd.DataFrame()
new_df["date"]=[i+1 for i in range(len(new_distance_list))]
new_df["Distance"]=new_distance_list
new_df["Angle"]=new_degree_list
new_df["Motion"]=new_motion_list
# new_df["RSSI"]=new_RSSI_list
new_df["OT"]=new_RSSI_list
new_df.to_csv("processed_data_dis_ang_mot.csv", index=False)
print(new_df)

new_df=pd.DataFrame()
new_df["date"]=[i+1 for i in range(len(new_distance_list))]
new_df["Distance"]=new_distance_list
new_df["Angle"]=new_degree_list
new_df["Motion"]=new_motion_list
new_df["Velocity"]=new_velocity_list
# new_df["RSSI"]=new_RSSI_list
new_df["OT"]=new_RSSI_list
new_df.to_csv("processed_data_all.csv", index=False)
print(new_df)

    


#--------------------------------------------------------------




print(max(distance_list),min(distance_list))
print(max(velocity_list),min(velocity_list))




