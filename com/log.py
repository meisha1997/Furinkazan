import sys

def _print(*args, **kwargs):
    sep = kwargs.get('sep', '-')
    out = kwargs.get('file', sys.stdout)
    end = kwargs.get('end', '\n')
    out.write(sep.join(args) + end)

print = _print