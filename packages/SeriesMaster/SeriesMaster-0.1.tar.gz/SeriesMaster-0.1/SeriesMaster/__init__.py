"""  
    Library  SeriesMaster:
    Modules:
        PatternSer:
            Classes:
                RepeatingPatternSer
                A class to create a repeating pattern SeriesMaster.

                This class allows you to create a list where the same initial value (first_row)
                is repeated for a given number of rows.

                Attributes:
                    a (any): The first row, which is repeated throughout the SeriesMaster.
                    n (int): The total number of rows in the SeriesMaster.
                    ser (list): The generated SeriesMaster with repeated values.

                Methods:
                    FullSer(): Returns the full SeriesMaster.

                    A class to create a growing pattern SeriesMaster.


                GrowingPatternSer
                This class generates a numerical sequence where each term grows by  a common ratio (geometric progression).

                Attributes:
                    d (int, optional): The common difference for an arithmetic progression. Default is 0.
                    r (int, optional): The common ratio for a geometric progression. Default is 1.
                    a (int/float): The first term of the sequence.
                    n (int): The total number of terms in the SeriesMaster.
                    ser (list): The generated growing SeriesMaster.

                Methods:
                    FullSer(): Returns the full SeriesMaster.
        HardCodeSer:
            Classes:
            HardCodeSer:
                        
                Takes any SeriesMaster

                Attributes:
                    ser (list[any]): The user-defined SeriesMaster.

                Methods:
                

                    Append(append: any) -> str:
                        Appends an anything to the SeriesMaster and returns a success message.
                        

                    Remove(r: any) -> None:
                        Removes the given anything from the SeriesMaster if it exists.
                        Raises:
                            ValueError: If the number is not in the SeriesMaster.
            

                    IsInSer(char: any) -> bool:
                        Checks if a given char exists in the SeriesMaster.

                    __repr__() -> str:
                        Returns a string representation of the SeriesMaster.
                    
                Example Usage:
                    >>> hc = HardCodeSer([3, 5, 7, 9])
                    >>> hc.Append(11)
                    'Successfully appended'
                    >>> hc.Remove(5)
                    >>> hc.IsInSer(7)
                    True
    Packages:
                
Package: MathSer SeriesMaster  

This module provides tools for working with different types of mathematical MathSer SeriesMaster, including **Arithmetic**, **Geometric**, and **Fibonacci** MathSer SeriesMaster.  
It also includes a utility class for performing element-wise arithmetic operations between two MathSer SeriesMaster.

Modules:


Package: MathSer SeriesMaster  

This module provides tools for working with different types of mathematical MathSer SeriesMaster, including **Arithmetic**, **Geometric**, **Fibonacci**, **Tribonacci**, and **Hardcoded MathSer SeriesMaster**.  
It also includes a utility class for performing element-wise arithmetic operations between two MathSer SeriesMaster.

Modules:
    Factors:
    Classes:
        Factors:
                A class that generates and operates on the factors of a given number.
    
    PasTri:
    Classes:
        PasTri:
    

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
            - `MulSeriesMaster(x)`: Multiplies each element in the row by `x`.
            - `DivSeriesMaster(x)`: Divides each element in the row by `x`.
            - `LCM()`: Returns the least common multiple of the row elements.

            Usage Example:
            --------------
            ```python
            pascal_row = PasTri(5)
            print(pascal_row.FullSer())  # Output: (1, 5, 10, 10, 5, 1)
            print(pascal_row.Sum())      # Output: 32
            ```
    ProgSer:
    Classes:

        ArthSer:
            Represents and manipulates an **arithmetic MathSer SeriesMaster**.

            Attributes:
                n1 (int): The number of terms in the MathSer SeriesMaster.
                a (int): The first term of the MathSer SeriesMaster.
                d (int): The common difference between consecutive terms.
                n (int): The last term of the MathSer SeriesMaster (calculated as a + (n1 - 1) * d).
                ser (list of int): The full arithmetic MathSer SeriesMaster stored as a list.

            Methods:
                __init__(number_of_terms, first_term, difference):
                    Initializes an arithmetic MathSer SeriesMaster with the specified number of terms, first term, and common difference.

                Sum() -> int:
                    Returns the sum of all terms in the MathSer SeriesMaster.

                LastTerm() -> int:
                    Returns the last term of the MathSer SeriesMaster.

                FullSer() -> tuple:
                    Returns the entire MathSer SeriesMaster as a tuple.

                SqSum() -> int:
                    Returns the sum of the squares of the terms in the MathSer SeriesMaster.

                FormsUsed() -> dict:
                    Returns a dictionary containing the formulas used in calculations.

                Mean() -> float:
                    Returns the arithmetic mean (average) of the MathSer SeriesMaster.

                Append(appends) -> bool or list[bool]:
                    Appends a value or a list/tuple of values to the MathSer SeriesMaster.
                    Note: The appended values must maintain the arithmetic progression.

                Remove(r) -> bool or list[bool]:
                    Removes a value or a list/tuple of values from the MathSer SeriesMaster.
                    Note: Only the first or last element of the MathSer SeriesMaster can be removed without breaking the progression.

                IsInSer(num) -> bool:
                    Checks if a number is in the arithmetic MathSer SeriesMaster.

                IndexSubsetSum(start, end) -> int or str:
                    Returns the sum of a subset of the MathSer SeriesMaster within a specified range.

                PrimeNumbers() -> list[int]:
                    Returns a list of prime numbers present in the MathSer SeriesMaster.

                Plot():
                    Plots the MathSer SeriesMaster using matplotlib.

                SubPlot(start_index, end_index):
                    Plots a subset of the MathSer SeriesMaster.

                Help():
                    Displays help documentation for the class.

                GetEven() -> list[int]:
                    Returns a list of all even numbers in the MathSer SeriesMaster.

                GetOdd() -> list[int]:
                    Returns a list of all odd numbers in the MathSer SeriesMaster.

                Median() -> float:
                    Returns the median of the MathSer SeriesMaster.

                MulSeriesMaster(x) -> list[int]:
                    Returns a new MathSer SeriesMaster with each term multiplied by x.

                DivSeriesMaster(x) -> list[float]:
                    Returns a new MathSer SeriesMaster with each term divided by x.

                LCM() -> int:
                    Returns the least common multiple of all terms in the MathSer SeriesMaster.

        HardCodeSer:
            Allows users to define and manipulate a manually created numerical MathSer SeriesMaster. 
            Unlike an arithmetic or geometric MathSer SeriesMaster, this class lets users input their own 
            sequences without enforcing any mathematical pattern.

            Attributes:
                ser (list[int]): The user-defined number MathSer SeriesMaster.

            Methods:
                __init__(SeriesMaster: list[int] or tuple[int]):
                    Initializes the class with a manually defined number sequence.

                Sum() -> int:
                    Returns the sum of all elements in the MathSer SeriesMaster.

                SqSum() -> int:
                    Returns the sum of the squares of all elements in the MathSer SeriesMaster.

                Append(append: int) -> str:
                    Appends an integer to the MathSer SeriesMaster and returns a success message.
                    Raises:
                        TypeError: If the input is not an integer.

                Remove(r: int) -> None:
                    Removes the given integer from the MathSer SeriesMaster if it exists.
                    Raises:
                        ValueError: If the number is not in the MathSer SeriesMaster.
                        TypeError: If the input is not an integer.

                IsInSer(num: int) -> bool:
                    Checks if a given number exists in the MathSer SeriesMaster.

                __repr__() -> str:
                    Returns a string representation of the MathSer SeriesMaster.

        GeoSer:
            Represents and manipulates a **geometric MathSer SeriesMaster**.

            Attributes:
                n1 (int): The number of terms in the MathSer SeriesMaster.
                a (int): The first term of the MathSer SeriesMaster.
                r (int): The common ratio between consecutive terms.
                n (int): The last term of the MathSer SeriesMaster (calculated as a * r^(n1-1)).
                ser (list of int): The full geometric MathSer SeriesMaster stored as a list.

            Methods:
                __init__(number_of_terms, first_term, ratio):
                    Initializes a geometric MathSer SeriesMaster with the given parameters.

                Sum() -> float:
                    Returns the sum of the geometric MathSer SeriesMaster.

                LastTerm() -> int:
                    Returns the last term of the MathSer SeriesMaster.

                FullSer() -> list[int]:
                    Returns the entire MathSer SeriesMaster.

                SqSum() -> float:
                    Returns the sum of the squares of the terms in the MathSer SeriesMaster.

                FormsUsed() -> dict:
                    Returns a dictionary containing formulas used in calculations.

                Append(appends) -> bool or list[bool]:
                    Appends a value or a list/tuple of values to the MathSer SeriesMaster.
                    Note: The appended values must maintain the geometric progression.

                Remove(r) -> bool or list[bool]:
                    Removes a value or a list/tuple of values from the MathSer SeriesMaster.
                    Note: Only the first or last element of the MathSer SeriesMaster can be removed without breaking the progression.

                Help():
                    Displays help documentation for the class.

    HarmSer (Harmonic MathSer SeriesMaster)

    This class represents a **harmonic MathSer SeriesMaster**, which is derived from an arithmetic sequence
    where each term is the reciprocal of the corresponding arithmetic sequence term.

    Inherits from:
        ArthSer: Since a harmonic MathSer SeriesMaster is based on an arithmetic progression.

    Attributes:
        n1 (int): The number of terms in the MathSer SeriesMaster.
        a (int or float): The first term of the arithmetic sequence.
        d (int or float): The common difference in the arithmetic sequence.
        n (int or float): The last term of the arithmetic sequence.
        ser (list of float): The harmonic MathSer SeriesMaster, containing reciprocals of the arithmetic sequence terms.

    Methods:
        Sum():
            Computes and returns the sum of all terms in the harmonic MathSer SeriesMaster.

        LastTerm():
            Returns the last term of the harmonic MathSer SeriesMaster.

        Append():
            Raises an error, as appending values is not supported for harmonic MathSer SeriesMaster.

        Remove():
            Raises an error, as removing values is not supported for harmonic MathSer SeriesMaster.

        SqSum():
            Returns the sum of squares of all terms in the harmonic MathSer SeriesMaster.

        __repr__():
            Returns a short description of the class.

        Exceptions:
            ValueError: Raised for invalid input values (e.g., negative terms in MathSer SeriesMaster initialization, appending/removing values that break the progression).
            TypeError: Raised when performing operations between incompatible MathSer SeriesMaster.
            IndexError: Raised if two MathSer SeriesMaster do not have the same length (in BasicOperationsOnSeriesMaster).
            ZeroDivisionError: Raised when attempting to divide by zero in DivSeriesMaster() or BasicOperationsOnSeriesMaster.Divide().

    Example Usage:

        >>> s1 = ArthSer(5, 2, 3)  # Arithmetic MathSer SeriesMaster: 2, 5, 8, 11, 14
        >>> s1.Sum()
        40
        >>> s2 = GeoSer(5, 3, 2)  # Geometric MathSer SeriesMaster: 3, 6, 12, 24, 48
        >>> s2.Sum()
        93
        >>> hc = HardCodeSer([3, 5, 7, 9])  # Manually defined MathSer SeriesMaster
        >>> hc.Sum()
        24
        >>> hc.SqSum()
        164
        >>> hc.Append(11)
        'Successfully appended'
        >>> hc.Remove(5)
        >>> hc.IsInSer(7)
        True


    FibSer:
        Represents and manipulates a **Fibonacci MathSer SeriesMaster**.

        Attributes:
            n (int): The number of terms in the Fibonacci MathSer SeriesMaster.
            ser (list of int): The full Fibonacci MathSer SeriesMaster stored as a list.

        Methods:
            __init__(number_of_terms):
                Initializes a Fibonacci MathSer SeriesMaster with the given number of terms.

            FullSer() -> list[int]:
                Returns the entire MathSer SeriesMaster.

            LastTerm() -> int:
                Returns the last term of the MathSer SeriesMaster.

            Sum() -> int:
                Returns the sum of all terms in the Fibonacci MathSer SeriesMaster.

            IsInSer(num) -> bool:
                Checks if a number exists in the Fibonacci MathSer SeriesMaster.

            PrimeNumbers() -> list[int]:
                Returns a list of prime numbers present in the Fibonacci MathSer SeriesMaster.

            IndexSubsetSum(start, end) -> int:
                Returns the sum of a subset of the Fibonacci MathSer SeriesMaster.

            GetEven() -> list[int]:
                Returns a list of all even numbers in the Fibonacci MathSer SeriesMaster.

            GetOdd() -> list[int]:
                Returns a list of all odd numbers in the Fibonacci MathSer SeriesMaster.

            Median() -> float:
                Returns the median of the Fibonacci MathSer SeriesMaster.

            MulSeriesMaster(x) -> list[int]:
                Returns a new MathSer SeriesMaster with each term multiplied by x.

            DivSeriesMaster(x) -> list[float]:
                Returns a new MathSer SeriesMaster with each term divided by x.

            LCM() -> int:
                Returns the least common multiple of all terms in the Fibonacci MathSer SeriesMaster.

            Plot():
                Plots the Fibonacci MathSer SeriesMaster using matplotlib.

            SubPlot(start_index, end_index):
                Plots a subset of the Fibonacci MathSer SeriesMaster.

            Help():
                Displays help documentation for the class.

    TribSer (Tribonacci MathSer SeriesMaster)

        This class generates a Tribonacci MathSer SeriesMaster and provides various methods
        to analyze and manipulate it.

        Attributes
        ----------
        n : int
            The number of terms in the MathSer SeriesMaster.
        ser : list
            The Tribonacci sequence up to `n` terms.

        Methods
        -------
        FullSer() : list
            Returns the complete Tribonacci MathSer SeriesMaster.
        LastTerm() : int
            Returns the last term of the Tribonacci MathSer SeriesMaster.
        IsInSer(num: int) : bool
            Checks if a given number is present in the Tribonacci MathSer SeriesMaster.
        IndexSubsetSum(start_idx: int, end_idx: int) : int
            Returns the sum of Tribonacci numbers between two indices.
        PrimeNumbers() : list
            Returns a list of prime numbers found in the MathSer SeriesMaster.
        Plot() : None
            Plots the Tribonacci MathSer SeriesMaster.
        SubPlot(start_index: int, end_index: int) : None
            Plots a subset of the Tribonacci MathSer SeriesMaster.
        GetEven() : list
            Returns a list of all even Tribonacci numbers.
        GetOdd() : list
            Returns a list of all odd Tribonacci numbers.
        Median() : float
            Returns the median value of the MathSer SeriesMaster.
        MulSeriesMaster(x) : list
            Returns a new MathSer SeriesMaster with each term multiplied by `x`.
        DivSeriesMaster(x) : list
            Returns a new MathSer SeriesMaster with each term divided by `x`.
        AddSer(x) : list
            Returns a new MathSer SeriesMaster with each term added by `x`.
        SubSer(x) : list
            Returns a new MathSer SeriesMaster with each term subtracted by `x`.
        LCM() : int
            Returns the Least Common Multiple (LCM) of the MathSer SeriesMaster.
        Help() : None
            Displays help documentation for the TribSer class.

        Examples
        --------
        >>> trib = TribSer(10)
        >>> trib.FullSer()
        [1, 1, 2, 4, 7, 13, 24, 44, 81, 149]
        >>> trib.LastTerm()
        149
        

    BasicOperationsOnSeriesMaster:
        Performs element-wise operations on two MathSer SeriesMaster (Arithmetic, Geometric, Fibonacci or Tribonacci).

        Attributes:
            ser1 (ArthSer | GeoSer | FibSer): The first MathSer SeriesMaster.
            ser2 (ArthSer | GeoSer | FibSer): The second MathSer SeriesMaster.

        Methods:
            Subtract(ser1,ser2) -> list[int]:
                Returns a new list where each element is the result of subtracting the 
                corresponding element of ser2 from ser1.

            Add(ser1,ser2) -> list[int]:
                Returns a new list where each element is the sum of the corresponding 
                elements of ser1 and ser2.

            Multiply(ser1,ser2) -> list[int]:
                Returns a new list where each element is the product of the corresponding 
                elements of ser1 and ser2.

            Divide(ser,ser2) -> list[float]:
                Returns a new list where each element is the result of dividing the 
                corresponding element of ser1 by ser2.

        BonAcci:
        Classes:
        FibSer:
        Represents and manipulates a **Fibonacci MathSer SeriesMaster**.

        Attributes:
            n (int): The number of terms in the Fibonacci MathSer SeriesMaster.
            ser (list of int): The full Fibonacci MathSer SeriesMaster stored as a list.

        Methods:
            __init__(number_of_terms):
                Initializes a Fibonacci MathSer SeriesMaster with the given number of terms.

            FullSer() -> list[int]:
                Returns the entire MathSer SeriesMaster.

            LastTerm() -> int:
                Returns the last term of the MathSer SeriesMaster.

            Sum() -> int:
                Returns the sum of all terms in the Fibonacci MathSer SeriesMaster.

            IsInSer(num) -> bool:
                Checks if a number exists in the Fibonacci MathSer SeriesMaster.

            PrimeNumbers() -> list[int]:
                Returns a list of prime numbers present in the Fibonacci MathSer SeriesMaster.

            IndexSubsetSum(start, end) -> int:
                Returns the sum of a subset of the Fibonacci MathSer SeriesMaster.

            GetEven() -> list[int]:
                Returns a list of all even numbers in the Fibonacci MathSer SeriesMaster.

            GetOdd() -> list[int]:
                Returns a list of all odd numbers in the Fibonacci MathSer SeriesMaster.

            Median() -> float:
                Returns the median of the Fibonacci MathSer SeriesMaster.

            MulSeriesMaster(x) -> list[int]:
                Returns a new MathSer SeriesMaster with each term multiplied by x.

            DivSeriesMaster(x) -> list[float]:
                Returns a new MathSer SeriesMaster with each term divided by x.

            LCM() -> int:
                Returns the least common multiple of all terms in the Fibonacci MathSer SeriesMaster.

            Plot():
                Plots the Fibonacci MathSer SeriesMaster using matplotlib.

            SubPlot(start_index, end_index):
                Plots a subset of the Fibonacci MathSer SeriesMaster.

            Help():
                Displays help documentation for the class.

    TribSer (Tribonacci MathSer SeriesMaster)

        This class generates a Tribonacci MathSer SeriesMaster and provides various methods
        to analyze and manipulate it.

        Attributes
        ----------
        n : int
            The number of terms in the MathSer SeriesMaster.
        ser : list
            The Tribonacci sequence up to `n` terms.

        Methods
        -------
        FullSer() : list
            Returns the complete Tribonacci MathSer SeriesMaster.
        LastTerm() : int
            Returns the last term of the Tribonacci MathSer SeriesMaster.
        IsInSer(num: int) : bool
            Checks if a given number is present in the Tribonacci MathSer SeriesMaster.
        IndexSubsetSum(start_idx: int, end_idx: int) : int
            Returns the sum of Tribonacci numbers between two indices.
        PrimeNumbers() : list
            Returns a list of prime numbers found in the MathSer SeriesMaster.
        Plot() : None
            Plots the Tribonacci MathSer SeriesMaster.
        SubPlot(start_index: int, end_index: int) : None
            Plots a subset of the Tribonacci MathSer SeriesMaster.
        GetEven() : list
            Returns a list of all even Tribonacci numbers.
        GetOdd() : list
            Returns a list of all odd Tribonacci numbers.
        Median() : float
            Returns the median value of the MathSer SeriesMaster.
        MulSeriesMaster(x) : list
            Returns a new MathSer SeriesMaster with each term multiplied by `x`.
        DivSeriesMaster(x) : list
            Returns a new MathSer SeriesMaster with each term divided by `x`.
        AddSer(x) : list
            Returns a new MathSer SeriesMaster with each term added by `x`.
        SubSer(x) : list
            Returns a new MathSer SeriesMaster with each term subtracted by `x`.
        LCM() : int
            Returns the Least Common Multiple (LCM) of the MathSer SeriesMaster.
        Help() : None
            Displays help documentation for the TribSer class.

        Examples
        --------
        >>> trib = TribSer(10)
        >>> trib.FullSer()
        [1, 1, 2, 4, 7, 13, 24, 44, 81, 149]
        >>> trib.LastTerm()
        149

        PrimeNumbers:
        Classes:
        Primes:
    
        Generates and manipulates prime number MathSer SeriesMaster.

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
            Returns a string representation of the prime number MathSer SeriesMaster.
        Sum() : int
            Returns the sum of the prime numbers.
        Mean() : float
            Returns the mean (average) of the prime numbers.
        Append(appends) : bool or list[bool]
            Appends value(s) to the MathSer SeriesMaster if they are prime.
        Remove(r) : bool or list[bool]
            Removes value(s) from the MathSer SeriesMaster.
        AddSer(x) : list
            Adds a value to each element of the MathSer SeriesMaster (temporary change).
        SubSer(x) : list
            Subtracts a value from each element of the MathSer SeriesMaster (temporary change).
        IsInSer(num) : bool
            Checks if a number is present in the MathSer SeriesMaster.
        IndexSubsetSum(start, end) : int or str
            Returns the sum of a subset of the MathSer SeriesMaster within a given range.
        Plot() : None
            Plots the MathSer SeriesMaster.
        SubPlot(start_index, end_index) : None
            Plots a subset of the MathSer SeriesMaster.
        Help() : None
            Displays help documentation.
        GetEven() : list
            Returns even numbers in the MathSer SeriesMaster.
        GetOdd() : list
            Returns odd numbers in the MathSer SeriesMaster.
        Median() : float
            Returns the median of the MathSer SeriesMaster.
        MulSeriesMaster(x) : list
            Multiplies each element of the MathSer SeriesMaster by x.
        DivSeriesMaster(x) : list
            Divides each element of the MathSer SeriesMaster by x.
        LCM() : int
            Returns the Least Common Multiple (LCM) of the MathSer SeriesMaster.
        
    
    LucasSer:

    Classes:
    LucasSer:

    This class generates a Lucas MathSer SeriesMaster, which is similar to the Fibonacci MathSer SeriesMaster.
    The Lucas MathSer SeriesMaster starts with the terms 1 and 2, instead of 0 and 1 as in the Fibonacci MathSer SeriesMaster.

    Inherits from:
        BonAcci.FibSer: This class extends the Fibonacci MathSer SeriesMaster class.

    Attributes:
        n1 (int): The number of terms to generate in the Lucas MathSer SeriesMaster.
        ser (list): A list containing the terms of the Lucas MathSer SeriesMaster.

    Methods:
        __init__(self, number_of_terms):
            Initializes the Lucas MathSer SeriesMaster with a given number of terms.
        
        IsInSer(self, num):
            Checks if a given number is part of the Lucas MathSer SeriesMaster.

        __repr__(self):
            Provides a string representation of the Lucas MathSer SeriesMaster class.   


    #ExponentialSer

    ## Module Overview
    This module provides a class, `SquareSer`,`CubicSer` for generating and analyzing a squared arithmetic MathSer SeriesMaster.
    The class creates a sequence where each term is the square of an arithmetic sequence term and provides
    various utility functions for analysis, transformation, and visualization.

    ## Dependencies
    This module requires the following libraries:
    - `warnings` (for potential future warnings)
    - `math` (for mathematical operations)
    - `matplotlib.pyplot` (for plotting the MathSer SeriesMaster)
    - `functools.reduce` (for LCM calculation)

    ## Class: SquareSer
    ### Description
    The `SquareSer` class generates a squared arithmetic MathSer SeriesMaster and offers methods to analyze, modify, and visualize the MathSer SeriesMaster.

    ### Attributes
    - `n1` *(int)*: Number of terms in the MathSer SeriesMaster.
    - `a` *(int)*: First term of the arithmetic MathSer SeriesMaster.
    - `d` *(int)*: Common difference of the arithmetic MathSer SeriesMaster.
    - `n` *(int)*: Last term of the arithmetic MathSer SeriesMaster.
    - `ser` *(list of int)*: List containing the squared terms of the arithmetic MathSer SeriesMaster.

    ### Methods

    #### MathSer SeriesMaster Information & Analysis
    - `LastTerm() -> int`
    Returns the last term of the arithmetic MathSer SeriesMaster.

    - `FullSer() -> tuple`
    Returns the complete squared MathSer SeriesMaster as a tuple.

    - `Sum() -> int`
    Computes the sum of all squared terms in the MathSer SeriesMaster.

    - `Mean() -> int`
    Computes the mean (average) of the squared MathSer SeriesMaster.

    - `Median() -> int or float`
    Returns the median value of the MathSer SeriesMaster.

    - `LCM() -> int`
    Computes the least common multiple (LCM) of all terms in the MathSer SeriesMaster.

    - `FormsUsed() -> dict`
    Returns a dictionary of formulas used in MathSer SeriesMaster calculations.

    #### Filtering & Checking
    - `GetEven() -> list`
    Returns a list of even numbers in the MathSer SeriesMaster.

    - `GetOdd() -> list`
    Returns a list of odd numbers in the MathSer SeriesMaster.

    - `IsInSer(num: int) -> bool`
    Checks if a given number exists in the MathSer SeriesMaster.

    - `PrimeNumbers() -> list`
    Returns the prime numbers present in the MathSer SeriesMaster.

    #### Subset & Index Operations
    - `IndexSubsetSum(start: int, end: int) -> int or str`
    Computes the sum of a subset of the MathSer SeriesMaster based on a given range.

    #### Modifying the MathSer SeriesMaster (Temporary Changes)
    - `AddSer(x: int) -> list`
    Returns a modified MathSer SeriesMaster with each term incremented by `x`.

    - `SubSer(x: int) -> list`
    Returns a modified MathSer SeriesMaster with each term decremented by `x`.

    - `MulSeriesMaster(x: int) -> list`
    Returns a modified MathSer SeriesMaster with each term multiplied by `x`.

    - `DivSeriesMaster(x: int) -> list`
    Returns a modified MathSer SeriesMaster with each term divided by `x`.
    - **Raises** `ValueError` if `x == 0`.

    #### Visualization
    - `Plot()`
    Generates a plot of the MathSer SeriesMaster using `matplotlib`.

    - `SubPlot(start_index: int, end_index: int)`
    Generates a plot of a subset of the MathSer SeriesMaster.

    #### Utility & Help
    - `Help()`
    Displays the documentation for the `SquareSer` class.

    CubicSer
    A class to represent a cubic sequence derived from an arithmetic sequence.

        Inherits from:
            SquareSer (Assuming SquareSer is a class that handles square MathSer SeriesMaster)

        Attributes:
            n1 (int): Number of terms in the MathSer SeriesMaster.
            a (int or float): First term of the MathSer SeriesMaster.
            d (int or float): Common difference between terms.
            n (int or float): Last term before applying the cubic operation.
            ser (list): List containing the cubic values of the arithmetic MathSer SeriesMaster.

        Methods:
            Sum():
                Returns the sum of the cubic MathSer SeriesMaster.

            LastTerm():
                Returns the last term of the MathSer SeriesMaster raised to the power of 3.

            FormsUsed():
                Returns a dictionary of formulas used in calculations.

    ### Example Usage
    ```python
    from square_SeriesMaster_module import SquareSer

    # Create a squared arithmetic MathSer SeriesMaster
    ser = SquareSer(5, 2, 3)

    # Get the full squared MathSer SeriesMaster
    print(ser.FullSer())  # Output: (4, 25, 64, 121, 196)

    # Compute the sum of the MathSer SeriesMaster
    print(ser.Sum())  # Output: 410

    # Get all even numbers in the MathSer SeriesMaster
    print(ser.GetEven())  # Output: [4, 64, 196]

    # Check if a number exists in the MathSer SeriesMaster
    print(ser.IsInSer(25))  # Output: True

    # Get prime numbers from the MathSer SeriesMaster
    print(ser.PrimeNumbers())  # Output: [5]

    # Plot the MathSer SeriesMaster
    ser.Plot()
Exceptions:
    ValueError: Raised for invalid input values (e.g., negative terms in MathSer SeriesMaster initialization, appending/removing values that break the progression).
    TypeError: Raised when performing operations between incompatible MathSer SeriesMaster.
    IndexError: Raised if two MathSer SeriesMaster do not have the same length (in BasicOperationsOnSeriesMaster).
    ZeroDivisionError: Raised when attempting to divide by zero in DivSeriesMaster() or BasicOperationsOnSeriesMaster.Divide().

Example Usage:

    >>> s1 = ArthSer(5, 2, 3)  # Arithmetic MathSer SeriesMaster: 2, 5, 8, 11, 14
    >>> s1.Sum()
    40
    >>> s2 = GeoSer(5, 3, 2)  # Geometric MathSer SeriesMaster: 3, 6, 12, 24, 48
    >>> s2.Sum()
    93
    >>> fib = FibSer(7)  # Fibonacci MathSer SeriesMaster: 1, 1, 2, 3, 5, 8, 13
    >>> fib.Sum()
    33
    >>> ops = BasicOperationsOnSeriesMaster(s1, s2)
    >>> ops.Add()
    [5, 11, 20, 35, 62]
            """

import SeriesMaster.MathSer #type:ignore
import SeriesMaster.PatternSer #type:ignore
import SeriesMaster.HardCodeSer #type:ignore


