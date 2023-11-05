import pandas as pd
import glob
import os
import time
import datetime
from collections import Counter

def image_scrape_summary(to_print=True, autosave=True, save_snapshot_cadence='daily'):
    now = datetime.datetime.now()
    today = pd.to_datetime((now).strftime("%Y-%m-%d"))
    #yesterday = today - pd.Timedelta(days=1)
    last_week = today - pd.Timedelta(days=7)

    camera_folders = [folder for folder in glob.glob("images/*") if os.path.isdir(folder)]
    print(len(camera_folders), camera_folders[:3], camera_folders[-3:])
    folder_summaries = {}
    for folder in camera_folders:
        subfiles = glob.glob("{}/*".format(folder))
        if len(subfiles) > 0:
            subfile_timestamps = [pd.to_datetime(time.ctime(os.path.getmtime(subfile))) for subfile in subfiles]
            monthly_summaries = dict(Counter([x.strftime("%B %Y") for x in subfile_timestamps]))
            nimages_today = len([x for x in subfile_timestamps if x>today])
            nimages_last_week = len([x for x in subfile_timestamps if x>last_week])
            #print(list(zip(subfiles, subfile_timestamps)))
            summary = {'min': min(subfile_timestamps),
                       'max': max(subfile_timestamps),
                       'count' : len(subfile_timestamps),
                       'nimages_today': nimages_today,
                       'nimages_last_week' : nimages_last_week
                      }
            summary = {**summary, **monthly_summaries}
            
        else:
            summary = {'min':None,'max':None, 'count':0}
        folder_summaries[folder.strip('images/')] = summary
    df = pd.DataFrame.from_dict(folder_summaries).transpose()
    df = df.sort_values(by='max', ascending=False)
    if to_print:
        print("Total Files: {}".format(df['count'].sum()))
        print("Images scraped today: {}".format(df['nimages_today'].sum()))
        print("Images scraped in the last week: {}".format(df['nimages_last_week'].sum()))

    if autosave:
        #Potential add on: Detect Existing Image File Snapshots
        
        filename = "NYC_511_ImageScrape_File_Summary_as_of_{}.csv".format(now.strftime("%m-%d-%Y"))
        if os.path.isfile(filename):
            overwrite = input("File: {} already exists. Do you wish to overwrite? (Y/N)".format(filename))
            if overwrite:
                if to_print:
                    print("Overwriting file. Saving to: {}".format(filename))
                df.to_csv(filename)
        else:
            df.to_csv(filename)
            if to_print:
                    print("Saving to: {}".format(filename))
    return df