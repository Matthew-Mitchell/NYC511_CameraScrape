import pandas as pd
import glob
import os
import time
import datetime
from collections import Counter
import re

def format_byte_size(byte_size):
    kb = float(2**10)
    mb = kb**2
    gb = kb**3
    #Under 0.1KB
    if byte_size < 0.1*kb:
        return "{} bytes".format(byte_size)
    elif byte_size < 0.1*mb:
        return "{} kb".format(round(byte_size/kb,2))
    elif byte_size < 0.5*gb:
        return "{} mb".format(round(byte_size/mb,2))
    else:
        return "{} gb".format(round(byte_size/gb,2))

def extract_filetime(filename):
    try:
        base_filename = "NYC_511_ImageScrape_File_Summary_as_of_"
        pattern = "{base_filename}(\d\d-\d\d-\d\d\d\d)[.]csv".format(base_filename=base_filename)
        date_str = re.findall(pattern,filename)[0]
        return pd.to_datetime(date_str)
    except:
        return None

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
            subfile_sizes = [os.path.getsize(subfile) for subfile in subfiles]
            monthly_summaries = dict(Counter([x.strftime("%B %Y") for x in subfile_timestamps]))
            nimages_today = len([x for x in subfile_timestamps if x>today])
            nimages_last_week = len([x for x in subfile_timestamps if x>last_week])
            #print(list(zip(subfiles, subfile_timestamps)))
            summary = {'min': min(subfile_timestamps),
                       'max': max(subfile_timestamps),
                       'count' : len(subfile_timestamps),
                       'nimages_today': nimages_today,
                       'nimages_last_week' : nimages_last_week,
                       'total_size_in_bytes' : sum(subfile_sizes)
                      }
            summary = {**summary, **monthly_summaries}
            
        else:
            summary = {'min':None,'max':None, 'count':0}
        folder_summaries[folder.strip('images/')] = summary
    df = pd.DataFrame.from_dict(folder_summaries).transpose()
    df = df.sort_values(by='max', ascending=False)
    if autosave | to_print:
        #Needed for both branches below.
        previous_snapshots = glob.glob("NYC_511_ImageScrape_File_Summary_as_of_*.csv")
        previous_snapshots = sorted(previous_snapshots, key=lambda x: extract_filetime(x))
        last_file = previous_snapshots[-1]
    if to_print:
        n_images = df['count'].sum()
        print("Total Files: {}".format(n_images))
        print("Images scraped today: {}".format(df['nimages_today'].sum()))
        print("Images scraped in the last week: {}".format(df['nimages_last_week'].sum()))
        previous_total = pd.read_csv(last_file, usecols=['count']).sum()
        n_new_images = n_images - previous_total
        print("Additional files since last snapshot: {}".format(n_new_images))
        byte_size = df['total_size_in_bytes'].sum()
        print("Total Size On Disk: {}".format(format_byte_size(byte_size)))
    if autosave:
        #Potential add on: Detect Existing Image File Snapshots
        if to_print:
            print("Last file: {}".format(last_file))

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