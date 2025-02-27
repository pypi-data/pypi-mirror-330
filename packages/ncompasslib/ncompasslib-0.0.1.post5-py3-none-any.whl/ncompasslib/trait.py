from ncompasslib.immutable import Immutable
from abc import ABC

class Trait(Immutable, ABC):
    def __init__(self):
        super().__init__()
