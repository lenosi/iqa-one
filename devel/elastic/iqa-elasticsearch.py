from argparse import ArgumentParser
from subprocess import check_output
from time import sleep

from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections, Search

# parse arguments

parser = ArgumentParser()

# Output configuration
parser.add_argument('-p', '--print', help='print logs to stdout', action='store_true')

group = parser.add_mutually_exclusive_group()
group.add_argument('-o', '--output-once', help='output once and exit', action='store_true')
group.add_argument('-r', '--refresh', type=int, nargs='?', default=5,
                   help='refresh interval in seconds during live output, default is 5')

# Log filtering
parser.add_argument('-k', '--keyword', type=str, help='output only logs containing this keyword')
parser.add_argument('-n', '--hostname', type=str, help='retrieve logs only from a specific hostname')
parser.add_argument('-b', '--beat', type=str, nargs='?', default='filebeat', choices=['filebeat', 'journalbeat'],
                    help='which beat to retrieve logs from (filebeat / journalbeat), default is filebeat')

# Filter time and quantity
parser.add_argument('-s', '--start', type=str, nargs='?', default='now-1d',
                    help=
                    '''Start of the period for which results are displayed, default is 1 day ago.
                    Format can be either a timestamp in the ISO datetime format: YYYY-MM-DDTHH:MM:SS,
                    for example 1970-01-01T00:00:00 (T is a date/time separator), or 'now'.
                    You can also add or subtract a time period from 'now' or a date string using
                    this format: [+|-]n[y|M|w|d|h|m|s], where n is the number of time units you
                    want to add or subtract. Time units are listed from longest to shortest beginning
                    with 'y' (year) and ending with 's' (second). This must be separated from a timestamp by ||.
                    Examples: 'now-1h' - one hour ago
                    '2020-01-01T00:00:00||-1y' - one year before the start of 2020''')
parser.add_argument('-e', '--end', type=str, nargs='?', default='now',
                    help=
                    '''End of period for which results are displayed, default is now.
                    Time format is the same as for 'start' ''')
parser.add_argument('-m', '--max', type=int,
                    help='''maximum number of results to be displayed - maximum number which Elasticsearch allows
                        is 10 000, Elasticsearch's default is 10''')

args = parser.parse_args()

# check argument collisions

if args.max and not args.output_once:
    parser.error('\'max\' option only valid with \'output_once\' option')

# obtain necessary info from received arguments

index_str: str = args.beat + '-*'

ip: str = check_output(
    ['docker', 'inspect', '-f', '"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"',
     'elasticsearch'], encoding='utf-8').strip('\n\"')

es_addr: str = ip + ':9200'
print(es_addr)

# establish a connection and create an Elastic search

connections.create_connection(hosts=[es_addr])

client = Elasticsearch()

# construct search object

s = Search(using=client, index=index_str)

if args.output_once:
    s = s.sort({'@timestamp': {"order": "desc"}}) \
        .filter('range', **{'@timestamp': {'gte': args.start, 'lte': args.end}})

    if args.max:
        s = s[:args.max]
else:
    timestamp_s = Search(using=client, index=index_str) \
        .sort({'@timestamp': {"order": "desc"}})
    timestamp_s = timestamp_s[0]

    response = timestamp_s.execute(ignore_cache=True)

    if s.count() != 0:
        timestamp = response[0]['@timestamp']
    else:
        timestamp = 'now'

    del response, timestamp_s

    s = s.sort({'@timestamp': {"order": "asc"}}) \
        .filter('range', **{'@timestamp': {'gt': timestamp}})

if args.keyword:
    msg = '.*' + args.keyword.lower() + '.*'
    s = s.query('regexp', message=msg)

if args.hostname:
    s = s.query('match', host__name=args.hostname)

# search and output results once
if args.output_once:
    response = s.execute(ignore_cache=True)

    if s.count() == 0:
        print('No results found')
    else:
        print('Total hits:', s.count(), '\n')

    for hit in response:
        if args.print:
            print(hit['@timestamp'] + ' in ' + hit['log']['file']['path'] + ':', hit['message'], '', sep='\n')

# output results in real time as they arrive
else:
    while True:
        sleep(args.refresh)

        response = s.execute(ignore_cache=True)

        for hit in response:
            if args.print:
                print(hit['@timestamp'] + ' in ' + hit['log']['file']['path'] + ':', hit['message'], '', sep='\n')
            timestamp = hit['@timestamp']
