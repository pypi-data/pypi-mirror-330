"""FibSer:
        Represents and manipulates a **Fibonacci MathSer Series**.

        Attributes:
            n (int): The number of terms in the Fibonacci MathSer Series.
            ser (list of int): The full Fibonacci MathSer Series stored as a list.

        Methods:
            __init__(number_of_terms):
                Initializes a Fibonacci MathSer Series with the given number of terms.

            FullSer() -> list[int]:
                Returns the entire MathSer Series.

            LastTerm() -> int:
                Returns the last term of the MathSer Series.

            Sum() -> int:
                Returns the sum of all terms in the Fibonacci MathSer Series.

            IsInSer(num) -> bool:
                Checks if a number exists in the Fibonacci MathSer Series.

            PrimeNumbers() -> list[int]:
                Returns a list of prime numbers present in the Fibonacci MathSer Series.

            IndexSubsetSum(start, end) -> int:
                Returns the sum of a subset of the Fibonacci MathSer Series.

            GetEven() -> list[int]:
                Returns a list of all even numbers in the Fibonacci MathSer Series.

            GetOdd() -> list[int]:
                Returns a list of all odd numbers in the Fibonacci MathSer Series.

            Median() -> float:
                Returns the median of the Fibonacci MathSer Series.

            MulSeries(x) -> list[int]:
                Returns a new MathSer Series with each term multiplied by x.

            DivSeries(x) -> list[float]:
                Returns a new MathSer Series with each term divided by x.

            LCM() -> int:
                Returns the least common multiple of all terms in the Fibonacci MathSer Series.

            Plot():
                Plots the Fibonacci MathSer Series using matplotlib.

            SubPlot(start_index, end_index):
                Plots a subset of the Fibonacci MathSer Series.

            Help():
                Displays help documentation for the class.

    
    TribSer (Tribonacci MathSer Series)

        This class generates a Tribonacci MathSer Series and provides various methods
        to analyze and manipulate it.

        Attributes
        ----------
        n : int
            The number of terms in the MathSer Series.
        ser : list
            The Tribonacci sequence up to `n` terms.

        Methods
        -------
        FullSer() : list
            Returns the complete Tribonacci MathSer Series.
        LastTerm() : int
            Returns the last term of the Tribonacci MathSer Series.
        IsInSer(num: int) : bool
            Checks if a given number is present in the Tribonacci MathSer Series.
        IndexSubsetSum(start_idx: int, end_idx: int) : int
            Returns the sum of Tribonacci numbers between two indices.
        PrimeNumbers() : list
            Returns a list of prime numbers found in the MathSer Series.
        Plot() : None
            Plots the Tribonacci MathSer Series.
        SubPlot(start_index: int, end_index: int) : None
            Plots a subset of the Tribonacci MathSer Series.
        GetEven() : list
            Returns a list of all even Tribonacci numbers.
        GetOdd() : list
            Returns a list of all odd Tribonacci numbers.
        Median() : float
            Returns the median value of the MathSer Series.
        MulSeries(x) : list
            Returns a new MathSer Series with each term multiplied by `x`.
        DivSeries(x) : list
            Returns a new MathSer Series with each term divided by `x`.
        AddSer(x) : list
            Returns a new MathSer Series with each term added by `x`.
        SubSer(x) : list
            Returns a new MathSer Series with each term subtracted by `x`.
        LCM() : int
            Returns the Least Common Multiple (LCM) of the MathSer Series.
        Help() : None
            Displays help documentation for the TribSer class.

        Examples
        --------
        >>> trib = TribSer(10)
        >>> trib.FullSer()
        [1, 1, 2, 4, 7, 13, 24, 44, 81, 149]
        >>> trib.LastTerm()
        149
        """

import warnings
import matplotlib.pyplot as plt # type: ignore
from math import gcd
from functools import reduce

class FibSer:
    """
    FibSer (Fibonacci MathSer Series)

    This class generates a Fibonacci MathSer Series and provides various methods to analyze and manipulate it.

    Attributes:
        n (int): The number of terms in the MathSer Series.
        ser (list): The Fibonacci sequence up to `n` terms.

    Methods:
        FullSer() -> list:
            Returns the complete Fibonacci MathSer Series.

        LastTerm() -> int:
            Returns the last term of the Fibonacci MathSer Series.

        IsInSer(num: int) -> bool:
            Checks if a given number is present in the Fibonacci MathSer Series.

        IndexSubsetSum(start_idx: int, end_idx: int) -> int:
            Returns the sum of Fibonacci numbers between two indices.

        PrimeNumbers() -> list:
            Returns a list of prime numbers found in the MathSer Series.

        Plot() -> None:
            Plots the Fibonacci MathSer Series.

        SubPlot(start_index: int, end_index: int) -> None:
            Plots a subset of the Fibonacci MathSer Series.

        GetEven() -> list:
            Returns a list of all even Fibonacci numbers.

        GetOdd() -> list:
            Returns a list of all odd Fibonacci numbers.

        Median() -> float:
            Returns the median value of the MathSer Series.

        MulSeries(x) -> list:
            Returns a new MathSer Series with each term multiplied by `x`.

        DivSeries(x) -> list:
            Returns a new MathSer Series with each term divided by `x`.

        AddSer(x) -> list
            Returns a new MathSer Series with each term added by `x`. 

        SubSer(x) -> list
            Returns a new MathSer Series with each term subtracted by `x`.

        LCM() -> int:
            Returns the Least Common Multiple (LCM) of the MathSer Series.

        Help() -> None:
            Displays help documentation for the FibSer class.
    """

    def __init__(self, number_of_terms):
        """
        Initializes the Fibonacci MathSer Series with the given number of terms.

        Args:
            number_of_terms (int): The number of terms in the MathSer Series.

        Raises:
            ValueError: If number_of_terms is less than 2.
        """
        if number_of_terms < 2:
            raise ValueError("Number of terms must be at least 2.")

        self.n = number_of_terms
        self.ser = [1, 1]

        for _ in range(self.n - 2):
            self.ser.append(self.ser[-1] + self.ser[-2])

    def __repr__(self):
        return (
            "FibSer is short for Fibonacci MathSer Series. "
            "The methods defined here are FullSer(), LastTerm(), Sum(), and more via Help()."
        )

    def FullSer(self):
        """Returns the full Fibonacci MathSer Series."""
        return self.ser

    def LastTerm(self):
        """Returns the last term of the Fibonacci MathSer Series."""
        return self.ser[-1]

    def IsInSer(self, num):
        """
        Checks if a number is in the Fibonacci MathSer Series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the MathSer Series, False otherwise.
        """
        a, b = 1, 1
        while a <= num:
            if a == num:
                return True
            a, b = b, a + b
        return False

    def IndexSubsetSum(self, start_idx, end_idx) :
        """
        Returns the sum of Fibonacci numbers between two indices.

        Args:
            start_idx (int): The starting index (0-based).
            end_idx (int): The ending index (0-based).

        Returns:
            int: The sum of the subset.

        Raises:
            IndexError: If indices are out of bounds or invalid.
        """
        if not (0 <= start_idx < self.n and 0 <= end_idx < self.n and start_idx <= end_idx):
            raise IndexError("Invalid index range.")

        return sum(self.ser[start_idx:end_idx + 1])

    def PrimeNumbers(self):
        """
        Returns all prime numbers in the Fibonacci MathSer Series.

        Returns:
            list: A list of prime numbers.
        """
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True

        return [num for num in self.ser if is_prime(num)]

    def Plot(self):
        """Plots the Fibonacci MathSer Series using matplotlib."""
        plt.plot(range(self.n), self.ser, marker="o", color="red")
        plt.title("Fibonacci MathSer Series")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.show()

    def SubPlot(self, start_index, end_index):
        """
        Plots a subset of the Fibonacci MathSer Series.

        Args:
            start_index (int): The starting index (0-based).
            end_index (int): The ending index (0-based).
        """
        if not (0 <= start_index < self.n and 0 <= end_index < self.n and start_index <= end_index):
            raise IndexError("Invalid index range.")

        subser = self.ser[start_index:end_index + 1]
        plt.plot(range(start_index, end_index + 1), subser, marker="o", color="blue")
        plt.title("Subset of Fibonacci MathSer Series")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.show()

    def GetEven(self):
        """Returns a list of all even numbers in the Fibonacci MathSer Series."""
        return [num for num in self.ser if num % 2 == 0]

    def GetOdd(self):
        """Returns a list of all odd numbers in the Fibonacci MathSer Series."""
        return [num for num in self.ser if num % 2 != 0]

    def Median(self):
        """
        Returns the median of the Fibonacci MathSer Series.

        Returns:
            float: The median value.
        """
        sorted_ser = sorted(self.ser)
        mid = len(sorted_ser) // 2
        if len(sorted_ser) % 2 == 1:
            return sorted_ser[mid]
        return (sorted_ser[mid - 1] + sorted_ser[mid]) / 2

    def MulSeries(self, x):
        """
        Returns a new MathSer Series with each term multiplied by x.

        Args:
            x (int): The multiplier.

        Returns:
            list of int: The multiplied MathSer Series.
        Raises:
            TypeError: If the input is not an int.
        """
        if type(x) != int and type(x) != float:
            raise TypeError('The provided input is not an int/float')
        return [i * x for i in self.ser]

    def DivSeries(self, x):
        """
        Returns a new MathSer Series with each term divided by x.

        Args:
            x (int): The divisor.

        Returns:
            list of float: The divided MathSer Series.

        Raises:
            ValueError: If divisor is 0
            TypeError: If the input is not an int.
        """
        if type(x) != int and type(x) != float:
            raise TypeError('The provided input is not an int/float')
        if x == 0:
            raise ValueError('Cannot divide by 0')
        return [i / x for i in self.ser]

        """
        Returns a new MathSer Series with each term divided by x.

        Args:
            x (int): The divisor.

        Returns:
            list: The divided MathSer Series.

        Raises:
            ValueError: If x is 0.
        """
        if x == 0:
            raise ValueError("Cannot divide by 0.")
        return [num / x for num in self.ser]
    
    def AddSer(self,x):
            """
            Add value to the MathSer Series. This is a temperory change.

            Args:
                x (int): The addend

            Returns:
                list: The added MathSer Series

            Raises:
                TypeError: If the input is not an int.
            """
            if type(x) != int and type(x) != float:
                raise TypeError('The provided input is not an int/float')
            new_ser = []

            for i in range(len(self.ser)):
                new_ser.append(self.ser[i]+x)

            return new_ser
    
    def SubSer(self,x):
        """
        Subtract value to the MathSer Series. This is a temperory change.

        Args:
            x (int): The minuend

        Returns:
            list: The subtracted MathSer Series
        Raises:
            TypeError: If the input is not an int.
        """
        if type(x) != int and type(x) != float:
            raise TypeError('The provided input is not an int/float')

        new_ser = []

        for i in range(len(self.ser)):
            new_ser.append(self.ser[i]-x)

        return new_ser


    def LCM(self):
        """
        Returns the Least Common Multiple (LCM) of the Fibonacci MathSer Series.

        Returns:
            int: The LCM of the MathSer Series.
        """
        return reduce(lambda x, y: (x * y) // gcd(x, y), self.ser)

    def __len__(self):
        """Returns the length of the MathSer Series."""
        return len(self.ser)

    def Help(self):
        """Displays help documentation for the FibSer class."""
        return help(FibSer)

class TribSer(FibSer):

    """

    TribSer (Tribonacci MathSer Series)

    This class generates a Trionacci MathSer Series and provides various methods to analyze and manipulate it.

    Attributes:
        n (int): The number of terms in the MathSer Series.
        ser (list): The Fibonacci sequence up to `n` terms.

    Methods:
        FullSer() -> list:
            Returns the complete Fibonacci MathSer Series.

        LastTerm() -> int:
            Returns the last term of the Fibonacci MathSer Series.

        IsInSer(num: int) -> bool:
            Checks if a given number is present in the Fibonacci MathSer Series.

        IndexSubsetSum(start_idx: int, end_idx: int) -> int:
            Returns the sum of Fibonacci numbers between two indices.

        PrimeNumbers() -> list:
            Returns a list of prime numbers found in the MathSer Series.

        Plot() -> None:
            Plots the Fibonacci MathSer Series.

        SubPlot(start_index: int, end_index: int) -> None:
            Plots a subset of the Fibonacci MathSer Series.

        GetEven() -> list:
            Returns a list of all even Fibonacci numbers.

        GetOdd() -> list:
            Returns a list of all odd Fibonacci numbers.

        Median() -> float:
            Returns the median value of the MathSer Series.

        MulSeries(x) -> list:
            Returns a new MathSer Series with each term multiplied by `x`.

        DivSeries(x) -> list:
            Returns a new MathSer Series with each term divided by `x`.

        AddSer(x) -> list
            Returns a new MathSer Series with each term added by `x`. 

        SubSer(x) -> list
            Returns a new MathSer Series with each term subtracted by `x`.

        LCM() -> int:
            Returns the Least Common Multiple (LCM) of the MathSer Series.

        Help() -> None:
            Displays help documentation for the TribSer class.
    """
     
    def __init__(self, number_of_terms):
        """
        Initializes the Tribonacci MathSer Series with the given number of terms.

        Args:
            number_of_terms (int): The number of terms in the MathSer Series.

        Raises:
            ValueError: If number_of_terms is less than 3.
        """
        if number_of_terms < 3:
            raise ValueError("Number of terms must be at least 3.")

        self.n = number_of_terms
        self.ser = [1, 1,2]

        for _ in range(self.n - 3):
            self.ser.append(self.ser[-1] + self.ser[-2]+ self.ser[-3])


    def __repr__(self):
        return (
            "TribSer is short for tribonacci MathSer Series. "
            "The methods defined here are FullSer(), LastTerm(), Sum(), and more via Help()."
        )
    

    def Plot(self):
        """Plots the Fibonacci MathSer Series using matplotlib."""
        plt.plot(range(self.n), self.ser, marker="o", color="red")
        plt.title("Tribonacci MathSer Series")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.show()

    def SubPlot(self, start_index, end_index):
        """
        Plots a subset of the Fibonacci MathSer Series.

        Args:
            start_index (int): The starting index (0-based).
            end_index (int): The ending index (0-based).
        """
        if not (0 <= start_index < self.n and 0 <= end_index < self.n and start_index <= end_index):
            raise IndexError("Invalid index range.")

        subser = self.ser[start_index:end_index + 1]
        plt.plot(range(start_index, end_index + 1), subser, marker="o", color="blue")
        plt.title("Subset of Tribonacci MathSer Series")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.show()

