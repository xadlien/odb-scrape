import argparse
from collections import namedtuple
import datetime
import json
import psycopg2
import requests
import sys

Devotion = namedtuple("Devotion", ["date", "title", "verses", "content"])


def main():
    #define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, help="date start in yyyy-mm-dd format")
    parser.add_argument("--end", required=True, help="date inclusive end in yyyy-mm-dd format")
    parser.add_argument("-f", "--file", required=False, help="json file to create with scraped data")
    parser.add_argument("-p", "--postgres", required=False, help="push to postgres using provided config file")

    #parse arguments
    args = parser.parse_args()

    #set file handle to file or stdout
    if args.file:
        f = open(args.file, "w")
    else:
        f = sys.stdout

    #call generator to get json data and print/write to file
    devos = get_devotionals(args.start, args.end)
    for dv in devos:
        f.write(json.dumps(dv))

    if args.postgres:
        config = json.load(open(args.postgres, 'r'))
        # get postgres config
        pg_host = config["host"]
        pg_port = config["port"]
        pg_user = config["username"]
        pg_pass = config["password"]
        pg_db = config["database"]

        # connect to postgres
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            database=pg_db,
            user=pg_user,
            password=pg_pass
        )
        cur = conn.cursor()

        # ensure table exists
        query = "create table if not exists devotionals (" + \
            "id int constraint firstkey primary key," +\
            "title varchar," + \
            "content varchar);"
        cur.execute(query)
        conn.commit()

        # iterate and generate records
        for dv in devos:
            id = dv['id']
            title = dv['title']['rendered']
            content = dv['content']['rendered']
            query = f"select count(*) from devotionals where id = {id};"
            cur.execute(query)
            check_val = cur.fetchall()[0][0]
            # insert value if it doesn't exist
            if check_val == 0:
                query = f"insert into devotionals values ({id},'{title}','{content}');"
                cur.execute(query) 
                conn.commit()

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

if __name__ == "__main__":
    main()

#headers = {'Accept': 'application/json', 'Referer': 'https://odb.org/2020/02/08'}
#url = "https://odb.org/wp-json/wp/v2/posts?after=2020-02-07T23:59:59.000Z&before=2020-02-09T00:00:00.000Z"
#print(json.dumps(r.json(), indent=4, sort_keys=True))
