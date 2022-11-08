from typing import Optional
import math

def mult_inverse(number, modulus) -> Optional[int]:
    """
    Returns x such that: number * x % modulus = 1 
        or None if no such x exists
    """
    if math.gcd(number, modulus) != 1:
        return None
    return pow(number, -1, modulus)
    
