
import numpy as np
import matplotlib.pyplot as plt
class Plotter:

    def __init__(self):
        print 'Going to plot the graphs'


    def line_plot(self,xaxis,yaxis,):
        plt.figure(1)
        plt.plot(xaxis,yaxis)
        plt.grid(True)


        plt.show()



if __name__ == '__main__':
    pltr = Plotter()
    x = [1,2,3,4,5,6]
    y = [0.1,0.2,0.3,0.4,0.5,0.4]
    pltr.line_plot(x,y)