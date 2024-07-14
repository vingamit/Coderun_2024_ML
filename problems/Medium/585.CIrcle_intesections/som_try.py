import numpy as np

def is_inside_circles(x, y, centers, radii):
    return all((x - cx)**2 + (y - cy)**2 <= r**2 for (cx, cy), r in zip(centers, radii))

def integrand(x, y, centers, radii):
    return 1.0 if is_inside_circles(x, y, centers, radii) else 0.0

def simpson_double_integral(f, xa, xb, ya, yb, nx, ny, *args):
    hx = (xb - xa) / nx
    hy = (yb - ya) / ny
    
    integral = 0.0
    
    for i in range(nx + 1):
        for j in range(ny + 1):
            x = xa + i * hx
            y = ya + j * hy
            
            coef = 1
            if i in (0, nx): coef *= 1/3
            if j in (0, ny): coef *= 1/3
            if 0 < i < nx: coef *= 4/3 if i % 2 else 2/3
            if 0 < j < ny: coef *= 4/3 if j % 2 else 2/3
            
            integral += coef * f(x, y, *args)
    
    return integral * hx * hy

# Пример использования
centers = [(2, 2), (1, 1), (9, 2)]
radii = [6, 6, 4]

xa, xb = 5, 7
ya, yb = -2, 5
nx, ny = 10000, 10000

area = simpson_double_integral(integrand, xa, xb, ya, yb, nx, ny, centers, radii)
print(f"Площадь пересечения: {area}")