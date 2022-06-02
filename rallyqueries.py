import sys
import os
import pandas as pd
import time
from datetime import datetime
from datetime import date

from pyral import Rally, rallyWorkset


tasks_in_backlog = {"Name": [], "formattedID": [], "ScheduleState": [] , "CreationDate": [], "duration_in_backlog": [], "added_today": []}

rally = Rally("rally1.rallydev.com", "email, "password", apiKey=apikey, workspace="Workspace 1", project="Sample Project")
rally.enableLogging('rally.simple-use.log')


response = rally.get('UserStory', fetch="Name,FormattedID,ScheduleState,CreationDate")

for story in response:
    if story.ScheduleState == "Defined":
        tasks_in_backlog["Name"].append(story.Name)
        tasks_in_backlog["formattedID"].append(story.FormattedID)
        tasks_in_backlog["ScheduleState"].append(story.ScheduleState)
        date_added= datetime.strptime(story.CreationDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_today = datetime.now()
        if date_added.date() == date_today.date():
            tasks_in_backlog["added_today"].append("True")
        else:
            tasks_in_backlog["added_today"].append("False")
        tasks_in_backlog["CreationDate"].append(str(date_added))
        tasks_in_backlog["duration_in_backlog"].append(str(date_today - date_added))
       




df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in tasks_in_backlog.items()]))

df.to_csv('rally_stories_duration_in_backlog.csv')

print(df)