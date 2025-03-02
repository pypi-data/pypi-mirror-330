"""
Module: MathSer Series  

This module provides tools for working with different types of mathematical MathSer Series, including **Arithmetic**, **Geometric**, and **Fibonacci** MathSer Series.  
It also includes a utility class for performing element-wise arithmetic operations between two MathSer Series.

Classes:

    ArthSer:
        Represents and manipulates an **arithmetic MathSer Series**.

        Attributes:
            n1 (int): The number of terms in the MathSer Series.
            a (int): The first term of the MathSer Series.
            d (int): The common difference between consecutive terms.
            n (int): The last term of the MathSer Series (calculated as a + (n1 - 1) * d).
            ser (list of int): The full arithmetic MathSer Series stored as a list.

        Methods:
            __init__(number_of_terms, first_term, difference):
                Initializes an arithmetic MathSer Series with the specified number of terms, first term, and common difference.

            Sum() -> int:
                Returns the sum of all terms in the MathSer Series.

            LastTerm() -> int:
                Returns the last term of the MathSer Series.

            FullSer() -> tuple:
                Returns the entire MathSer Series as a tuple.

            SqSum() -> int:
                Returns the sum of the squares of the terms in the MathSer Series.

            FormsUsed() -> dict:
                Returns a dictionary containing the formulas used in calculations.

            Mean() -> float:
                Returns the arithmetic mean (average) of the MathSer Series.

            Append(appends) -> bool or list[bool]:
                Appends a value or a list/tuple of values to the MathSer Series.
                Note: The appended values must maintain the arithmetic progression.

            Remove(r) -> bool or list[bool]:
                Removes a value or a list/tuple of values from the MathSer Series.
                Note: Only the first or last element of the MathSer Series can be removed without breaking the progression.

            IsInSer(num) -> bool:
                Checks if a number is in the arithmetic MathSer Series.

            IndexSubsetSum(start, end) -> int or str:
                Returns the sum of a subset of the MathSer Series within a specified range.

            PrimeNumbers() -> list[int]:
                Returns a list of prime numbers present in the MathSer Series.

            Plot():
                Plots the MathSer Series using matplotlib.

            SubPlot(start_index, end_index):
                Plots a subset of the MathSer Series.

            Help():
                Displays help documentation for the class.

            GetEven() -> list[int]:
                Returns a list of all even numbers in the MathSer Series.

            GetOdd() -> list[int]:
                Returns a list of all odd numbers in the MathSer Series.

            Median() -> float:
                Returns the median of the MathSer Series.

            MulSeries(x) -> list[int]:
                Returns a new MathSer Series with each term multiplied by x.

            DivSeries(x) -> list[float]:
                Returns a new MathSer Series with each term divided by x.

            LCM() -> int:
                Returns the least common multiple of all terms in the MathSer Series.

    GeoSer:
        Represents and manipulates a **geometric MathSer Series**.

        Attributes:
            n1 (int): The number of terms in the MathSer Series.
            a (int): The first term of the MathSer Series.
            r (int): The common ratio between consecutive terms.
            n (int): The last term of the MathSer Series (calculated as a * r^(n1-1)).
            ser (list of int): The full geometric MathSer Series stored as a list.

        Methods:
            __init__(number_of_terms, first_term, ratio):
                Initializes a geometric MathSer Series with the given parameters.

            Sum() -> float:
                Returns the sum of the geometric MathSer Series.

            LastTerm() -> int:
                Returns the last term of the MathSer Series.

            FullSer() -> list[int]:
                Returns the entire MathSer Series.

            SqSum() -> float:
                Returns the sum of the squares of the terms in the MathSer Series.

            FormsUsed() -> dict:
                Returns a dictionary containing formulas used in calculations.

            Append(appends) -> bool or list[bool]:
                Appends a value or a list/tuple of values to the MathSer Series.
                Note: The appended values must maintain the geometric progression.

            Remove(r) -> bool or list[bool]:
                Removes a value or a list/tuple of values from the MathSer Series.
                Note: Only the first or last element of the MathSer Series can be removed without breaking the progression.

            Help():
                Displays help documentation for the class.

    HardCodeSer:
        Allows users to define and manipulate a manually created numerical MathSer Series.
        Unlike an arithmetic or geometric MathSer Series, this class lets users input their own 
        sequences without enforcing any mathematical pattern.

        Attributes:
            ser (list[int]): The user-defined number MathSer Series.

        Methods:
            __init__(series: list[int] or tuple[int]):
                Initializes the class with a manually defined number sequence.

            Sum() -> int:
                Returns the sum of all elements in the MathSer Series.

            SqSum() -> int:
                Returns the sum of the squares of all elements in the MathSer Series.

            Append(append: int) -> str:
                Appends an integer to the MathSer Series and returns a success message.
                Raises:
                    TypeError: If the input is not an integer.

            Remove(r: int) -> None:
                Removes the given integer from the MathSer Series if it exists.
                Raises:
                    ValueError: If the number is not in the MathSer Series.
                    TypeError: If the input is not an integer.

            IsInSer(num: int) -> bool:
                Checks if a given number exists in the MathSer Series.

            __repr__() -> str:
                Returns a string representation of the MathSer Series.

    HarmSer (Harmonic MathSer Series)

    This class represents a **harmonic MathSer Series**, which is derived from an arithmetic sequence
    where each term is the reciprocal of the corresponding arithmetic sequence term.

    Inherits from:
        ArthSer: Since a harmonic MathSer Series is based on an arithmetic progression.

    Attributes:
        n1 (int): The number of terms in the MathSer Series.
        a (int or float): The first term of the arithmetic sequence.
        d (int or float): The common difference in the arithmetic sequence.
        n (int or float): The last term of the arithmetic sequence.
        ser (list of float): The harmonic MathSer Series, containing reciprocals of the arithmetic sequence terms.

    Methods:
        Sum():
            Computes and returns the sum of all terms in the harmonic MathSer Series.

        LastTerm():
            Returns the last term of the harmonic MathSer Series.

        Append():
            Raises an error, as appending values is not supported for harmonic MathSer Series.

        Remove():
            Raises an error, as removing values is not supported for harmonic MathSer Series.

        SqSum():
            Returns the sum of squares of all terms in the harmonic MathSer Series.

        __repr__():
            Returns a short description of the class.

    Exceptions:
        ValueError: Raised for invalid input values (e.g., negative terms in MathSer Series initialization, appending/removing values that break the progression).
        TypeError: Raised when performing operations between incompatible MathSer Series.
        IndexError: Raised if two MathSer Series do not have the same length (in BasicOperationsOnSeries).
        ZeroDivisionError: Raised when attempting to divide by zero in DivSeries() or BasicOperationsOnSeries.Divide().

Example Usage:

    >>> s1 = ArthSer(5, 2, 3)  # Arithmetic MathSer Series: 2, 5, 8, 11, 14
    >>> s1.Sum()
    40
    >>> s2 = GeoSer(5, 3, 2)  # Geometric MathSer Series: 3, 6, 12, 24, 48
    >>> s2.Sum()
    93
    >>> hc = HardCodeSer([3, 5, 7, 9])  # Manually defined MathSer Series
    >>> hc.Sum()
    24
    >>> hc.SqSum()
    164
    >>> hc.Append(11)
    'Successfully appended'
    >>> hc.Remove(5)
    >>> hc.IsInSer(7)
    True
"""



import warnings
import matplotlib.pyplot as plt #type:ignore
from math import gcd  
from functools import reduce  


class ArthSer():
    """
    Ser (Series) Class

    Creates an arithmetic MathSer Series and provides methods for various calculations.

    Attributes:
        n1 (int): Number of terms in the MathSer Series.
        a (int): First term of the MathSer Series.
        d (int): Common difference.
        n (int): Last term of the MathSer Series (computed as a + (n1 - 1) * d).
        ser (list of int): The arithmetic MathSer Series.

    Methods:
        Sum() -> int:
            Returns the sum of the MathSer Series using a closed-form formula.
        LastTerm() -> int:
            Returns the last term of the MathSer Series.
        FullSer() -> tuple:
            Returns the full MathSer Series as a tuple.
        SqSum() -> int:
            Returns the sum of squares of all terms.
        FormsUsed() -> dict:
            Returns the formulas used in the calculations.
        Append(appends: int or list/tuple of int) -> str:
            Adds value(s) to the MathSer Series with error handling.
        Remove(r: int or list/tuple of int) -> str:
            Removes value(s) from the MathSer Series with error handling.
        IsInSer(num: int) -> bool:
            Checks if a given number is in the MathSer Series.
        IndexSubsetSum(start: int, end: int) -> int or str:
            Returns the sum of a subset of the MathSer Series; returns an error message if the range is invalid.
        PrimeNumbers() -> list of int:
            Returns all prime numbers in the MathSer Series using the Sieve of Eratosthenes.
        GetOdd() -> list of int:
            Returns a list of all odd numbers in the MathSer Series.
        GetEven() -> list of int:
            Returns a list of all even numbers in the MathSer Series.
        Median() -> int:
            Returns the median of the MathSer Series.
        MulSeries(x: int) -> list of int/float:
            Returns a new MathSer Series with each term multiplied by x.
        DivSeries(x: int) -> list of float/int:
            Returns a new MathSer Series with each term divided by x.
        AddSer(x) -> list of int/float
            Returns a new MathSer Series with each term added by `x`. 

        SubSer(x) -> list of int/float
            Returns a new MathSer Series with each term subtracted by `x`.

        LCM() -> int:
            Returns the Least Common Multiple (LCM) of the MathSer Series.
        Plot() -> None:
            Plots the MathSer Series using matplotlib.
        SubPlot(start_index: int, end_index: int) -> None:
            Plots a portion of the MathSer Series using matplotlib.
        Help() -> None:
            Displays help documentation for the Ser class.
    """

    def __init__(self, number_of_terms, first_term, difference):
        """
        Initializes the Ser instance with the specified number of terms, first term, and common difference.
        
        A warning is issued if the MathSer Series pattern might be disrupted by Append() or Remove() operations.
        """
        warnings.warn(
            ('Warning! While using the Append() method, if the appended values are not in the '
             'correct pattern or if you remove a digit randomly (not from the start or end), '
             'the Sum, SqSum, and IndexSubsetSum functions may error because the code relies on a '
             'consistent arithmetic pattern (e.g., (2,3,4,5,6) or (7,9,11,13)).'),
            UserWarning
        )

        self.n1 = number_of_terms
        self.a = first_term
        self.d = difference
        self.n = self.a + (self.n1 - 1) * self.d
        self.ser = [self.a + i * self.d for i in range(self.n1)]
    
        if self.a <0 or self.d < 0 or self.n < 0:
            raise ValueError("One of the terms is less than 0")

    def Sum(self):
        """
        Returns:
            int: The sum of the MathSer Series calculated using a closed-form formula.
        """
        
        self.sum = round((self.n / self.d * (self.n / self.d + 1) - (self.a - self.d) / self.d * ((self.a - self.d) / self.d + 1)) * self.d / 2)
        return self.sum

    def LastTerm(self):
        """
        Returns:
            int: The last term of the MathSer Series.
        """
        return self.n

    def FullSer(self):
        """
        Returns:
            tuple: The full MathSer Series as a tuple.
        """
        return tuple(self.ser)

    def SqSum(self):
        """
        Returns:
            int: The sum of squares of all terms in the MathSer Series.
        """
        
        self.sqsum = round(((self.n / self.d * (self.n / self.d + 1) * (2 * self.n / self.d + 1) -
                             (self.a - self.d) / self.d * ((self.a - self.d) / self.d + 1) * (2 * (self.a - self.d) / self.d + 1))
                            * self.d / 6) * self.d)
        return self.sqsum

    def __repr__(self):
        """
        Returns:
            str: A short representation of the MathSer Series with usage hints.
        """
        if len(self.ser) >= 100:
            return (f"ArthSer is short for Arthemetic MathSer Series. The provided MathSer Series is {tuple(self.ser[:100])}.....\n"
                    "To look at the full MathSer Series use FullSer(), LastTerm(), Sum(), SqSum(), or FormsUsed().\n"
                    "Other functions can be accessed via the Help() method.")
        return (f"ArthSer is short for Arthemetic MathSer Series. The provided MathSer Series is {tuple(self.ser)}\n"
                "To look at the Last term, use LastTerm(); for the sum, use Sum(); for the square sum, use SqSum();\n"
                "For formulas, see FormsUsed() and other functions via Help().")

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
            "n1": "Number of terms",
            "a": "First Term",
            "d": "Common Difference",
            "n": "Last Term (a + (n1 - 1) * d)",
            "Sum Formula": "(n/d * (n/d + 1) - (a-d)/d * ((a-d)/d + 1)) * d / 2",
            "Last Term Formula": "a + (n1 - 1) * d",
            "Sum of Squares Formula": "round(((n/d * (n/d + 1) * (2*n/d + 1) - (a-d)/d * ((a-d)/d + 1) * (2*(a-d)/d + 1)) * d / 6) * d)",
            "Mean Formula": "Sum of terms / Number of terms"
        }

    def Mean(self):
        """
        Returns:
            int: The mean (average) of the MathSer Series.
        """
        return round(self.Sum() / self.n1)

    def Append(self, appends):
        """
        Appends value(s) to the MathSer Series.

        Args:
            appends (int or list/tuple of int): Value(s) to append.

        Returns:
            str: A message indicating the result of the append operation.
            


        Raises:
            TypeError: If the input is not an int or a list/tuple of ints.
        """
        t_f = []
        if type(appends) == int:
            if self.n < appends and (appends - self.a) % self.d == 0:
                self.ser.append(appends)
                self.n = self.a +(len(self.ser) - 1) * self.d
                self.n1+=1
                print('Appended Succesfully')
                return True
            
            else:
                warnings.warn('It will break some functions so it is not appended')
                return False
            
        elif type(appends) == list or type(appends) == tuple:
            appends = list(appends)
            appends = sorted(appends)
            for i in appends:
                if self.n < i and (i - self.a) % self.d == 0:
                    self.ser.append(i)
                    print(f'Appended {i} Succesfully')
                    self.n1 = len(self.ser)    
                    self.n = self.a +(len(self.ser) - 1) * self.d
                    t_f.append(True)
                    
            
                else:
                    warnings.warn(f'It will break some functions so {i} is not appended')
                    t_f.append(False)

            return t_f
        else:
            raise TypeError(f"The provided {appends} isn't a list/tuple/int")
            
                

    def Remove(self, r):
        """
        Removes value(s) from the MathSer Series.

        Args:
            r (int or list/tuple of int): Value(s) to remove.

        Returns:
            str: A message indicating the result of the removal operation.

        Raises:
            TypeError: If the input is not an int or a list/tuple of ints.
        """
        t_f = []
        if type(r) == int and self.IsInSer(r):
            if self.a == r or self.n == r:
                self.ser.remove(r)
                self.n1= len(self.ser)
                self.n = self.a + (self.n1-1) *self.d
                print('Removed Successfully')
                return True
            else:
                warnings.warn(f'It will break some functions so {r} is not removed')
                return False
        elif type(r) == list or type(r) == tuple:
             r1 = list(r)
             r1 = sorted(r1, reverse=True)
             for i in r1:
                if self.a == r or self.n == i:
                    self.ser.remove(i)
                    self.n1= len(self.ser)
                    self.n = self.a + (self.n1-1) *self.d
                    print('Removed Successfully')
                    t_f.append(True)
                    
                else:
                    warnings.warn(f'It will break some functions so {i} is not removed')
                    t_f.append(False)
        else:
            raise TypeError(f"The provided {r} isn't a list/tuple/int or it is not in the MathSer Series")
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

        for i in range(self.n1):
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

        for i in range(self.n1):
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
        return help(ArthSer)

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
         return self.ser[self.n1 // 2]
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

class GeoSer(ArthSer):
    """
    GeoSer (Geometric MathSer Series) Class

    Inherits from ArthSer and represents a geometric MathSer Series.

    Attributes:
        n1 (int): Number of terms in the MathSer Series.
        a (float): First term of the MathSer Series.
        r (float): Common ratio of the MathSer Series.
        n (float): Last term of the MathSer Series (computed as a * (r ** (n1 - 1))).
        ser (list of float): The geometric MathSer Series, generated using the formula a * (r ** i) for i in range(n1).
        d: Set to None (not applicable for a geometric MathSer Series).

    Methods:
        __init__(number_of_terms, first_term, ratio):
            Initializes a GeoSer instance.
        Sum() -> float:
            Returns the sum of the MathSer Series using the formula:
                a * (1 - r ** n1) / (1 - r)    if r != 1, else a * n1.
        LastTerm() -> float:
            Returns the last term of the MathSer Series.
        FullSer() -> list:
            Returns the complete geometric MathSer Series as a list.
        SqSum() -> float:
            Returns the sum of squares of the MathSer Series using the formula:
                a^2 * (1 - r^(2 * n1)) / (1 - r^2)    if r != 1, else a^2 * n1.
        FormsUsed() -> dict:
            Returns a dictionary of formulas used for the MathSer Series calculations.
        Help() -> None:
            Displays help documentation for the GeoSer class.
        Append(appends: int or list/tuple of int) -> bool or list of bool:
            Appends value(s) to the MathSer Series if they maintain the geometric progression.
        Remove(r: int or list/tuple of int) -> bool or list of bool:
            Removes value(s) from the MathSer Series if they are at the boundaries.
        IsInSer(num: float) -> bool:
            Checks if a given number is in the MathSer Series.
    """

    def __init__(self, number_of_terms, first_term, ratio):
        """
        Initializes the GeoSer instance with the given number of terms, first term, and common ratio.

        Args:
            number_of_terms (int): Number of terms in the MathSer Series.
            first_term (float): The first term of the MathSer Series.
            ratio (float): The common ratio of the MathSer Series.

        Raises:
            ValueError: If ratio <= 0 or number_of_terms <= 0.
        """
        if ratio <= 0:
            raise ValueError('Ratio cannot be 0 or less than 0')
        if number_of_terms <= 0:
            raise ValueError('Number of terms cannot be 0 or less than 0')
        
        self.a = first_term
        self.n1 = number_of_terms
        self.r = ratio
        self.n = self.a * (self.r ** (self.n1 - 1))
        self.ser = [self.a * (self.r ** i) for i in range(self.n1)]
        self.d = None
        

    def Sum(self):
        """
        Returns:
            float: The sum of the geometric MathSer Series calculated using:
                   a * (1 - r ** n1) / (1 - r) if r != 1, else a * n1.
        """
        if self.r == 1:
            return self.a * self.n1
        return self.a * (1 - self.r ** self.n1) / (1 - self.r)

    def LastTerm(self):
        """
        Returns:
            float: The last term of the geometric MathSer Series.
        """
        return self.n

    def FullSer(self):
        """
        Returns:
            list: The complete geometric MathSer Series.
        """
        return self.ser

    def SqSum(self):
        """
        Returns:
            float: The sum of squares of all terms in the MathSer Series calculated using:
                   a^2 * (1 - r^(2*n1)) / (1 - r^2) if r != 1, else a^2 * n1.
        """
        if self.r == 1:
            return self.a ** 2 * self.n1
        return self.a ** 2 * (1 - self.r ** (2 * self.n1)) / (1 - self.r ** 2)

    def FormsUsed(self):
        """
        Returns:
            dict: A dictionary of formulas used for calculating MathSer Series values.
        """
        return {
            "Last Term": "a * (r ** (n1 - 1))",
            "Sum": "a * (1 - r ** n1) / (1 - r)  if r != 1, else a * n1",
            "Sum of Squares": "a^2 * (1 - r^(2*n1)) / (1 - r^2)  if r != 1, else a^2 * n1"
        }

    def Help(self):
        """
        Displays help documentation for the GeoSer class.
        """
        return help(GeoSer)

    # Append, Remove, and IsInSer methods remain as per your implementation.
    

    def Append(self, appends):
        """
        Appends value(s) to the geometric MathSer Series.

        Args:
            appends (int or list/tuple of int): Value(s) to append.

        Returns:
            bool or list of bool: True if appended successfully, or a list of booleans for each value; 
            False otherwise.

        Raises:
            TypeError: If the input is not an int or a list/tuple of ints.
        """
        t_f = []
        if type(appends) == int:
            if appends != self.r * self.n:
                self.ser.append(appends)
                self.n1 += 1
                self.n = self.a * (self.r ** (self.n1 - 1))
                print('Appended Successfully')
                return True
            else:
                warnings.warn('It will break some functions so it is not appended')
                return False
        elif type(appends) == list or type(appends) == tuple:
            appends = list(appends)
            appends = sorted(appends, reverse=False)
            for i in appends:
                if i != self.r * self.n:
                    self.ser.append(i)
                    print(f'Appended {i} Successfully')
                    self.n1 = len(self.ser)
                    self.n = self.a * (self.r ** (self.n1 - 1))
                    t_f.append(True)
                else:
                    warnings.warn(f'It will break some functions so {i} is not appended')
                    t_f.append(False)
            return t_f
        else:
            raise TypeError(f"The provided {appends} isn't a list/tuple/int")

    def Remove(self, r):
        """
        Removes value(s) from the geometric MathSer Series.

        Args:
            r (int or list/tuple of int): Value(s) to remove.

        Returns:
            bool or list of bool: True if removed successfully, or a list of booleans for each value; 
            False otherwise.

        Raises:
            TypeError: If the input is not an int or a list/tuple of ints, or if the value is not in the MathSer Series.
        """
        t_f = []
        if type(r) == int and self.IsInSer(r):
            if self.a == r or self.n == r:
                self.ser.remove(r)
                self.n1 = len(self.ser)
                self.n = self.a * (self.r ** (self.n1 - 1))
                print('Removed Successfully')
                return True
            else:
                warnings.warn(f'It will break some functions so {r} is not removed')
                return False
        elif type(r) == list or type(r) == tuple:
            r1 = list(r)
            r1 = sorted(r1, reverse=True)
            for i in r1:
                if self.a == i or self.n == i:
                    self.ser.remove(i)
                    self.n1 = len(self.ser)
                    self.n = self.a * (self.r ** (self.n1 - 1))
                    print('Removed Successfully')
                    t_f.append(True)
                else:
                    warnings.warn(f'It will break some functions so {i} is not removed')
                    t_f.append(False)
            return t_f
        else:
            raise TypeError(f"The provided {r} isn't a list/tuple/int or it is not in the MathSer Series")

    def IsInSer(self, num):
        """
        Checks if a number is in the geometric MathSer Series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the MathSer Series, False otherwise.
        """
        return (num - self.a) % self.r == 0 and self.a <= num <= self.n

class HardCodeMathSer(ArthSer):
    """
    HardCodeSer

    A subclass of ArthSer that allows users to define and manipulate a custom numerical MathSer Series. 
    Unlike an arithmetic MathSer Series, this class does not enforce a common difference; instead, 
    the user provides a manually chosen sequence.

    Attributes:
        ser (list[int]): The user-defined number MathSer Series.

    Methods:
        Sum() -> int:
            Returns the sum of all elements in the MathSer Series.

        SqSum() -> int:
            Returns the sum of the squares of all elements in the MathSer Series.

        Append(append: int) -> str:
            Appends an integer to the MathSer Series and returns a success message.
            Raises:
                TypeError: If the input is not an integer.

        Remove(r: int) -> None:
            Removes the given integer from the MathSer Series if it exists.
            Raises:
                ValueError: If the number is not in the MathSer Series.
                TypeError: If the input is not an integer.

        IsInSer(num: int) -> bool:
            Checks if a given number exists in the MathSer Series.

        __repr__() -> str:
            Returns a string representation of the MathSer Series.
        
    Example Usage:
        >>> hc = HardCodeSer([3, 5, 7, 9])
        >>> hc.Sum()
        24
        >>> hc.SqSum()
        164
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
            MathSer Series (list[int] or tuple[int]): The custom MathSer Series to be stored.

        Raises:
            ValueError: If the provided MathSer Series is not a list or tuple.
        """
        if not isinstance(series, (list, tuple)):
            raise ValueError('The provided MathSer Series is not a list/tuple')
        
        self.ser = list(series)

    def __repr__(self):
        """
        Returns a string representation of the MathSer Series.

        Returns:
            str: A readable representation of the MathSer Series.
        """
        return f"HardCodeSer({self.ser})"

    def Sum(self):
        """
        Returns the sum of all elements in the MathSer Series.

        Returns:
            int: The sum of the MathSer Series elements.
        """
        return sum(self.ser)
    
    def SqSum(self):
        """
        Returns the sum of squares of all elements in the MathSer Series.

        Returns:
            int: The sum of squares of the MathSer Series elements.
        """
        return sum(i**2 for i in self.ser)
    
    def Append(self, append):
        """
        Appends an integer to the MathSer Series.

        Args:
            append (int): The number to be added to the MathSer Series.

        Returns:
            str: A success message.

        Raises:
            TypeError: If the input is not an integer.
        """
        if not isinstance(append, int):
            raise TypeError('Provided append is not an integer')
        
        self.ser.append(append)
        return 'Successfully appended'
    
    def Remove(self, r):
        """
        Removes a number from the MathSer Series if it exists.

        Args:
            r (int): The number to remove.

        Raises:
            ValueError: If the number is not in the MathSer Series.
            TypeError: If the input is not an integer.
        """
        if not isinstance(r, int):
            raise TypeError("Provided value must be an integer")
        if r not in self.ser:
            raise ValueError(f"{r} is not in the MathSer Series")
        
        self.ser.remove(r)

    def IsInSer(self, num):
        """
        Checks if a number exists in the MathSer Series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the MathSer Series, False otherwise.
        """
        return num in self.ser

class HarmSer(ArthSer):
    """
    HarmSer (Harmonic MathSer Series)

    This class represents a **harmonic MathSer Series**, which is derived from an arithmetic sequence
    where each term is the reciprocal of the corresponding arithmetic sequence term.

    Inherits from:
        ArthSer: Since a harmonic MathSer Series is based on an arithmetic progression.

    Attributes:
        n1 (int): The number of terms in the MathSer Series.
        a (int or float): The first term of the arithmetic sequence.
        d (int or float): The common difference in the arithmetic sequence.
        n (int or float): The last term of the arithmetic sequence.
        ser (list of float): The harmonic MathSer Series, containing reciprocals of the arithmetic sequence terms.

    Methods:
        Sum():
            Computes and returns the sum of all terms in the harmonic MathSer Series.

        LastTerm():
            Returns the last term of the harmonic MathSer Series.

        Append():
            Raises an error, as appending values is not supported for harmonic MathSer Series.

        Remove():
            Raises an error, as removing values is not supported for harmonic MathSer Series.

        SqSum():
            Returns the sum of squares of all terms in the harmonic MathSer Series.

        __repr__():
            Returns a short description of the class.
    """

    def __init__(self, number_of_terms, first_term, difference):
        """
        Initializes the HarmSer class with the given parameters.

        Args:
            number_of_terms (int): Number of terms in the MathSer Series.
            first_term (int or float): The first term of the arithmetic sequence.
            difference (int or float): The common difference between terms.

        Attributes:
            n1 (int): Stores the number of terms.
            a (int or float): Stores the first term.
            d (int or float): Stores the common difference.
            n (int or float): Stores the last term of the arithmetic sequence.
            ser (list of float): Stores the harmonic MathSer Series.

        Raises:
            ValueError: If any term in the sequence is negative.
        """
        self.n1 = number_of_terms
        self.a = first_term
        self.d = difference
        self.n = self.a + (self.n1 - 1) * self.d
        self.ser = [1 / (self.a + i * self.d) for i in range(self.n1)]
        
        if self.a < 0 or self.d < 0 or self.n < 0:
            raise ValueError("One of the terms is less than 0")

    def Sum(self):
        """
        Computes the sum of all terms in the harmonic MathSer Series.

        Returns:
            float: The sum of the harmonic MathSer Series.
        """
        return sum(self.ser)

    def LastTerm(self):
        """
        Computes the last term of the harmonic MathSer Series.

        Returns:
            float: The reciprocal of the last term in the arithmetic sequence.
        """
        return 1 / self.n

    def Append(self, appends):
        """
        Raises an error, as appending values to a harmonic MathSer Series is not supported.

        Args:
            appends: Any input (not used).

        Raises:
            ValueError: Always raises an error since harmonic MathSer Series does not support appending terms.
        """
        raise ValueError("Append does not work in HarmSer")

    def Remove(self, appends):
        """
        Raises an error, as removing values from a harmonic MathSer Series is not supported.

        Args:
            appends: Any input (not used).

        Raises:
            ValueError: Always raises an error since harmonic MathSer Series does not support removing terms.
        """
        raise ValueError("Remove does not work in HarmSer")

    def SqSum(self):
        """
        Computes the sum of squares of all terms in the harmonic MathSer Series.

        Returns:
            float: The sum of squares of the harmonic MathSer Series terms.
        """
        return sum(i**2 for i in self.ser)

    def __repr__(self):
        """
        Returns a short description of the HarmSer class.

        Returns:
            str: A brief summary of the class.
        """
        return "HarmSer is short for Harmonic Progression MathSer Series."

    