from math import *
from functools import reduce
import warnings
import matplotlib.pyplot as plt #type:ignore
class PasTri():
    """
    PasTri Class
    ============

    This class generates and operates on a single row of Pascal's Triangle.

    Methods:
    --------
    - `Sum()`: Returns the sum of the Pascal row.
    - `FullSer()`: Returns the Pascal row as a tuple.
    - `__repr__()`: Returns a short representation of the class.
    - `__len__()`: Returns the number of elements in the row.
    - `FormsUsed()`: Returns the formula used to generate Pascal's Triangle.
    - `Mean()`: Returns the mean of the row.
    - `AddSer(x)`: Adds a value to each term in the row.
    - `SubSer(x)`: Subtracts a value from each term in the row.
    - `IsInSer(num)`: Checks if a number exists in the row.
    - `IndexSubsetSum(start, end)`: Returns the sum of a subset of the row.
    - `PrimeNumbers()`: Returns prime numbers in the row.
    - `Plot()`: Plots the row as a graph.
    - `SubPlot(start_index, end_index)`: Plots a subset of the row.
    - `Help()`: Displays help documentation for the class.
    - `GetEven()`: Returns all even numbers in the row.
    - `GetOdd()`: Returns all odd numbers in the row.
    - `Median()`: Returns the median of the row.
    - `MulSeries(x)`: Multiplies each element in the row by `x`.
    - `DivSeries(x)`: Divides each element in the row by `x`.
    - `LCM()`: Returns the least common multiple of the row elements.

    Usage Example:
    --------------
    ```python
    pascal_row = PasTri(5)
    print(pascal_row.FullSer())  # Output: (1, 5, 10, 10, 5, 1)
    print(pascal_row.Sum())      # Output: 32
    ```
    """

    def __init__(self,row):
        
        self.n1  = row
        self.ser = [comb(self.n1, k) for k in range(self.n1 + 1)]
        self.n = self.ser[-1]

    def Sum(self):
        """
        Returns:
            int: The sum of the MathSer Series calculated using a closed-form formula.
        """
        
    
        return sum(self.ser)

    def FullSer(self):
        """
        Returns:
            tuple: The full MathSer Series as a tuple.
        """
        return tuple(self.ser)

   

    def __repr__(self):
        """
        Returns:
            str: A short representation of the MathSer Series with usage hints.
        """
        return "PasTri is short for Pascals' Triangle"

    def __len__(self):
        """
        Returns:
            int: The number of elements in the MathSer Series.
        """
        return len(self.ser)

    def FormsUsed(self):
        """
        Returns:
            dict: The formulas used for calculating MathSer Series values.
        """
        return {
            "nth row" : "[comb(self.n, k) for k in range(self.n + 1)]"
        }

    def Mean(self):
        """
        Returns:
            int: The mean (average) of the MathSer Series.
        """
        return round(self.Sum() / len(self.ser))

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



    def IsInSer(self, num):
        """
        Checks if a number is in the MathSer Series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the MathSer Series, False otherwise.
        """
        return num in self.ser

    def IndexSubsetSum(self, start, end):
        """
        Returns the sum of a subset of the MathSer Series within a given range.

        Args:
            start (int): The starting value of the subset.
            end (int): The ending value of the subset.

        Returns:
            int or str: The sum of the subset or an error message if the range is invalid.
        """
    
        if start < self.ser[0] or end > self.n or start > end:
            return "Invalid range!"
        return sum(list(self.ser[start:end]))

    def PrimeNumbers(self):
        """
        Returns all prime numbers in the MathSer Series using the Sieve of Eratosthenes.

        Returns:
            list of int: Prime numbers found in the MathSer Series.
        """
        if self.ser[-1] < 2:
            return []
        limit = self.ser[-1]
        is_prime = [True] * (limit + 1)
        is_prime[0], is_prime[1] = False, False
        for num in range(2, int(limit ** 0.5) + 1):
            if is_prime[num]:
                for multiple in range(num * num, limit + 1, num):
                    is_prime[multiple] = False
        return [num for num in self.ser if is_prime[num]]

    def Plot(self):
        """
        Plots the MathSer Series using matplotlib.
        """
        y = list(range(len(self.ser)))
        plt.plot(self.ser, y, marker='o', color='red')
        plt.title("Series")
        plt.xlabel("Numbers of MathSer Series")
        plt.show()

    def SubPlot(self, start_index, end_index):
        """
        Plots a subset of the MathSer Series using matplotlib.

        Args:
            start_index (int): Starting index of the subset.
            end_index (int): Ending index of the subset.
        """
        subser = self.ser[start_index:end_index]
        y = list(range(len(subser)))
        plt.plot(subser, y, marker='o', color='red')
        plt.title("Sub-Series")
        plt.xlabel("Numbers of MathSer Series")
        plt.show()

    def Help(self):
        """
        Displays help documentation for the Ser class.
        """
        return help(PasTri)

    def GetEven(self):
        """
        Returns a list of all even numbers in the MathSer Series.

        Returns:
            list of int: Even numbers.
        """
        return [i for i in self.ser if i % 2 == 0]

    def GetOdd(self):
        """
        Returns a list of all odd numbers in the MathSer Series.

        Returns:
            list of int: Odd numbers.
        """
        return [i for i in self.ser if i % 2 != 0]

    def Median(self):
        """
        Returns the median of the MathSer Series.

        Returns:
            int: The median value.
        """
        if len(self.ser) % 2 == 1:
         return self.ser[len(self.ser) // 2]
        return(self.ser[len(self.ser) // 2 - 1] + self.ser[len(self.ser) // 2]) / 2

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

    def LCM(self):
        """
        Returns the Least Common Multiple (LCM) of the MathSer Series.

        Returns:
            int: The LCM of the MathSer Series.
        """
        return reduce(lambda x, y: (x * y) // gcd(x, y), self.ser)
