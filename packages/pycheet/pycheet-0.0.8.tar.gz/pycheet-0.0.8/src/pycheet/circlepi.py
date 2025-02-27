import math

def calculate_area(radius):
    """Calculate the area of a circle given its radius."""
    return math.pi * radius ** 2

def calculate_circumference(radius):
    """Calculate the circumference of a circle given its radius."""
    return 2 * math.pi * radius

def calculate_radius(area):
    """Calculate the radius of a circle given its area."""
    return math.sqrt(area / math.pi)