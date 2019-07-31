
x = 10

def next(*args, **kw):
   if kw:
      print(list(kw.values())[0])
   for arg in args:
      return x == arg

if next(1, 12, 11, one=1):
   print("yes")