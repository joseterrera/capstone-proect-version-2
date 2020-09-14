
print('hello') #?

def pick(keys,dict):
  return { your_key: dict[your_key] for your_key in keys }



things = [{
  'name': 'bob',
  'employee': True
},
{
  'name': 'peter',
  'employee': False
}]



for i in map(lambda  x: x['name'], things):
  print(i) #?