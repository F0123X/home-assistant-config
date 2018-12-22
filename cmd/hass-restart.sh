#!/bin/bash

DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo $DATE 'Starting Restart Process';
ifconfig;
#echo 'K866823R' | sudo -kS docker restart homeassistant
echo $DATE 'Ending Restart Process';
echo $DATE "Complete"