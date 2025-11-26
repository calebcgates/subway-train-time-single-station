I created this project so that my girlfriend could see when the train near her appartment would arrive, it's a 6 minute walk there and the train only comes every 12 minutes. and the train spacing is not consistent.

I found that the MTA has a public set of APIs that dont' require authentication. it's not a json api so you do need a python libary to decode the responses.

My goal was to run this on a raspberry pi becuase I have a bunch of them, I knew I could set it up at my home and then pre configure the wifi so that it would attach when I plugged it in at the house i was bringing it to.

I did the initial setup on an old pie and was then forced to upgrade from the 2017 OS to the 2025 os becuase pip wouldnt install any of my dependencies

Hours later, litterally the worst part of projects like this, I had an SD card formatted to ExFat and then copied the 1.1gb ISO onto it.

I then had to boot the pi and go through the startup, thank god I have the microhdmi to hdmi converter, a dongle for micro usb to usb2 with a keyboard and mouse and an extra monitor on my desk.

I did the manual setup and chose the localization and then turned on ssh mode.

Note that I tried to use the raspberry pi installer but it kept rejecting my sd card mid way.  It was ither the installer or it was my sd to microsd adapter.  I got a new adapter and just downloaded the entire image first from their website. that made it much faster to then copy onto the sd card from the command line - it did take a while to finalize

Once I had the OS and ssh turned on I connected via ssh from my mac and pushed the file I had worked on locally to the pi, moved them to the right folder, created a venv, activated it, installed requirments, and ran the script.

the .py file was designed to pull from thesubway api, format the data and then display it on the attached 16 char by 2 char screen.

Some challenges I faced were the contrast of the screen 

Turns out there is a small potentiometer on the back that you can twist, i used an exacto knife, and I foudn the perfect contrast

I also had to add the wifi for the other house

And then set the code to run on startup.

If you choose to clone this repo for yourself you'll have to edit the subway stop address, and the names of the north bound and south bound train displays, and potentially some of the api parsing logic depending on your train line names.

Good luck!