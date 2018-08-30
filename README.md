# SpeedTweet
Tweet at Comcast every time your speed dips too low.

For a while I was having a lot of trouble with my internet connection. I'd call up, sit on hold for half an hour, and then the Comcast service rep would tell me that there were no outages in my area and they'd try to blame it on the fact that I owned my modem rather than renting one of theirs. And no matter how many times I called, they never seemed to have any record of there ever being any previous issues.

I discovered that Comcast has a pretty responsive customer service team on Twitter. And better yet, I don't have to sit on hold to talk to them -- I just tweet at them and they respond, and there's the added bonus that I also have a written record of the discussion.

This project is a bit discombobulated -- I used speedtest-cli (like I do in Weather-vs-Internet-Speed) to measure and log my internet speeds with my Raspberry Pi.

Then speedtweet.py takes a look and checks if I've had slow speeds for an hour. If so, it automatically tweets at Comcast. I wrote it in Python because I wanted it to run on the Raspberry Pi without too much fuss.

And because I had the data I decided to create a graph of my speeds so I could see performance over time, then upload the PNG to a site that I can view over the internet. PlotIt.r is written in R because that's what I initially used when I was looking at my speedtest data, so I just spun out a little script for that. The Python script (plotit.py) is an updated version written so that the whole process lives on my Raspberry Pi.
