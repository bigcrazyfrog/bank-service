class AlreadyExistException(Exception):
    """Already exist user exception."""

    def __init__(self, name: str = "Object", id: str = "ID", *args):
        """Init general info about exception.

        Args:
            name: Name of object class.
            id: ID of instance.

        """
        self.name = name
        self.id = id

        super().__init__(*args)
