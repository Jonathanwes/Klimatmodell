import numpy as np

def sfär(resolution,radie=1):
    r=radie
    phi = np.linspace(0, 2*np.pi, 50)
    cx,cy,cz=0,0,0
    theta = np.linspace(0, np.pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    r_xy = r*np.sin(theta) #radie beroende av höjden
    x = cx + np.cos(phi) * r_xy 
    y = cy + np.sin(phi) * r_xy
    z = cz + r * np.cos(theta)
    new_x,new_y,new_z=[],[],[]    
    
    
    for x1,y1,z1 in zip(x,y,z): #packar upp x,y,z
        new_x.extend(x1)
        new_y.extend(y1)
        new_z.extend(z1)
    return new_x,new_y,new_z


if __name__ == "__main__":
#    import plotly.express as px
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(projection="3d")
    x,y,z=sfär(50,1)
    ax.scatter(x,y,z)


    