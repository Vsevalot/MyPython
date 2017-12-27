def add_wrapping(item): # takes function
    def wrapped_item(x): # takes args
        return 'a wrapped up box of {}'.format(str(item(x)))
    return wrapped_item

@add_wrapping
def new_gpu(x):
    return 'a new Tesla P{} GPU!'.format(x)

print(new_gpu(19))