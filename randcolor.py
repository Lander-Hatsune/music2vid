import numpy as np

def getColors(n:int):

    white = np.array([0xFF, 0xFF, 0xFF])
    colors = []
    for i in range(n - 1):
        colors.append(np.random.randint(white))
        white -= colors[-1]
    colors.append(white)
    return colors

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
