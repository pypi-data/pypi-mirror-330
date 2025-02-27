def mutate(func):
    """Decorator to make a method mutable by temporarily allowing attribute changes"""
    def wrapper(self, *args, **kwargs):
        # Store current state of attributes
        stored_attrs = self.attrWasSet.copy()
        # Clear attribute list to allow changes
        self.attrWasSet.clear()
        
        try:
            # Execute the function
            result = func(self, *args, **kwargs)
            # Restore attribute protection
            self.attrWasSet = stored_attrs
            return result
        except Exception as e:
            # Restore attribute protection even if function fails
            self.attrWasSet = stored_attrs
            raise e
            
    return wrapper

class Immutable(object):
    def __init__(self):
        self.attrWasSet = []

    def __setattr__(self, name, value):
        if name == 'attrWasSet':
            super().__setattr__(name, value)
        elif name in self.attrWasSet:
            raise RuntimeError('Cannot change state once created')
        else:
            self.attrWasSet.append(name)
            super().__setattr__(name, value)
