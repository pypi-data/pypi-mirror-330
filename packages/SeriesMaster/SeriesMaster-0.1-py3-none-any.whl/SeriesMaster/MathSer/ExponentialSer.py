"""
#ExponentialSer

## Module Overview
This module provides a class, `SquareSer`,`CubicSer` for generating and analyzing a squared arithmetic Math Series.
The class creates a sequence where each term is the square of an arithmetic sequence term and provides
various utility functions for analysis, transformation, and visualization.

## Dependencies
This module requires the following libraries:
- `warnings` (for potential future warnings)
- `math` (for mathematical operations)
- `matplotlib.pyplot` (for plotting the Math Series)
- `functools.reduce` (for LCM calculation)

## Class: SquareSer
### Description
The `SquareSer` class generates a squared arithmetic Math Series and offers methods to analyze, modify, and visualize the Math Series.

### Attributes
- `n1` *(int)*: Number of terms in the Math Series.
- `a` *(int)*: First term of the arithmetic Math Series.
- `d` *(int)*: Common difference of the arithmetic Math Series.
- `n` *(int)*: Last term of the arithmetic Math Series.
- `ser` *(list of int)*: List containing the squared terms of the arithmetic Math Series.

### Methods

#### Math Series Information & Analysis
- `LastTerm() -> int`
  Returns the last term of the arithmetic Math Series.

- `FullSer() -> tuple`
  Returns the complete squared Math Series as a tuple.

- `Sum() -> int`
  Computes the sum of all squared terms in the Math Series.

- `Mean() -> int`
  Computes the mean (average) of the squared Math Series.

- `Median() -> int or float`
  Returns the median value of the Math Series.

- `LCM() -> int`
  Computes the least common multiple (LCM) of all terms in the Math Series.

- `FormsUsed() -> dict`
  Returns a dictionary of formulas used in Math Series calculations.

#### Filtering & Checking
- `GetEven() -> list`
  Returns a list of even numbers in the Math Series.

- `GetOdd() -> list`
  Returns a list of odd numbers in the Math Series.

- `IsInSer(num: int) -> bool`
  Checks if a given number exists in the Math Series.

- `PrimeNumbers() -> list`
  Returns the prime numbers present in the Math Series.

#### Subset & Index Operations
- `IndexSubsetSum(start: int, end: int) -> int or str`
  Computes the sum of a subset of the Math Series based on a given range.

#### Modifying the Math Series (Temporary Changes)
- `AddSer(x: int) -> list`
  Returns a modified Math Series with each term incremented by `x`.

- `SubSer(x: int) -> list`
  Returns a modified Math Series with each term decremented by `x`.

- `MulSeries(x: int) -> list`
  Returns a modified Math Series with each term multiplied by `x`.

- `DivSeries(x: int) -> list`
  Returns a modified Math Series with each term divided by `x`.
  - **Raises** `ValueError` if `x == 0`.

#### Visualization
- `Plot()`
  Generates a plot of the Math Series using `matplotlib`.

- `SubPlot(start_index: int, end_index: int)`
  Generates a plot of a subset of the Math Series.

#### Utility & Help
- `Help()`
  Displays the documentation for the `SquareSer` class.

CubicSer
A class to represent a cubic sequence derived from an arithmetic sequence.

    Inherits from:
        SquareSer (Assuming SquareSer is a class that handles square Math Series)

    Attributes:
        n1 (int): Number of terms in the Math Series.
        a (int or float): First term of the Math Series.
        d (int or float): Common difference between terms.
        n (int or float): Last term before applying the cubic operation.
        ser (list): List containing the cubic values of the arithmetic Math Series.

    Methods:
        Sum():
            Returns the sum of the cubic Math Series.

        LastTerm():
            Returns the last term of the Math Series raised to the power of 3.

        FormsUsed():
            Returns a dictionary of formulas used in calculations.

### Example Usage
```python
from square_series_module import SquareSer

# Create a squared arithmetic Math Series
ser = SquareSer(5, 2, 3)

# Get the full squared Math Series
print(ser.FullSer())  # Output: (4, 25, 64, 121, 196)

# Compute the sum of the Math Series
print(ser.Sum())  # Output: 410

# Get all even numbers in the Math Series
print(ser.GetEven())  # Output: [4, 64, 196]

# Check if a number exists in the Math Series
print(ser.IsInSer(25))  # Output: True

# Get prime numbers from the Math Series
print(ser.PrimeNumbers())  # Output: [5]

# Plot the Math Series
ser.Plot()
"""


import warnings
from math import *

import matplotlib.pyplot as plt#type:ignore
from functools import reduce  

##Square Class
class SquareSer():
    """
    A class to generate and analyze a squared arithmetic Math Series.

    The class generates a Math Series where each term is the square of an arithmetic 
    sequence term. It provides various utility functions to analyze and manipulate 
    the Math Series.

    Attributes:
        n1 (int): The number of terms in the Math Series.
        a (int): The first term of the arithmetic Math Series.
        d (int): The common difference of the arithmetic Math Series.
        n (int): The last term of the arithmetic Math Series.
        ser (list of int): The list containing the squared terms of the arithmetic Math Series.

    Methods:
        LastTerm(): Returns the last term of the arithmetic Math Series.
        FullSer(): Returns the complete squared Math Series as a tuple.
        Sum(): Computes the sum of all squared terms.
        Mean(): Computes the average value of the squared Math Series.
        Median(): Returns the median value of the Math Series.
        LCM(): Computes the least common multiple of all terms in the Math Series.
        GetEven(): Returns a list of even numbers in the Math Series.
        GetOdd(): Returns a list of odd numbers in the Math Series.
        IsInSer(num): Checks if a given number exists in the Math Series.
        IndexSubsetSum(start, end): Computes the sum of a subset of the Math Series.
        PrimeNumbers(): Returns the prime numbers present in the Math Series.
        AddSer(x): Returns a modified Math Series with each term incremented by x.
        SubSer(x): Returns a modified Math Series with each term decremented by x.
        MulSeries(x): Returns a modified Math Series with each term multiplied by x.
        DivSeries(x): Returns a modified Math Series with each term divided by x.
        Plot(): Generates a plot of the Math Series.
        SubPlot(start_index, end_index): Generates a plot of a subset of the Math Series.
        FormsUsed(): Returns a dictionary of formulas used in computations.
        Help(): Displays the documentation for the class.
    
    Example:
        >>> ser = SquareSer(5, 2, 3)
        >>> ser.FullSer()
        (4, 25, 64, 121, 196)
        >>> ser.Sum()
        410
        >>> ser.GetEven()
        [4, 64, 196]
        >>> ser.PrimeNumbers()
        [5]
    """



    def __init__(self,number_of_terms,first_term,difference):

        self.n1 = number_of_terms
        self.a = first_term
        self.d = difference
        self.n = self.a + (self.n1-1) * self.d

        self.ser = [(self.a + i * self.d)**2 for i in range(self.n1)]

    def __len__(self):
        return len(self.ser)


    def LastTerm(self):
        """
        Returns:
            int: The last term of the Math Series.
        """
        return self.n**2

    def FullSer(self):
        """
        Returns:
            tuple: The full Math Series as a tuple.
        """
        return tuple(self.ser)

    def Sum(self):
        """
        Returns:
            int: The sum of all terms in the Math Series.
        """
        
        self.sqsum = round(((self.n / self.d * (self.n / self.d + 1) * (2 * self.n / self.d + 1) -
                             (self.a - self.d) / self.d * ((self.a - self.d) / self.d + 1) * (2 * (self.a - self.d) / self.d + 1))
                            * self.d / 6) * self.d)
        return self.sqsum

    def __repr__(self):
        """
        Returns:
            str: A short representation of the Math Series with usage hints.
        """
        return (f"The provided Math Series is {tuple(self.ser)}\n"
                "To look at the Last term, use LastTerm(); for the sum, use Sum(); for the square sum, use ;\n"
                "For formulas, see FormsUsed() and other functions via Help().")

    def __len__(self):
        """
        Returns:
            int: The number of elements in the Math Series.
        """
        return len(self.ser)

    def FormsUsed(self):
        """
        Returns:
            dict: The formulas used for calculating Math Series values.
        """
        return {
            "n1": "Number of terms",
            "a": "First Term",
            "d": "Common Difference",
            "n": "Last Term (a + (n1 - 1) * d)",
            "Last Term Formula": "a + (n1 - 1) * d",
            "Sum Formula": "round(((n/d * (n/d + 1) * (2*n/d + 1) - (a-d)/d * ((a-d)/d + 1) * (2*(a-d)/d + 1)) * d / 6) * d)",
            "Mean Formula": "Sum of terms / Number of terms"
        }

    def Mean(self):
        """
        Returns:
            int: The mean (average) of the Math Series.
        """
        return round(self.Sum() / self.n1)

    def AddSer(self,x):
        """
        Add value to the Math Series. This is a temperory change.

        Args:
            x (int): The addend

        Returns:
            list: The added Math Series

        Raises:
            TypeError: If the input is not an int.
        """
        if type(x) != int and type(x) != float:
            raise TypeError('The provided input is not an int/float')
        new_ser = []

        for i in range(self.n1):
            new_ser.append(self.ser[i]+x)

        return new_ser
 
    def SubSer(self,x):
        """
        Subtract value to the Math Series. This is a temperory change.

        Args:
            x (int): The minuend

        Returns:
            list: The subtracted Math Series
        Raises:
            TypeError: If the input is not an int.
        """
        if type(x) != int and type(x) != float:
            raise TypeError('The provided input is not an int/float')

        new_ser = []

        for i in range(self.n1):
            new_ser.append(self.ser[i]-x)

        return new_ser



    def IsInSer(self, num):
        """
        Checks if a number is in the Math Series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the Math Series, False otherwise.
        """
        return num in self.ser

    def IndexSubsetSum(self, start, end):
        """
        Returns the sum of a subset of the Math Series within a given range.

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
        Returns all prime numbers in the Math Series using the Sieve of Eratosthenes.

        Returns:
            list of int: Prime numbers found in the Math Series.
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
        Plots the Math Series using matplotlib.
        """
        y = list(range(len(self.ser)))
        plt.plot(self.ser, y, marker='o', color='red')
        plt.title("Series")
        plt.xlabel("Numbers of Math Series")
        plt.show()

    def SubPlot(self, start_index, end_index):
        """
        Plots a subset of the Math Series using matplotlib.

        Args:
            start_index (int): Starting index of the subset.
            end_index (int): Ending index of the subset.
        """
        subser = self.ser[start_index:end_index]
        y = list(range(len(subser)))
        plt.plot(subser, y, marker='o', color='blue')
        plt.title("Sub-Series")
        plt.xlabel("Numbers of Math Series")
        plt.show()

    def Help(self):
        """
        Displays help documentation for the Ser class.
        """
        return help(SquareSer)

    def GetEven(self):
        """
        Returns a list of all even numbers in the Math Series.

        Returns:
            list of int: Even numbers.
        """
        return [i for i in self.ser if i % 2 == 0]

    def GetOdd(self):
        """
        Returns a list of all odd numbers in the Math Series.

        Returns:
            list of int: Odd numbers.
        """
        return [i for i in self.ser if i % 2 != 0]

    def Median(self):
        """
        Returns the median of the Math Series.

        Returns:
            int: The median value.
        """
        if len(self.ser) % 2 == 1:
         return self.ser[self.n1 // 2]
        return(self.ser[len(self.ser) // 2 - 1] + self.ser[len(self.ser) // 2]) / 2

    def MulSeries(self, x):
        """
        Returns a new Math Series with each term multiplied by x.

        Args:
            x (int): The multiplier.

        Returns:
            list of int: The multiplied Math Series.
        Raises:
            TypeError: If the input is not an int.
        """
        if type(x) != int and type(x) != float:
            raise TypeError('The provided input is not an int/float')
        return [i * x for i in self.ser]

    def DivSeries(self, x):
        """
        Returns a new Math Series with each term divided by x.

        Args:
            x (int): The divisor.

        Returns:
            list of float: The divided Math Series.

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
        Returns the Least Common Multiple (LCM) of the Math Series.

        Returns:
            int: The LCM of the Math Series.
        """
        return reduce(lambda x, y: (x * y) // gcd(x, y), self.ser)


class CubicSer(SquareSer):
    """
    A class to represent a cubic sequence derived from an arithmetic sequence.

    Inherits from:
        SquareSer (Assuming SquareSer is a class that handles square Math Series)

    Attributes:
        n1 (int): Number of terms in the Math Series.
        a (int or float): First term of the Math Series.
        d (int or float): Common difference between terms.
        n (int or float): Last term before applying the cubic operation.
        ser (list): List containing the cubic values of the arithmetic Math Series.

    Methods:
        Sum():
            Returns the sum of the cubic Math Series.

        LastTerm():
            Returns the last term of the Math Series raised to the power of 3.

        FormsUsed():
            Returns a dictionary of formulas used in calculations.
    """

    def __init__(self, number_of_terms, first_term, difference):
        """
        Initializes the CubicSer class with the given parameters.

        Args:
            number_of_terms (int): Number of terms in the Math Series.
            first_term (int or float): The first term of the Math Series.
            difference (int or float): The common difference between terms.

        Attributes:
            n1 (int): Stores the number of terms.
            a (int or float): Stores the first term.
            d (int or float): Stores the common difference.
            n (int or float): Stores the last term before applying cubic operation.
            ser (list): Stores the computed cubic Math Series.
        """
        self.n1 = number_of_terms
        self.a = first_term
        self.d = difference
        self.n = self.a + (self.n1 - 1) * self.d
        self.ser = [(self.a + i * self.d) ** 3 for i in range(self.n1)]

    def Sum(self):
        """
        Calculates the sum of all terms in the cubic Math Series.

        Returns:
            int or float: The sum of the cubic Math Series.
        """
        return sum(self.ser)
    
    def LastTerm(self):
        """
        Computes the last term of the Math Series raised to the power of 3.

        Returns:
            int or float: The last term cubed.
        """
        return self.n ** 3

    def FormsUsed(self):
        """
        Provides the formulas used in the Math Series calculations.

        Returns:
            dict: The formulas for the number of terms, first term, 
                  common difference, last term, last term formula, 
                  and mean formula.
        """
        return {
            "n1": "Number of terms",
            "a": "First Term",
            "d": "Common Difference",
            "n": "Last Term (a + (n1 - 1) * d)",
            "Last Term Formula": "a + (n1 - 1) * d",
            "Mean Formula": "Sum of terms / Number of terms"
        }
    def Help(self):
        """Returns the help documentation on CubicSer"""

        return help(CubicSer)