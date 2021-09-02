from abc import ABC, abstractmethod


class BaseBuilder(ABC):
    """
    Builder interface that specifies methods that Builder objects
    must adhere to.
    """

    @abstractmethod
    def build(self, *args, **kwargs):
        raise NotImplementedError
