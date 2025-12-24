class Base:
    """
    The base class for all classes in pymodd.
    The to_dict function should be implemented to return a python dict in the Modd JSON schema
    """

    def to_dict(self):
        raise NotImplementedError("to_dict method not implemented")
