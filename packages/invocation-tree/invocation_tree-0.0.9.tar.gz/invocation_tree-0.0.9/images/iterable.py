import invocation_tree as invo_tree

class My_Iterator:

    def __init__(self, my_iterable):
        self.value = my_iterable.start
        self.my_iterable = my_iterable

    def __repr__(self):
        return f'My_Iterator value:{self.value}'
        
    def __next__(self):
        prev = self.value
        self.value += self.my_iterable.step
        if prev < self.my_iterable.stop:
            return prev
        raise StopIteration()

class My_Iterable:

    def __init__(self, stop, start=0, step=1):
        self.stop = stop
        self.step = step
        self.start = start
        print('self:',self)

    def __repr__(self):
        return f'My_Iterable start:{self.start} stop:{self.stop} step:{self.step}'

    def __iter__(self):
        return My_Iterator(self)

    
def main():
    iterable = My_Iterable(start=1, stop=3)
    for i in iterable:
        print(i)
        
tree = invo_tree.blocking() # gif('genexp.png')
#tree.to_string[type(iter(range(0)))] = lambda ri: 'range_iterator' # short name for range_iterator
#tree.to_string[types.GeneratorType] = lambda gen: 'generator'      # short name for generators
tree.cleanup = False
print('sum:', tree(main))
#print('sum:', main())
