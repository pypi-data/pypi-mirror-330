import matplotlib.pyplot as plt#type:ignore
from functools import reduce
from math import gcd

class Factors:
    """
    A class that generates and operates on the factors of a given number.
    """

    def __init__(self, num):
        """
        Initializes the Factors object and calculates the factors of the given number.

        Args:
            num (int): The number whose factors are to be found.
        """
        self.num = num
        self.ser = [i for i in range(1, round(num/2) + 1) if num % i == 0]
        self.ser.append(self.num)

    def Sum(self):
        """
        Returns the sum of all factors.

        Returns:
            int: The sum of the factors.
        """
        return sum(self.ser)

    def FullSer(self):
        """
        Returns the full series of factors.

        Returns:
            tuple: The factors as a tuple.
        """
        return tuple(self.ser)

    def __repr__(self):
        """
        Returns a string representation of the Factors object.

        Returns:
            str: A description of the class.
        """
        return f"Factors of {self.num}"

    def __len__(self):
        """
        Returns the number of elements in the factor series.

        Returns:
            int: The count of factors.
        """
        return len(self.ser)

    def Mean(self):
        """
        Returns the mean (average) of the factor series.

        Returns:
            float: The average of the factors.
        """
        return round(self.Sum() / len(self.ser), 2)

    def AddSer(self, x):
        """
        Adds a value to each element in the factor series.

        Args:
            x (int): The value to add.

        Returns:
            list: The modified series.
        """
        if not isinstance(x, (int, float)):
            raise TypeError('The provided input is not an int/float')
        return [i + x for i in self.ser]

    def SubSer(self, x):
        """
        Subtracts a value from each element in the factor series.

        Args:
            x (int): The value to subtract.

        Returns:
            list: The modified series.
        """
        if not isinstance(x, (int, float)):
            raise TypeError('The provided input is not an int/float')
        return [i - x for i in self.ser]

    def IsInSer(self, num):
        """
        Checks if a number is in the factor series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the series, False otherwise.
        """
        return num in self.ser

    def IndexSubsetSum(self, start, end):
        """
        Returns the sum of a subset of the factor series.

        Args:
            start (int): The starting index.
            end (int): The ending index.

        Returns:
            int or str: The sum of the subset or an error message if the range is invalid.
        """
        if start < 0 or end > len(self.ser) or start > end:
            return "Invalid range!"
        return sum(self.ser[start:end])

    def PrimeNumbers(self):
        """
        Returns all prime numbers in the factor series.

        Returns:
            list: Prime numbers from the series.
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
        """
        Plots the factor series using matplotlib.
        """
        plt.plot(self.ser, range(len(self.ser)), marker='o', color='red')
        plt.title("Factor Series")
        plt.xlabel("Factors")
        plt.ylabel("Index")
        plt.show()

    def SubPlot(self, start_index, end_index):
        """
        Plots a subset of the factor series.

        Args:
            start_index (int): Starting index.
            end_index (int): Ending index.
        """
        subser = self.ser[start_index:end_index]
        plt.plot(subser, range(len(subser)), marker='o', color='red')
        plt.title("Subset of Factor Series")
        plt.xlabel("Factors")
        plt.ylabel("Index")
        plt.show()

    def GetEven(self):
        """
        Returns all even numbers in the factor series.

        Returns:
            list: Even numbers.
        """
        return [i for i in self.ser if i % 2 == 0]

    def GetOdd(self):
        """
        Returns all odd numbers in the factor series.

        Returns:
            list: Odd numbers.
        """
        return [i for i in self.ser if i % 2 != 0]

    def Median(self):
        """
        Returns the median of the factor series.

        Returns:
            float: The median value.
        """
        n = len(self.ser)
        if n % 2 == 1:
            return self.ser[n // 2]
        return (self.ser[n // 2 - 1] + self.ser[n // 2]) / 2

    def MulSeries(self, x):
        """
        Multiplies each term in the factor series by x.

        Args:
            x (int): The multiplier.

        Returns:
            list: The modified series.
        """
        if not isinstance(x, (int, float)):
            raise TypeError('The provided input is not an int/float')
        return [i * x for i in self.ser]

    def DivSeries(self, x):
        """
        Divides each term in the factor series by x.

        Args:
            x (int): The divisor.

        Returns:
            list: The modified series.

        Raises:
            ValueError: If divisor is 0.
        """
        if not isinstance(x, (int, float)):
            raise TypeError('The provided input is not an int/float')
        if x == 0:
            raise ValueError('Cannot divide by 0')
        return [i / x for i in self.ser]

    def LCM(self):
        """
        Returns the Least Common Multiple (LCM) of the factor series.

        Returns:
            int: The LCM of the factors.
        """
        return reduce(lambda x, y: (x * y) // gcd(x, y), self.ser) if self.ser else None
