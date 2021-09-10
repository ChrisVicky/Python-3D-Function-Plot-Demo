import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import expr_np

X_L = -4
X_R = 4
X_STEP = 0.25
Y_L = -4
Y_R = 4
Y_STEP = 0.25

while(1):
    X = np.arange(X_L, X_R, X_STEP, dtype=np.float32)
    Y = np.arange(Y_L, Y_R, Y_STEP, dtype=np.float32)
    X, Y = np.meshgrid(X, Y)
    func = ""
    while(func==""):
        expr_np.War("Note that 'inf' can hardly be presented")
        func = input("\33[1;35mInput a Function:\33[0m\n\33[1;32mz=")
    Z, flag, name = expr_np.DO(func, X, Y)
    if(flag==False):
        plt.close('all')
        continue
    expr_np.Success("Building 3D Graph. . . . . .")
    name = "z="+name
    fig = plt.figure(name)
    ax = Axes3D(fig)
#    ax.plot_surface(X,Y,Z, rstride=X_STEP, cstride=Y_STEP, color='b', cmap=plt.cm.coolwarm, label="test_label")
#    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, color='b',  label="test_label")
#    ax.plot_surface(X,Y,Z, rstride=0.25, cstride=0.25, cmap=plt.cm.coolwarm)
    ax.plot_surface(X,Y,Z, cmap=plt.cm.coolwarm)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(name)
    path = "./figure/" + name.replace("/", " divide ") + ".png"
  #   plt.savefig(path)
  #  expr_np.Success(f"picture saved to {path}")
  #  expr_np.Success("")

    plt.show()
    plt.close('all')
    
