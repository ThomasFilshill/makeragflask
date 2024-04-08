import argparse
from searchDBAndQuery import query

parser = argparse.ArgumentParser()
parser.add_argument("query_text", type=str, help="The query text.")
args = parser.parse_args()
query_text = args.query_text

print(query(query_text))
