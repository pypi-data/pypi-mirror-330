class ClientError(Exception):
    """
    This class extends the built-in Exception class to provide specific
    error handling for client-related issues.
    """

    def __init__(self, text, status):
        """
        Initialize a new ClientError instance.

        Args:
            text (str): A description of the error.
            status (int): The status code associated with the error.

        Returns:
            None
        """
        self.txt = text
        self.status = status

    def __repr__(self):
        """
        Return a string representation of the ClientError.

        Returns:
            str: A formatted string containing the error message and status code.
        """
        return f'ClientError:  {self.txt} \nstatus: [{self.status}]'