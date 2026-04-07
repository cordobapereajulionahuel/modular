"""
Módulo de operaciones matemáticas básicas
Versión: 2 (suma, resta) | 2 (multiplicar)
"""

def sumar(a: float, b: float) -> float:
    """
    Suma dos números.
    
    Args:
        a: Primer número
        b: Segundo número
    
    Returns:
        La suma de a y b
    
    Ejemplo:
        >>> sumar(5, 3)
        8
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Ambos argumentos deben ser números")
    
    return a + b


def Restar(a: float, b: float) -> float:
    """
    Resta dos números.
    
    Args:
        a: Minuendo
        b: Sustraendo
    
    Returns:
        La diferencia (a - b)
    
    Ejemplo:
        >>> Restar(10, 4)
        6
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Ambos argumentos deben ser números")
    
    return a - b


def multiplicar(a: float, b: float) -> float:
    """
    Multiplica dos números.
    
    Args:
        a: Primer factor
        b: Segundo factor
    
    Returns:
        El producto (a * b)
    
    Ejemplo:
        >>> multiplicar(10, 4)
        40
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Ambos argumentos deben ser números")
    
    return a * b


# Opcional: función para mostrar que el módulo se cargó correctamente
def __version__():
    return "2.0 - modulos"