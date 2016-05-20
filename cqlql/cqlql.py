#!/usr/bin/env python3

from collections.abc import Mapping, Sequence
import json
import subprocess
import sys

DEMO_JSON = """{"status":"Success","query":"sum((default(0, rate(ts(SUM, some.prod.service, members(some.prod.service), srv/thrift/requests))) / 60))","name":"sum((default(0, rate(ts(SUM, some.prod.service, members(some.prod.service), srv/thrift/requests))) / 60))","timeseries":[{"label":"sum((default(0, rate(ts(SUM, some.prod.service, members(some.prod.service), srv/thrift/requests))) / 60))","extended_label":"sum((default(0, rate(ts(SUM, some.prod.service, members(some.prod.service), srv/thrift/requests))) / 60))","data":[[1453771080,8846.216666666667],[1453771140,9185.21666666667],[1453771200,8889.283333333331],[1453771260,9629.93333333334],[1453771320,8793.766666666668],[1453771380,8996.633333333339],[1453771440,9045.250000000002],[1453771500,8503.81666666667],[1453771560,8791.283333333333],[1453771620,8628.066666666668],[1453771680,8613.133333333328],[1453771740,9045.350000000002],[1453771800,8593.416666666666],[1453771860,9861.566666666666],[1453771920,9087.849999999999],[1453771980,8983.35],[1453772040,8997.550000000001],[1453772100,8568.950000000003],[1453772160,8926.216666666664],[1453772220,8594.566666666668],[1453772280,8724.183333333336],[1453772340,8715.150000000001],[1453772400,8799.75],[1453772460,9130.4],[1453772520,8718.716666666667],[1453772580,8787.033333333335],[1453772640,8744.283333333331],[1453772700,8704.733333333335],[1453772760,9356.833333333334],[1453772820,8757.700000000003],[1453772880,8431.100000000004],[1453772940,8690.533333333335],[1453773000,8597.800000000001],[1453773060,9021.5],[1453773120,8437.199999999997],[1453773180,8508.18333333333],[1453773240,8810.633333333337],[1453773300,8466.633333333331],[1453773360,8721.983333333332],[1453773420,8383.933333333332],[1453773480,8489.383333333339],[1453773540,8756.000000000002],[1453773600,8819.249999999996],[1453773660,10453.216666666662],[1453773720,9389.050000000003],[1453773780,8869.400000000001],[1453773840,9198.516666666663],[1453773900,9148.833333333336],[1453773960,9365.45],[1453774020,8809.300000000001],[1453774080,8844.166666666666],[1453774140,9068.116666666667],[1453774200,8872.050000000003],[1453774260,9314.300000000001],[1453774320,8660.616666666665],[1453774380,9010.283333333335],[1453774440,9214.4],[1453774500,9117.083333333334],[1453774560,9544.566666666671]],"source":{"zones":["smf1"],"services":["some.prod.service"],"sources":["some.prod.service.107","some.prod.service.0","some.prod.service.95","some.prod.service.36","some.prod.service.138","some.prod.service.117","some.prod.service.89","some.prod.service.46","some.prod.service.112","some.prod.service.102","some.prod.service.84","some.prod.service.149","some.prod.service.40","some.prod.service.79","some.prod.service.51","some.prod.service.13","some.prod.service.69","some.prod.service.29","some.prod.service.103","some.prod.service.24","some.prod.service.35","some.prod.service.5","some.prod.service.73","some.prod.service.58","some.prod.service.127","some.prod.service.62","some.prod.service.18","some.prod.service.87","some.prod.service.27","some.prod.service.106","some.prod.service.139","some.prod.service.116","some.prod.service.67","some.prod.service.6","some.prod.service.98","some.prod.service.128","some.prod.service.120","some.prod.service.45","some.prod.service.101","some.prod.service.52","some.prod.service.39","some.prod.service.68","some.prod.service.28","some.prod.service.41","some.prod.service.145","some.prod.service.7","some.prod.service.123","some.prod.service.70","some.prod.service.100","some.prod.service.63","some.prod.service.143","some.prod.service.30","some.prod.service.90","some.prod.service.34","some.prod.service.78","some.prod.service.110","some.prod.service.12","some.prod.service.83","some.prod.service.23","some.prod.service.121","some.prod.service.17","some.prod.service.2","some.prod.service.74","some.prod.service.134","some.prod.service.94","some.prod.service.132","some.prod.service.57","some.prod.service.99","some.prod.service.119","some.prod.service.19","some.prod.service.60","some.prod.service.20","some.prod.service.31","some.prod.service.26","some.prod.service.49","some.prod.service.105","some.prod.service.97","some.prod.service.86","some.prod.service.71","some.prod.service.15","some.prod.service.129","some.prod.service.130","some.prod.service.114","some.prod.service.131","some.prod.service.56","some.prod.service.146","some.prod.service.16","some.prod.service.111","some.prod.service.3","some.prod.service.115","some.prod.service.53","some.prod.service.64","some.prod.service.135","some.prod.service.93","some.prod.service.42","some.prod.service.8","some.prod.service.38","some.prod.service.124","some.prod.service.82","some.prod.service.142","some.prod.service.75","some.prod.service.61","some.prod.service.21","some.prod.service.72","some.prod.service.47","some.prod.service.32","some.prod.service.48","some.prod.service.126","some.prod.service.1","some.prod.service.59","some.prod.service.144","some.prod.service.66","some.prod.service.108","some.prod.service.137","some.prod.service.91","some.prod.service.55","some.prod.service.96","some.prod.service.44","some.prod.service.113","some.prod.service.133","some.prod.service.85","some.prod.service.122","some.prod.service.136","some.prod.service.125","some.prod.service.11","some.prod.service.92","some.prod.service.80","some.prod.service.50","some.prod.service.14","some.prod.service.148","some.prod.service.81","some.prod.service.33","some.prod.service.118","some.prod.service.43","some.prod.service.10","some.prod.service.4","some.prod.service.65","some.prod.service.141","some.prod.service.76","some.prod.service.140","some.prod.service.54","some.prod.service.88","some.prod.service.109","some.prod.service.37","some.prod.service.77","some.prod.service.22","some.prod.service.104","some.prod.service.25","some.prod.service.147","some.prod.service.9"],"metrics":["srv/thrift/requests"],"operations":["reduce","bin","default","rate"]}}]}"""
DEMO_DATA = json.loads(DEMO_JSON)

HELP = """
cqlql - Cuckoo query language query language

usage: cqlql [zone] [cql2 query] (path query)

  zone:         smf1 or atla
  cql2 query:   see manpage for cql2
  path query:   If not defined, this will dump the path structure of the results
                Otherwise, see description below.

Path queries: TODO
"""


S = '/' # Separator character. Dealwithit


def warn(msg):
  print('warning: {}'.format(msg), file=sys.stderr)


def is_list(obj):
  return isinstance(obj, Sequence) and not isinstance(obj, str)


def is_map(obj):
  return isinstance(obj, Mapping)


def get_value(obj, key, default=None):
  try:
    if is_list(obj):
      return obj[int(key)]
    else:
      return obj[key]
  except (KeyError, IndexError, ValueError, TypeError):
    return default


def fetch(obj, path, default=None, lvl=1):
  if obj is default or not path:
    # Yield obj if obj is default (lookup failed) or if the path is empty
    yield obj

  else:
    (key, sep, path) = path.partition(S)
    if sep != S:
      # Separator was not found. Terminating key.
      yield get_value(obj, key, default)

    elif not key:
      # Key is empty, iterate through all elements
      if is_list(obj):
        for i in obj:
          for value in fetch(i, path, default, lvl + 1):
            yield value
    else:
      # Key exists and there's additional path to traverse
      for value in fetch(get_value(obj, key, default), path, default, lvl + 1):
        yield value


def fetch_many(obj, paths, default=None):
  if not paths:
    return []

  # Force generation of all lists for length purposes
  fetched = [tuple(fetch(obj, p, default)) for p in paths]
  lengths = [len(data) for data in fetched]

  if not all(ln == lengths[0] for ln in lengths):
    warn("Patterns generated different sized lists: {}".format(lengths))

  return zip(*fetched)


def cql2(zone, query):
  cmd = ('cql2', '--json', '-z', zone, 'q', query)
  result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
  return json.loads(result.stdout)


def cql2_demo(zone, query):
  return DEMO_DATA


def gen_paths(obj, path_stack=()):
  paths = set()

  if is_list(obj):
    addition = (str(len(obj)), )
    for o in obj:
      paths.update(gen_paths(o, path_stack + addition))

  elif is_map(obj):
    for (key, value) in obj.items():
      paths.update(gen_paths(value, path_stack + (key,)))

  elif path_stack: # It's non-root element in a dict or list
    paths.add(S.join(path_stack))

  return paths


if __name__ == '__main__':

  zone = get_value(sys.argv, 1)
  query = get_value(sys.argv, 2)
  patterns = sys.argv[3:]

  if not zone and query:
    print(HELP, file=sys.stderr)
    sys.exit(1)

  results = cql2(zone, query)

  if not patterns:
    for p in sorted(gen_paths(results)):
      print(p)

  else:
    for i in fetch_many(results, patterns):
      print('\t'.join(str(x) for x in i))
