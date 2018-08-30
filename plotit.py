#!/usr/bin/env python3
	
print("Preparing to update SpeedTest graph...")


print("Importing libraries")
import pandas as pd

import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt	

# Read in the speedtest data
print("Reading speedtest log data")
df = pd.read_csv('speedtest.csv')#, index_col = 'Timestamp')

# Clean up rows where speed data wasn't entered
print("Truncating empty rows")
#df = df[~(df['Server ID'] == "Cannot retrieve speedtest configuration")]
df = df.dropna()

# String to timestamp
print("Parsing timestamp data")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create extra columns
df['Hour'] = df['Timestamp'].apply(lambda x: x.hour)
df['Minute'] = df['Timestamp'].apply(lambda x: x.minute)
df['Day'] = df['Timestamp'].apply(lambda x: x.day)
df['Month'] = df['Timestamp'].apply(lambda x: x.month)
df['Year'] = df['Timestamp'].apply(lambda x: x.year)
df['Date'] = pd.to_datetime(df['Timestamp'].dt.date)

print("Calculating transfer speeds")
df['DownMbps'] = df['Download'] / (1024 ** 2)
df['UpMbps'] = df['Upload'] / (1024 ** 2)


# Average speed by day
df_avg = df[['Date', 'DownMbps', 'UpMbps']]
df_avg.columns = ['Date', 'AvgDown', 'AvgUp']

df_avg = df_avg.groupby('Date').mean()
df_avg['Date'] = df_avg.index

print("Bring in average daily speeds")

# Bring in average daily speeds
df = df.merge(df_avg, on = 'Date')
df.index = df['Timestamp'] #switch to datetime index


# Create graph of speed data
print("Generating speed plot")

# Give this graph some style
plt.style.use('seaborn-whitegrid')
font = {'family' : 'Arial', 'weight' : 'bold', 'size'   : 12}
matplotlib.rc('font', **font)

# Create empty figure
fig = plt.figure(figsize = (9,9))
ax = plt.subplot(1, 1, 1)

# Download Speeds
ax.scatter(df.index, df['DownMbps'], alpha = 0.7, s = 12)
ax.plot(df.index, df['AvgDown'], color = 'blue', linewidth = 2)

# Upload speeds
ax.scatter(df.index, df['UpMbps'], alpha = 0.7, s = 12)
ax.plot(df.index, df['AvgUp'], color = 'red', linewidth = 2)

# Set title and axis labels
ax.set_title(df['Timestamp'].min().strftime('Internet speeds (%b %d, %Y - ') + 
             df['Timestamp'].max().strftime('%b %d, %Y)'))
ax.set_xlabel('Date')
ax.set_ylabel('Mbps')

# Add in the legend
ax.legend(["Download", "Upload"], loc='center left', bbox_to_anchor=(1, 0.5))

#sns.despine(top = True, right = True)

# Save the plot to file
print("Exporting plot image to file")
filename = 'speedtest.png'
fig.savefig(filename, bbox_inches = 'tight')

# Upload the file to FTP
print("Uploading file to FTP server")
from ftplib import FTP

# Establish connection, log in
site = ''
un = ''
pw = ''

ftp = FTP(site)
ftp.login(user = un, passwd = pw)

# Change FTP directory
save_dir = ''
ftp.cwd(save_dir)

# Open file as binary and write it to the FTP server
file = open(filename,'rb')
ftp.storbinary('STOR ' + filename, file)

#ftp.retrbinary('RETR filename.jpg', open('filename.jpg', 'wb').write)   #download a file

# Close the FTP connection
ftp.quit()

print("Transfer complete -- exiting script")