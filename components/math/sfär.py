import numpy as np

def sfär(resolution,radie):
    r=radie
    phi = np.linspace(0, 2*np.pi, 50)
    cx,cy,cz=0,0,0
    theta = np.linspace(0, np.pi, resolution)
    
    theta, phi = np.meshgrid(theta, phi)
    
    r_xy = r*np.sin(theta) #radie beroende av höjden
    x = cx + np.cos(phi) * r_xy 
    y = cy + np.sin(phi) * r_xy
    z = cz + r * np.cos(theta)
    return x,y,z


if __name__ == "__main__":
#    import plotly.express as px
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(projection="3d")
    x,y,z=sfär(50,1)
    ax.scatter(x,y,z)
#%%


    