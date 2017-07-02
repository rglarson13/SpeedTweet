# Script to generate a plot from speedtest logs

library(tidyverse)

setwd("D:/BitTorrent Sync/PiSync/Misc Scripts/SpeedTest/")

df <- read.csv("speedtest.csv", header = TRUE)
df <- na.omit(df)

df <- mutate(df, Date = substr(Timestamp, 1, 10), Time = substr(Timestamp, 12, 12 + 7), Download = Download / 1024^2, Upload = Upload / 1024^2)
df <- mutate(df, Timestamp = as.POSIXct(paste(Date, Time, sep = " ")))

png("SpeedTest.png")
plotPoint <- ggplot(data = df) + geom_point(mapping = aes(x = Timestamp, y = Download, color = (Download > 40))) + geom_smooth(mapping = aes(x = Timestamp, y = Download))
print(plotPoint)
dev.off()

#png("SpeedTest-smooth.png")
#plotSmooth <- ggplot(data = df) + geom_smooth(mapping = aes(x = Timestamp, y = Download))
#print(plotSmooth)
#dev.off()

library(RCurl)
ftpUpload("SpeedTest.png", "ftp://username:password@ftp.address.com/SpeedTest.png")