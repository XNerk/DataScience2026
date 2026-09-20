#dont take this seriously, this code was written for learning purposes so do expect errors and incorrect usage. 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

csv = "app_usage.csv"


data = pd.read_csv(csv)

#print(data.head())


#find all instances of the usage of "Taskmgr.exe"
apps = data["application"].tolist()


#prints the index of each findings of the Taskmgr
for i,app in enumerate(apps):
    if "Task" in app:
        print(f"found {app}")
        print("at:", i)
    else:
        pass

#summarizes how much each value has appeared
print("------summary-----")
print(data["application"].value_counts())

#prints every distinct app without repetition
print("\n----Unique------")
unique_apps = data["application"].unique()
print("all unique apps:", unique_apps)
print("TOTAL number of unique apps:", data["application"].nunique())



#prints the value with most number of appearance
print("---usage----")
app_groups = data.groupby("application")

print(app_groups.size())


data["start_time"] = pd.to_datetime(data["start_time"])
data["end_time"] = pd.to_datetime(data["end_time"])

data["duration"] = (
    data["end_time"] - data["start_time"]
).dt.total_seconds()

print(data[["application", "duration"]])



#pie chart on the distribution of application appearances
app_counts = data["application"].value_counts()

plt.figure(figsize= (9,9))

plt.pie(app_counts,labels=app_counts.index,autopct="%1.1f%%",startangle=90)

plt.title("distribution of application appearances")

plt.axis("equal")
plt.show()





