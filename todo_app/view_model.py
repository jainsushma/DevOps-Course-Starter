class ViewModel:
    
 def __init__(self, items):
    self._items = items
 
 @property
 def items(self):
    return self._items

@property
def todo_items(self):
   items = []
   for item in self._items:
      print(item.status)
      # if item.status == 'to-do':
      #       items.append(item)
   return items

@property
def doing_items(self):
   items = []
   for item in self._items:
      if item.status == 'doing':
            items.append(item)
   return items

@property
def done_items(self):
   items = []
   for item in self._items:
      if item.status == 'done':
            items.append(item)
   return items