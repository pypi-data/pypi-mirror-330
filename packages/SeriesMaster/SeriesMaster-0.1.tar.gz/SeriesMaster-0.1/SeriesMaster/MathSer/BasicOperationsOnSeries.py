import warnings
from math import gcd  
from functools import reduce  
import SeriesMaster.MathSer.BasicOperationsOnSeries as BasicOperationsOnSeries #type:ignore


"""
    BasicOperationsOnSeries

    Performs element-wise arithmetic operations on two MathSer Series.

    This class requires two instances of the MathSer Series.Ser class that have the same length.
    It then allows you to perform basic arithmetic operations (addition, subtraction,
    multiplication, and division) on the corresponding elements of the two MathSer Series.

    Methods:
        Subtract() -> list:
            Returns a new list where each element is the result of subtracting the 
            corresponding element of ser2 from ser1.
        Add() -> list:
            Returns a new list where each element is the sum of the corresponding 
            elements of ser1 and ser2.
        Multiply() -> list:
            Returns a new list where each element is the product of the corresponding 
            elements of ser1 and ser2.
        Divide() -> list:
            Returns a new list where each element is the result of dividing the 
            corresponding element of ser1 by ser2.
        Help() -> str:
            Returns the help documentation on BasicOperationsOnSeries.
    """

    

def Subtract(ser1,ser2):
        """
        Performs element-wise subtraction between the two MathSer Series.

        Returns:
            list: A new list where each element is (ser1[i] - ser2[i]).
        """
        new_ser = []
        for i in range(len(ser1.ser)):
            new_ser.append(ser1.ser[i] -ser2.ser[i])
        return new_ser

def Add(ser1,ser2):
        """
        Performs element-wise addition of the two MathSer Series.

        Returns:
            list: A new list where each element is (ser1[i] + ser2[i]).
        """
        new_ser = []
        for i in range(len(ser1.ser)):
            new_ser.append(ser1.ser[i] + ser2.ser[i])
        return new_ser

def Multiply(ser1,ser2):
        """
        Performs element-wise multiplication of the two MathSer Series.

        Returns:
            list: A new list where each element is (ser1[i] * ser2[i]).
        """
        new_ser = []
        for i in range(len(ser1.ser)):
            new_ser.append(ser1.ser[i] * ser2.ser[i])
        return new_ser

def Divide(ser1,ser2):
        """
        Performs element-wise division of the two MathSer Series.

        Returns:
            list: A new list where each element is (ser1[i] / ser2[i]).
        """
        new_ser = []
        for i in range(len(ser1.ser)):
            if ser2.ser[i] == 0:
                raise ValueError('Cannot divide by 0')
            new_ser.append(ser1.ser[i] / ser2.ser[i])
        return new_ser
    
def Help(ser1,ser2):
        """Provides the help documentation on BasicOperationsOnSeries"""

        return help(BasicOperationsOnSeries)
