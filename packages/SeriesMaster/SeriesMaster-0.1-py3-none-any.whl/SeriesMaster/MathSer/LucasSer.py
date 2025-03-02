import warnings
from math import gcd
from functools import reduce
from matplotlib import pyplot as plt # type:ignore# type:ignore
class LucasSer():
    """
    This class generates a Lucas Series, which is similar to the Fibonacci Series.
    The Lucas Series starts with the terms 1 and 2 instead of 0 and 1 as in the Fibonacci Series.

    Inherits from:
        BonAcci.FibSer: This class extends the Fibonacci Series class.

    Attributes:
        n1 (int): The number of terms to generate in the Lucas Series.
        ser (list): A list containing the terms of the Lucas Series.

    Methods:
        __init__(self, number_of_terms):
            Initializes the Lucas Series with a given number of terms.

        IsInSer(self, num):
            Checks if a given number is part of the Lucas Series.

        __repr__(self):
            Provides a string representation of the Lucas Series class.

        FullSer(self):
            Returns the complete Lucas Series.

        LastTerm(self):
            Returns the last term of the Lucas Series.

        IndexSubsetSum(self, start_idx, end_idx):
            Returns the sum of the Lucas numbers within a specified index range.

        PrimeNumbers(self):
            Returns a list of prime numbers from the Lucas Series.

        Plot(self):
            Plots the Lucas Series using matplotlib.

        SubPlot(self, start_index, end_index):
            Plots a subset of the Lucas Series.

        GetEven(self):
            Returns a list of even numbers from the Lucas Series.

        GetOdd(self):
            Returns a list of odd numbers from the Lucas Series.

        Median(self):
            Computes and returns the median of the Lucas Series.

        MulSeries(self, x):
            Returns a new series where each term is multiplied by x.

        DivSeries(self, x):
            Returns a new series where each term is divided by x.

        AddSer(self, x):
            Returns a new series where each term is incremented by x.

        SubSer(self, x):
            Returns a new series where each term is decremented by x.

        LCM(self):
            Computes and returns the Least Common Multiple (LCM) of the Lucas Series.

        __len__(self):
            Returns the number of terms in the Lucas Series.
    """


    def __init__(self, number_of_terms):
        """
        Initializes the Lucas MathSer Series with the given number of terms.

        Args:
            number_of_terms (int): The number of terms to generate in the Lucas MathSer Series.

        Raises:
            ValueError: If the number_of_terms is less than 2.
        
        Example:
            lucas = LucasSer(10)
        """
        if number_of_terms < 2:
            raise ValueError("Number of terms should at least be 2")
        
        self.n1 = number_of_terms
        self.ser = [1, 2]

        # Generate the Lucas MathSer Series up to the required number of terms
        for i in range(self.n1 - 2):  # -2 because we already have the first two terms
            self.ser.append(self.ser[-1] + self.ser[-2])

    def IsInSer(self, num):
        """
        Checks if a number is in the Lucas MathSer Series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the MathSer Series, False otherwise.

        Example:
            lucas = LucasSer(10)
            lucas.IsInSer(13)  # Returns True if 13 is in the Lucas MathSer Series.
        """
        a, b = 1, 2
        while a <= num:
            if a == num:
                return True
            a, b = b, a + b
        return False

    def __repr__(self):
        """
        Returns a string representation of the Lucas MathSer Series class.

        Returns:
            str: A string describing the Lucas MathSer Series.

        Example:
            lucas = LucasSer(10)
            print(lucas)  # Outputs: "This is the Lucas Ser it is the same as Fib Ser just the start terms are 1,2"
        """
        return "This is the Lucas Ser. It is the same as Fib Ser, just the start terms are 1, 2."
    
    def FullSer(self):
        """Returns the full Fibonacci MathSer Series."""
        return self.ser

    def LastTerm(self):
        """Returns the last term of the Fibonacci MathSer Series."""
        return self.ser[-1]
    
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



