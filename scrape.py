from datetime import datetime as dt, timedelta
import argparse
import gzip
import glob
import os
import shutil
import time
import requests

# URL endpoint for BitMex data
endpoint = 'https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/trade/{}.csv.gz'

def scrape(year, date, end, symbol):
    end_date = min(dt(year, 12, 31), dt.today() - timedelta(days=1))
    while date <= end_date and date <= end:
        date_str = date.strftime('%Y%m%d')
        print(f"Processing {date_str}...")
        count = 0
        while True:
            r = requests.get(endpoint.format(date_str))
            if r.status_code == 200:
                break
            else:
                count += 1
                if count == 10:
                    r.raise_for_status()
                print(f"Error processing {date_str} - {r.status_code}, trying again")
                time.sleep(10)

        # Write the downloaded gzip file
        temp_gzip_path = f"{date_str}.gz"
        with open(temp_gzip_path, 'wb') as fp:
            fp.write(r.content)

        # Extract the content and filter for the symbol
        temp_csv_path = f"{date_str}.csv"
        with gzip.open(temp_gzip_path, 'rt') as fp_in, open(temp_csv_path, 'w') as fp_out:
            header = fp_in.readline()
            fp_out.write(header)  # Write header to output file
            for line in fp_in:
                if symbol in line:
                    fp_out.write(line)

        # Clean up the temporary gzip file
        os.remove(temp_gzip_path)

        date += timedelta(days=1)

def merge(year):
    print(f"Generating CSV for {year}")
    files = sorted(glob.glob(f"{year}*.csv"))
    first = True
    with open(f"{year}.csv", 'w') as out:
        for f in files:
            with open(f, 'r') as fp:
                if first:
                    out.write(fp.readline())  # Write header once
                    first = False
                else:
                    fp.readline()  # Skip header
                shutil.copyfileobj(fp, out)
    # Cleanup
    for f in files:
        os.unlink(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BitMex historical data scraper. Scrapes files into single year CSVs')
    parser.add_argument('--start', default="20141122", help='Start date in YYYYMMDD format. Default is 2014-11-22, the earliest data date for BitMex')
    parser.add_argument('--end', default=None, help='End date in YYYYMMDD format. Default is yesterday')
    parser.add_argument('--symbol', default="XBTUSD", help='Symbol to filter by, e.g., XBTUSD. Default is XBTUSD')
    args = parser.parse_args()

    start = dt.strptime(args.start, '%Y%m%d')
    end = dt.strptime(args.end, '%Y%m%d') if args.end else dt.utcnow()

    years = list(range(start.year, end.year + 1))
    starts = [dt(year, 1, 1) for year in years]
    starts[0] = start

    for year, start in zip(years, starts):
        scrape(year, start, end, args.symbol)
        merge(year)
