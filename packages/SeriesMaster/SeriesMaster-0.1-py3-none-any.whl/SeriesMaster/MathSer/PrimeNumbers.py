import warnings
import matplotlib.pyplot as plt # type: ignore
from math import gcd
from functools import reduce


class Prime():
    """
    Generates and manipulates prime number MathSer Series.

    Attributes
    ----------
    lim : int
        The upper limit for generating prime numbers (exclusive).
    ser : list
        List of prime numbers generated up to `lim`.
    tempser : list
        Temporary list used during prime number generation.

    Methods
    -------
    __len__() : int
        Returns the number of prime numbers generated.
    TwinPrimes() : list
        Returns a list of twin prime pairs.
    __repr__() : str
        Returns a string representation of the prime number MathSer Series.
    Sum() : int
        Returns the sum of the prime numbers.
    Mean() : float
        Returns the mean (average) of the prime numbers.
    Append(appends) : bool or list
        Appends value(s) to the MathSer Series if they are prime.
    Remove(r) : bool or list
        Removes value(s) from the MathSer Series.
    AddSer(x) : list
        Adds a value to each element of the MathSer Series (temporary change).
    SubSer(x) : list
        Subtracts a value from each element of the MathSer Series (temporary change).
    IsInSer(num) : bool
        Checks if a number is present in the MathSer Series.
    IndexSubsetSum(start, end) : int or str
        Returns the sum of a subset of the MathSer Series within a given range.
    Plot() : None
        Plots the MathSer Series.
    SubPlot(start_index, end_index) : None
        Plots a subset of the MathSer Series.
    Help() : None
        Displays help documentation.
    GetEven() : list
        Returns even numbers in the MathSer Series.
    GetOdd() : list
        Returns odd numbers in the MathSer Series.
    Median() : float
        Returns the median of the MathSer Series.
    MulSeries(x) : list
        Multiplies each element of the MathSer Series by x.
    DivSeries(x) : list
        Divides each element of the MathSer Series by x.
    LCM() : int
        Returns the Least Common Multiple (LCM) of the MathSer Series.
    """

    def __init__(self, limit):
        """
        Initializes the Prime object with an upper limit.

        Args:
            limit (int): The upper limit (exclusive) for generating primes.
        """
        self.lim = limit
        self.ser = []
        self.tempser = list(range(2, self.lim))

        while self.tempser:
            i = self.tempser[0]
            self.ser.append(i)
            self.tempser = [j for j in self.tempser if j % i != 0]

        self.n1 = len(self.ser)  # Store the length after generation

    def __len__(self):
        """Returns the number of prime numbers generated."""
        return len(self.ser)

    def TwinPrimes(self):
        """Returns a list of twin prime pairs."""
        self.twinprimes = []
        for i in range(len(self.ser) - 1):  # Corrected range to avoid IndexError
            if self.ser[i+1] - self.ser[i] == 2:
               self.twinprimes.append((self.ser[i],self.ser[i+1]))

        return self.twinprimes

    def __repr__(self):
        """Returns a string representation of the prime number MathSer Series."""
        return f'The provided prime numbers MathSer Series is {self.ser}'

    def Sum(self):
        """Returns the sum of the prime numbers."""
        self.sum = sum(self.ser)
        return self.sum  # Return the sum, not the MathSer Series

    def Mean(self):
        """Returns the mean (average) of the prime numbers."""
        return round(self.Sum() / self.n1)

    def Append(self, appends):
        """
        Appends value(s) to the MathSer Series if they are prime.

        Args:
            appends (int or list/tuple of int): Value(s) to append.

        Returns:
            bool or list: True if a single int append was successful,
                        or a list of bools indicating success for each
                        element in a list/tuple append.
            None: If the input is not valid

        Raises:
            TypeError: If the input is not an int or a list/tuple of ints.
        """

        is_prime = lambda n: n > 1 and all(n % i for i in range(2, int(n**0.5) + 1)) if n > 1 else False

        if isinstance(appends, int):
            if is_prime(appends):
                self.ser.append(appends)
                self.n1 += 1  # Update the count
                return True
            else:
                warnings.warn('It will break some functions so it is not appended')
                return False
        elif isinstance(appends, (list, tuple)):
            appends = list(appends)  # Ensure it's a list for sorting
            appends = sorted(appends)
            t_f = []
            for i in appends:
                if is_prime(i):
                    self.ser.append(i)
                    self.n1 += 1 # Update the count
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
            bool or list: True if a single int remove was successful,
                        or a list of bools indicating success for each
                        element in a list/tuple remove.
            None: If the input is not valid

        Raises:
            TypeError: If the input is not an int or a list/tuple of ints.
        """

        if isinstance(r, int):
            if r in self.ser:
                self.ser.remove(r)
                self.n1 -= 1 # Update the count
                return True
            return False  # Return False if not found
        elif isinstance(r, (list, tuple)):
            r1 = list(r)
            t_f = []
            for item in r1:  # Iterate over the provided list/tuple
                if item in self.ser:
                    self.ser.remove(item)
                    self.n1 -= 1 # Update the count
                    t_f.append(True)
                else:
                    t_f.append(False)
            return t_f
        else:
            raise TypeError(f"The provided {r} isn't a list/tuple/int")

    # ... (rest of the methods with docstrings)

    def AddSer(self,x):
        """Add value to the MathSer Series. This is a temperory change.

        Args:
            x (int/float): The addend

        Returns:
            list: The added MathSer Series

        Raises:
            TypeError: If the input is not an int/float.
        """
        if not isinstance(x, (int, float)):
            raise TypeError('The provided input is not an int/float')
        new_ser = [i + x for i in self.ser]  # More efficient list comprehension
        return new_ser

    def SubSer(self,x):
        """Subtract value to the MathSer Series. This is a temperory change.

        Args:
            x (int/float): The minuend

        Returns:
            list: The subtracted MathSer Series
        Raises:
            TypeError: If the input is not an int/float.
        """
        if not isinstance(x, (int, float)):
            raise TypeError('The provided input is not an int/float')

        new_ser = [i - x for i in self.ser]  # More efficient list comprehension

        return new_ser


    def IsInSer(self, num):
        """Checks if a number is in the MathSer Series.

        Args:
            num (int): The number to check.

        Returns:
            bool: True if the number is in the MathSer Series, False otherwise.
        """
        return num in self.ser

    def IndexSubsetSum(self, start, end):
        """Returns the sum of a subset of the MathSer Series within a given range.

        Args:
            start (int): The starting index of the subset (inclusive).
            end (int): The ending index of the subset (exclusive).

        Returns:
            int or str: The sum of the subset or an error message if the range is invalid.

        Raises:
            TypeError: If start or end are not integers.
            IndexError: If start or end are out of range.
        """
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError("start and end must be integers")

        if start < 0 or end > len(self.ser) or start >= end:  # More robust range checking
            return "Invalid range!"

        return sum(self.ser[start:end])  # Direct sum of the slice

    def Plot(self):
        """Plots the MathSer Series using matplotlib."""
        plt.plot(self.ser, marker='o', color='red')  #Simplified plotting
        plt.title("Prime Number MathSer Series")
        plt.xlabel("Index")  # More descriptive x-axis label
        plt.ylabel("Prime Number")  # Added y-axis label
        plt.grid(True) # Added a grid for better readability
        plt.show()

    def SubPlot(self, start_index, end_index):
        """Plots a subset of the MathSer Series using matplotlib.

        Args:
            start_index (int): Starting index of the subset (inclusive).
            end_index (int): Ending index of the subset (exclusive).

        Raises:
            TypeError: If start_index or end_index are not integers.
            IndexError: If start_index or end_index are out of range.
        """
        if not isinstance(start_index, int) or not isinstance(end_index, int):
            raise TypeError("start_index and end_index must be integers")

        if start_index < 0 or end_index > len(self.ser) or start_index >= end_index:
            raise IndexError("start_index and end_index are out of range")

        subser = self.ser[start_index:end_index]
        plt.plot(subser, marker='o', color='blue')
        plt.title("Sub-Series of Prime Numbers")
        plt.xlabel("Prime Number")
        plt.ylabel("Index")
        plt.grid(True)
        plt.show()

    def Help(self):
        """Displays help documentation for the Prime class."""
        help(Prime)

    def GetEven(self):
        """Returns a list of all even numbers in the MathSer Series.

        Returns:
            list of int: Even numbers.
        """
        return [i for i in self.ser if i % 2 == 0]

    def GetOdd(self):
        """Returns a list of all odd numbers in the MathSer Series.

        Returns:
            list of int: Odd numbers.
        """
        return [i for i in self.ser if i % 2 != 0]

    def Median(self):
        """Returns the median of the MathSer Series.

        Returns:
            float: The median value.
        """
        n = len(self.ser) # Use the correct length of the MathSer Series
        if n % 2 == 1:
            return self.ser[n // 2]
        return (self.ser[n // 2 - 1] + self.ser[n // 2]) / 2

    def MulSeries(self, x):
        """Returns a new MathSer Series with each term multiplied by x.

        Args:
            x (int/float): The multiplier.

        Returns:
            list of int/float: The multiplied MathSer Series.

        Raises:
            TypeError: If the input is not an int/float.
        """
        if not isinstance(x, (int, float)):
            raise TypeError('The provided input is not an int/float')
        return [i * x for i in self.ser]

    def DivSeries(self, x):
        """Returns a new MathSer Series with each term divided by x.

        Args:
            x (int/float): The divisor.

        Returns:
            list of float: The divided MathSer Series.

        Raises:
            ValueError: If divisor is 0
            TypeError: If the input is not an int/float.
        """
        if not isinstance(x, (int, float)):
            raise TypeError('The provided input is not an int/float')
        if x == 0:
            raise ValueError('Cannot divide by 0')
        return [i / x for i in self.ser]

    def LCM(self):
        """Returns the Least Common Multiple (LCM) of the MathSer Series.

        Returns:
            int: The LCM of the MathSer Series.
        """
        if not self.ser: # Check for empty MathSer Series
            return 1 # LCM of an empty set is conventionally 1

        return reduce(lambda x, y: (x * y) // gcd(x, y), self.ser)
    

