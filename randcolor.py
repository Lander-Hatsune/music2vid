import numpy as np

def get3Colors(seed:int=814):

    np.random.seed(seed)
    randc = lambda: np.random.random() * 0.5
    r = (1, randc(), randc())
    g = (randc(), 1, randc())
    b = (randc(), randc(), 1)
    return (r, g, b)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
