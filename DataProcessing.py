import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# from scipy.interpolate import interp1d

class dataset(object):
    def __init__(self,filename):
        with open(filename, 'r') as f:
            data = f.read()
            self.x = np.array([int(line.split(',')[0]) for line in data.split('\n') if line])
            self.set_x = set(self.x)
            self.y = np.array([round(float(line.split(',')[1]),4) for line in data.split('\n') if line])

    def get_x(self):
        return self.x

    def get_set_x(self):
        return self.set_x

    def get_y(self):
        return self.y

    def scatter_plot(self,show = False):
        x = self.get_x()
        y = self.get_y()
        plt.scatter(x,y,label = 'Scatter',c='gray')
        if show:
            plt.show()

    def mean_and_std_line(self,plot = [0,0],show = False):
        mean_data = {x: [] for x in self.get_set_x()}
        length = len(self.get_x())

        x = self.get_x()
        y = self.get_y()

        for index in range(length):
            mean_data[x[index]].append(y[index])

        x_averaged = np.array(list(mean_data.keys()))
        y_averaged = np.array([np.average(mean_data[key]) for key in mean_data])
        y_std = np.array([np.std(mean_data[key]) for key in mean_data])

        if plot[0]:
            plt.plot(x_averaged,y_averaged,label = 'Mean')
        if plot[1]:
            plt.plot(x_averaged,y_averaged+2*y_std,label = '+ 2std')
            plt.plot(x_averaged,y_averaged-2*y_std,label = '- 2std')
        if show:
            plt.show()

        return x_averaged,y_averaged

    def calculate_mse(self,y_estimated):
        y = self.mean_and_std_line()[1]

        return (np.sum((y-y_estimated)**2)/len(y))**0.5

    def linear_regression(self,degree):
        x,y = self.mean_and_std_line()
        half_length = int(len(x))

        return np.polyfit(x[:half_length],y[:half_length],degree)

    def best_linear_regression(self,degrees):
        x = self.mean_and_std_line()[0]
        best_degree = None

        for degree in degrees:
           mse = self.calculate_mse(np.polyval(self.linear_regression(degree),x))
           if not(best_degree) or mse < best_degree:
               best_degree = degree

        return best_degree

    def plot_linear_models(self,degrees,show = False):
        x = self.mean_and_std_line()[0]

        for degree in degrees:
            if degree == 1:
                coeffs = self.linear_regression(degree)
                y_estimate = np.polyval(coeffs,x)
                slope = coeffs[0]
                mse = self.calculate_mse(y_estimate)
                plt.plot(x,y_estimate,label=f'Degree (Slope, MSE): {degree} ({round(slope,3)},{round(mse,3)})')
            else:
                y_estimate = np.polyval(self.linear_regression(degree),x)
                mse = self.calculate_mse(y_estimate)
                plt.plot(x,y_estimate,label=f'Degree (MSE): {degree} ({round(mse,3)})')
        if show:
            plt.show()

    def exponential_model(self,exponent):
        x,y = self.mean_and_std_line()
        half_length = int(len(x))

        f = lambda x,a: a * x**(exponent)
        return curve_fit(f,x,y)[0]

    def plot_exponential_models(self,exponents,show = False):
        x = self.mean_and_std_line()[0]

        for e in exponents:
            a = self.exponential_model(e)[0]
            y_estimate = a * x**e
            mse = self.calculate_mse(y_estimate)
            plt.plot(x,y_estimate,label=f'Exp (MSE): {round(e,3)} ({round(mse,3)})')
        if show:
            plt.show()

    def plot_data(self,scatter = False, average_line = False, degrees = False, exponentials = False,x_axis = '',y_axis = '',title = ''):
        if scatter:
            self.scatter_plot()
        if average_line:
            self.mean_and_std_line(average_line)
        if degrees:
            self.plot_linear_models(degrees)
        if exponentials:
            self.plot_exponential_models(exponentials)

        plt.legend()
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.xticks(np.arange(0,self.get_x()[-1]+1,1))
        plt.grid()
        plt.title(title)
        plt.show()

if __name__ == "__main__":
    # blue = dataset('BlueMotor3Marker.csv')
    # switch = dataset('SwitchMotor3Marker.csv')
    # broken = dataset('BrokenMotor3Marker.csv')
    # blue1 = dataset('BlueMotor1Marker.csv')
    # current = dataset('CurrentWheelMotor.csv')
    # fifty_grams_down = dataset('50gDown.csv')
    # hundred_grams_down = dataset('100gDown.csv')

    # blue.plot_data(1,[1,1],[1],0,'Volts','RPM','RPM v. Volts for DC Motor: Blue3')

    # switch.plot_data(1,[1,1],[1],0,'Volts','RPM','RPM v. Volts for DC Motor: Switch')

    # broken.plot_data(1,[1,1],[1],0,'Volts','RPM','RPM v. Volts for DC Motor: Broken')

    # blue1.plot_data(1,[1,1],[1],0,'Volts','RPM','RPM v. Volts for DC Motor: Blue1')

    # current.plot_data(1,[0,0],[1,2],0,'Volts','A','A v. Volts for DC Motor: Wheel')
    # fifty_grams_down.plot_data(1,[0,0],[1,2],0,'Volts','A','A v. Volts for DC Motor: Wheel 50 g')
    # hundred_grams_down.plot_data(1,[0,0],[1,2],0,'Volts','A','A v. Volts for DC Motor: Wheel 100 g')
    pass
