from ncompasslib.immutable import Immutable
from abc import ABC

class Trait(Immutable, ABC):
    def __new__(cls, *args, **kwargs):
        # Pass no arguments to Immutable.__new__
        return Immutable.__new__(cls)
