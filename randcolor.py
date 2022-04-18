from matplotlib.colors import hsv_to_rgb
import numpy as np

def get3Colors(seed:int):
    randhue = (seed % 814) / 814 / 3
    decimal = lambda x: x - int(x)
    c1 = hsv_to_rgb((randhue, 1, 1))
    c2 = hsv_to_rgb((randhue + 1/3, 1, 1))
    c3 = hsv_to_rgb((randhue + 2/3, 1, 1))
    return (c1, c2, c3)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
