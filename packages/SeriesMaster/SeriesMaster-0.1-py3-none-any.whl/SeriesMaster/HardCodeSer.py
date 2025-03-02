
class HardCodeSer():
    """
    HardCodeSer
    Takes any Series

    Attributes:
        ser (list[any]): The user-defined Series.

    Methods:
    

        Append(append: any) -> str:
            Appends an anything to the Series and returns a success message.
            

        Remove(r: any) -> None:
            Removes the given anything from the Series if it exists.
            Raises:
                ValueError: If the number is not in the Series.
   

        IsInSer(char: any) -> bool:
            Checks if a given char exists in the Series.

        __repr__() -> str:
            Returns a string representation of the Series.
        
    Example Usage:
        >>> hc = HardCodeSer([3, 5, 7, 9])
        >>> hc.Append(11)
        'Successfully appended'
        >>> hc.Remove(5)
        >>> hc.IsInSer(7)
        True
    """

    def __init__(self, series):
        """
        Initializes the HardCodeSer instance with a user-defined sequence.

        Args:
            Series (list[int] or tuple[int]): The custom Series to be stored.

        Raises:
            ValueError: If the provided Series is not a list or tuple.
        """
        if not isinstance(series, (list, tuple)):
            raise ValueError('The provided Series is not a list/tuple')
        
        self.ser = list(series)

    def __repr__(self):
        """
        Returns a string representation of the Series.

        Returns:
            str: A readable representation of the Series.
        """
        return f"HardCodeSer({self.ser})"
    
    def Append(self, append):
        """
        Appends an integer to the Series.

        Args:
            append (int): The number to be added to the Series.

        Returns:
            str: A success message.
        """
        if not isinstance(append, int):
            raise TypeError('Provided append is not an integer')
        
        self.ser.append(append)
        return 'Successfully appended'
    
    def Remove(self, r):
        """
        Removes a number from the Series if it exists.

        Args:
            r (int): The number to remove.

        Raises:
            ValueError: If the number is not in the Series.
        """
        if r not in self.ser:
            raise ValueError(f"{r} is not in the Series")
        
        self.ser.remove(r)

    def IsInSer(self, num):
        """
        Checks if a number exists in the Series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the Series, False otherwise.
        """
        return num in self.ser
