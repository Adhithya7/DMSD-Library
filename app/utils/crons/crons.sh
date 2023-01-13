#!/bin/bash
crontab -l > mycrons
echo "00 18 * * * python3 /home/adhithya7/Work/DMSD-Library/app/crons/crons.sh" >> mycrons
crontab mycrons
rm mycrons