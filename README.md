# Our Daily Bread Scrape
## Description
This program was created to pull in Our Daily Bread devotional information. 
## Usage
--start DATE, the format is YYYY-mm-dd
--end DATE, the format is YYYY-mm-dd
-f FILE, this is the output file for the json data 
-p CONFIG, specifies the config file for postgres
## Example
`python3 odb-scrape.py --start 2021-01-01 --end 2021-06-29 -f file.json  `
## Building
```
make build-deb-setup
make build-deb
```
## Installing
`make install-deb`