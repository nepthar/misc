# Stuff I didn't use but don't want to get rid of


class ParseContext:

  def __init__(self, path, env={}):
    self.path = os.path.abspath(path)
    self.compiled = None
    self.globals = env.copy()

  def __enter__(self):
    with open(self.path, 'r') as f:
      self.compiled = compile(f.read(), self.path, 'exec')
    return self

  def parse(self):
    if not self.compiled:
      raise RuntimeError
    exec(self.compiled, self.globals)

  def __exit__(self, type, value, traceback):
    pass



# In class PantsEnvironment
@staticmethod
def find_pants_root(path):
  abspath = os.path.abspath(path)

  path_pieces = abspath.split('/')
  while path_pieces:
    head = os.path.join('/', *path_pieces, 'pants')
    if os.path.isfile(head):
      return head.replace('/pants', '')
    path_pieces.pop()

  return None

@staticmethod
def for_path(path):
  pants_path = PantsEnvironment.find_pants_root(path)
  if not pants_path:
    raise ValueError("No pants in {}".format(path))
  return PantsEnvironment(pants_path)