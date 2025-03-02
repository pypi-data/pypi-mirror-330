import warnings
import matplotlib.pyplot as plt  # type: ignore

class RepeatingPatternSer:
    """
    A class to create a repeating pattern series.

    This class allows you to create a list where the same initial value (first_row)
    is repeated for a given number of rows.

    Attributes:
        a (any): The first row, which is repeated throughout the series.
        n (int): The total number of rows in the series.
        ser (list): The generated series with repeated values.

    Methods:
        FullSer(): Returns the full series.
    """

    def __init__(self, first_row, number_of_rows):
        """
        Initializes the RepeatingPatternSer with a starting value and number of rows.

        Args:
            first_row (any): The value to be repeated in each row.
            number_of_rows (int): The number of times the first_row should be repeated.
        """
        self.a = first_row
        self.n = number_of_rows
        self.ser = list([first_row] * self.n)

    def __repr__(self):
        """
        Returns a string representation of the class.

        Returns:
            str: A description of the class.
        """
        return "Add a series of literally anything"

    def FullSer(self):
        """
        Returns the full repeating series.

        Returns:
            list: A list containing `number_of_rows` copies of `first_row`.
        """
        return self.ser


class GrowingPatternSer(RepeatingPatternSer):
    """
    A class to create a growing pattern series.

    This class generates a numerical sequence where each term grows by a common ratio (geometric progression).

    Attributes:
        d (int, optional): The common difference for an arithmetic progression. Default is 0.
        r (int, optional): The common ratio for a geometric progression. Default is 1.
        a (int/float): The first term of the sequence.
        n (int): The total number of terms in the series.
        ser (list): The generated growing series.

    Methods:
        FullSer(): Returns the full series.
    """

    def __init__(self, first_row, number_of_rows, r):
        """
        Initializes the GrowingPatternSer with a first term, number of terms, and a rule for progression.

        Args:
            first_row (int/float): The starting value of the series.
            number_of_rows (int): The number of terms to generate.
            d (int, optional): The common difference for arithmetic progression. Default is 0.
            r (int, optional): The common ratio for geometric progression. Default is 1.

        Raises:
            ValueError: If both d and r are defined or both are left undefined.
        """
        

        self.r = r
        self.a = first_row
        self.n = number_of_rows
        self.ser = [self.a]
        # Generate the series
        for _ in range(self.n - 1):
            tempser = []
            for i in self.ser[_]:
                tempser.append(i*r)
            
            self.ser.append(tempser)


    def __repr__(self):
        """
        Returns a string representation of the GrowingPatternSer class.

        Returns:
            str: A description of the series.
        """
        return f"GrowingPatternSer({self.ser})"

    def FullSer(self):
        """
        Returns the full growing series.

        Returns:
            list: A list containing the generated series.
        """
        return self.ser

