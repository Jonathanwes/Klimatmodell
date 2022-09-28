import numpy as np

def sfär(resolution,radie):
    r=radie
    phi = np.linspace(0, 2*np.pi, 2*resolution)
    theta = np.linspace(0, np.pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    
    
    cx,cy,cz=0,0,0
    r_xy = r*np.sin(theta)
    x = cx + np.cos(phi) * r_xy
    y = cy + np.sin(phi) * r_xy
    z = cz + r * np.cos(theta)
    return x,y,z

if __name__ == "__main__":
#    import plotly.express as px
    import matplotlib.pyplot as plt
    x,y,z=sfär(25,2) 
    fig=plt.figure()
    ax=fig.add_subplot(projection="3d")
    ax.scatter(x,y,z,marker="x") 