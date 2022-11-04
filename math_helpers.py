from typing import Optional
import math

def mult_inverse(number, modulus) -> Optional[int]:
    """
    Returns x such that: number * x \equiv 1 mod modulus or none if no such x exists
    """
    if math.gcd(number, modulus) != 1:
        return None
    return 
    
