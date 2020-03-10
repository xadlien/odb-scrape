import argparse
from collections import namedtuple
import datetime
import json
import requests
import sys

Devotion = namedtuple("Devotion", ["date", "title", "verses", "content"])


def main():
    #define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, help="date start in yyyy-mm-dd format")
    parser.add_argument("--end", required=True, help="date inclusive end in yyyy-mm-dd format")
    parser.add_argument("-f", "--file", required=False, help="json file to create with scraped data")

    #parse arguments
    args = parser.parse_args()

    #set file handle to file or stdout
    if args.file:
        f = open(args.file, "w")
    else:
        f = sys.stdout

    #call generator to get json data and print/write to file
    for dv in get_devotionals(args.start, args.end):
        f.write(json.dumps(dv))


def get_devotionals(start_date, end_date):
    
    #define boundaries
    start_year, start_month, start_day = map(int, start_date.split('-'))
    end_year, end_month, end_day = map(int, end_date.split('-'))
    start = datetime.date(start_year, start_month, start_day)
    end = datetime.date(end_year, end_month, end_day)

    #define delta
    day = datetime.timedelta(days=1)

    #pull the posts
    headers = {'Accept': 'application/json'}
    url = "https://odb.org/wp-json/wp/v2/posts?after=" + str(start - day) + "T23:59:59.000Z&before=" + str(end + day) + "T00:00:00.000Z"
    r = requests.get(url, headers=headers, verify=True)

    #return data
    return r.json()


main()

#headers = {'Accept': 'application/json', 'Referer': 'https://odb.org/2020/02/08'}
#url = "https://odb.org/wp-json/wp/v2/posts?after=2020-02-07T23:59:59.000Z&before=2020-02-09T00:00:00.000Z"
#print(json.dumps(r.json(), indent=4, sort_keys=True))
