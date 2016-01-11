#!/usr/bin/env python3
import functools
import os
import sys


HELP = """
Suspenders: Keep your pants on

This is intended to be a small, fast (sub ~100ms) set of utilities to help with
the pants build system. Right now all it does is tab completion.

Usage: suspenders [compgen query] where query must end in ":(subquery)".
  This will generate pants target completions. The subquery is optional and will
  be used as a prefix filter if present.
"""

DEBUG = 'DEBUG' in os.environ

COMMON_FUNCTIONS = (
  'bundle',
  'credentials',
  'Duplicate',
  'exclude',
  'get_buildroot',
  'jar_rules',
  'globs',
  'maven_layout',
  'netrc',
  'rglobs',
  'source_root',
  'zglobs',
)

COMMON_TARGETS = (
  'artifact',
  'artifactory',
  'benchmark',
  'confluence',
  'create_thrift_libraries',
  'hadoop_binary',
  'jar',
  'idl_jar_thrift_library',
  'thrift_jar',
  'jar_library',
  'java_agent',
  'java_antlr_library',
  'java_library',
  'java_protobuf_library',
  'java_ragel_library',
  'java_tests',
  'java_thrift_library',
  'java_wire_library',
  'jaxb_library',
  'junit_tests',
  'jvm_app',
  'jvm_binary',
  'page',
  'python_binary',
  'python_library',
  'python_requirement',
  'python_requirement_library',
  'python_test_suite',
  'python_tests',
  'resources',
  'scala_artifact',
  'scala_jar',
  'scala_library',
  'scalac_plugin',
  'target',
  'wiki_artifact',
)


def dmsg(msg, *args, **kwargs):
  if DEBUG: print('debug: ' + msg.format(*args, **kwargs), file=sys.stderr)


class BuildTarget:
  """ A generic build target, which requires a name """
  def __init__(self, targetType, name, path, args):
    self.type = targetType
    self.name = name
    self.args = args
    self.path = path
    self.id = ':'.join((self.path, self.name))

  def __str__(self):
    return "BuildTarget({}: {})".format(self.type, self.id)

  def __repr__(self):
    return 'BuildTarget({}: id={}, args={})'.format(self.type, self.id, self.args)


class BuildFunction:
  """ Global function call in a build file """
  def __init__(self, name):
    self.name = name
    self.str = self.type + "(...)"

  def __call__(self, *args, **kwargs):
    dmsg("Called {}({}, {})", self.name, args, kwargs)
    return self.str

  def __getattr__(self, name):
    return "{}.{}".format(self.name, name)

  def __str__(self):
    return self.str


class PantsEnvironment:
  """Environment for parsing BUILD files and working with pants targets"""

  def __init__(self, targets=COMMON_TARGETS, functions=COMMON_FUNCTIONS):
    self._target_collector = None
    self._current_build_path = None
    self.env = {}
    self.env.update({t: functools.partial(self._new_target, t) for t in targets})
    self.env.update({f: BuildFunction(f) for f in functions})

  def _new_target(self, targetType, *args, **kwargs):
    """Create a new target and add it to the target collector"""
    for i, arg in enumerate(args):
      kwargs[i] = arg
    name = kwargs.get('name', 'NO-TARGET-NAME')
    dmsg('Creating target type={} name={}', targetType, name)
    target = BuildTarget(targetType, name, self._current_build_path, kwargs)
    self._target_collector.append(target)

  def parse(self, buildpath):
    try:
      self._current_build_path = buildpath.replace('/BUILD', '')
      self._target_collector = []
      self._new_target("all", name=':')

      with open(buildpath, 'r') as f:
        dmsg("Parsing {}", buildpath)
        compiled = compile(f.read(), buildpath, 'exec')
        exec(compiled, self.env.copy())
        return self._target_collector

    finally:
      self._target_collector = None
      self._current_build_path = None


if __name__ == "__main__":
  def exit_next_compgen():
    """Exit and tell bash to use default completion"""
    sys.exit(124)

  def compgen(query):
    (build, subquery) = query.split(':', maxsplit=1)
    build_file = build + '/BUILD'
    if not os.path.isfile(build_file):
      dmsg("{} does not exist, so there are no completions.", build_file)
      # Not a failure, there's just no build file there
      exit_next_compgen()

    dmsg("compgen {} : {}", build, subquery)
    pants = PantsEnvironment()
    results = pants.parse(build_file)
    dmsg("results:\n{}\n", results)
    print('\n'.join(r.id for r in results if r.name.startswith(subquery)))

  if len(sys.argv) >= 2 and ':' in sys.argv[1]:
    compgen(sys.argv[1])
  else:
    print(HELP.strip(), file=sys.stderr)
    sys.exit(1)
