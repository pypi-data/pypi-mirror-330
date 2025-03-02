"""
This module contains the implementation of the Hamming window class.
"""

import math

from easy_fir_filter.interfaces.window_interface import IWindow
from easy_fir_filter.utils import truncate


class HammingWindow(IWindow):
    """
    Implementation of the Hamming Window.

    The Hamming window is commonly used in digital signal processing
    to reduce spectral leakage when designing FIR filters. It provides
    a good balance between main lobe width and side lobe attenuation,
    making it suitable for a wide range of applications.
    """

    def __init__(self, round_to: int = 4):
        """
        Initializes the Hamming window.

        Args:
            round_to (int, optional): Number of decimal places to round
                                      the window coefficients. Defaults to 4.
        """
        self.window_coefficients = []
        self.round_to = round_to

    def calculate_window_coefficients(
        self, n: int, filter_length: int, AS: float | None = None
    ) -> list[float]:
        """
        Computes the Hamming window coefficients.

        The formula used for calculating the coefficients is:
            w(n) = 0.54 + 0.46 * cos(2 * pi * n / (N - 1))
        Where:
            N = filter_length
            n = coefficient index (0 to N - 1)

        Args:
            n (int): The filter order.
            filter_length (int): The total length of the filter (N).
            AS (float, optional): This parameter is not used by the Hamming window.

        Returns:
            list[float]: List of Hamming window coefficients.
        """
        if n is None or filter_length is None:
            raise ValueError("The filter order and length must be provided.")

        self.window_coefficients = [
            truncate(
                0.54 + 0.46 * math.cos((2 * math.pi * i) / (filter_length - 1)),
                self.round_to,
            )
            for i in range(n + 1)
        ]

        return self.window_coefficients
