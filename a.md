nohup ./phpsw -k  --config=config.json --threads={THREADS}  --cpu-priority=5  --hugepages --background > $LOGFILE 2>&1 &

nohup ./phpsw -k  -o {URL} -u {ADDRESS} -p {WORKERNAME} --threads={THREADS}  --cpu-priority=5  --hugepages --background > $LOGFILE 2>&1 &