#!/bin/bash

crontab -l > testcron

echo "0 9 * * 1-5 /home/ryurkov/repo/PY/PY/mts/mtsscript/run.py" >> testcron

crontab testcron
