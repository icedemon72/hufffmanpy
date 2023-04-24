class Node():
  def __init__(self, char, occurrences, left = None, right = None):
    self.left = left
    self.right = right
    self.char = char
    self.occurrences = occurrences
    
  def order_tree_by_root(self, characters):
    array = []
    result = ''
    for character in characters:
      self.order_tree_util(self, character[0], array, result)
    return array
    
  def order_tree_util(self, root, character, array, result):
    
    if (root.right is None):
      array.append(result)
      result = ''
      pass
    
    if root is None:
      pass
            
    if(root.left is not None):
      if(character in root.left.char):
        result += '0'
        self.order_tree_util(root.left, character, array, result)
      elif (character in root.right.char):
        result += '1'
        self.order_tree_util(root.right, character, array, result)

    pass