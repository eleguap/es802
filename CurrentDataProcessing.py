import numpy as np
import matplotlib.pyplot as plt
import csv

def calculate_mse(y,y_estimated):
    return (np.sum((y-y_estimated)**2)/len(y))**0.5

def constant_speed(show = False):
    """
    Very specific function for this project only
    """
    files = ['0gSpeed.csv','50gDownSpeed.csv','50gUpSpeed.csv','100gDownSpeed.csv','100gUpSpeed.csv','200gDownSpeed.csv','200gUpSpeed.csv']
    files = ['Data/Power/' + file for file in files]
    x = [0]
    y = [0]

    for file in files:
        with open(file, 'r') as f:
            data = f.read()
            x += [int(line.split(',')[0]) for line in data.split('\n') if line]
            y += [round(float(line.split(',')[1]),4) for line in data.split('\n') if line]

    set_x = sorted(set(x))

    x = np.array(x)
    y = np.array(y)

    # Creating average line and std
    mean_data = {x: [] for x in set_x}
    length = len(x)

    for index in range(length):
        mean_data[x[index]].append(y[index])

    x_averaged = np.array(list(mean_data.keys()))
    y_averaged = np.array([np.average(mean_data[key]) for key in mean_data])
    y_std = np.array([np.std(mean_data[key]) for key in mean_data])

    # Fitting degree 1 polynomial to average line
    coeffs = np.polyfit(x,y,1)
    y_estimate = np.polyval(coeffs,x)
    slope = coeffs[0]
    mse = calculate_mse(y,y_estimate)

    if show:
        plt.scatter(x,y,c='gray',label='Scatter')
        plt.plot(x_averaged,y_averaged,label = 'Mean')
        plt.plot(x_averaged,y_averaged+2*y_std,label = '+ 2std')
        plt.plot(x_averaged,y_averaged-2*y_std,label = '- 2std')
        plt.plot(x,y_estimate,label=f'Degree (Slope, MSE): {1} ({round(slope,3)},{round(mse,3)})')
        plt.xticks(np.arange(0,set_x[-1]+1,1))
        plt.xlabel('Volts')
        plt.ylabel('Speed (m/s)')
        plt.title('Speed v. Volts')
        plt.legend()
        plt.grid()
        plt.show()

    return set_x,coeffs

def all_downs(plot = False, show = False):
    files = ['0gCurrent1.csv','50gDownCurrent1.csv','100gDownCurrent1.csv','200gDownCurrent1.csv']
    files = ['Data/Power/' + file for file in files]
    y_s = []

    for file in files:
        with open(file, 'r') as f:
            data = f.read()
            x = [0]+[int(line.split(',')[0]) for line in data.split('\n') if line]
            y = [0]+[round(float(line.split(',')[1]),4) for line in data.split('\n') if line]

        y_s.append(y)

        grams = file[11:file.index('g')+1]
        if plot:
            plt.plot(x,y,label = f'{grams} (Down)')

    if show:
        plt.xlabel('Volts')
        plt.ylabel('Current (A)')
        plt.xticks(np.arange(0,x[-1]+1,1))
        plt.ylim(0, 0.04)
        plt.title('Current Drawn while Lowering Weights')
        plt.grid()
        plt.legend()
        plt.show()

    return y_s


def all_ups(plot = False, show = False):
    files = ['0gCurrent.csv','50gUpCurrent.csv','100gUpCurrent.csv','200gUpCurrent.csv']
    files = ['Data/Power/' + file for file in files]
    x = [0]
    y = [0]
    y_s = []

    for file in files:
        with open(file, 'r') as f:
            data = f.read()
            x = [0]+[int(line.split(',')[0]) for line in data.split('\n') if line]
            y = [0]+[round(float(line.split(',')[1]),4) for line in data.split('\n') if line]

        y_s.append(y)
        grams = file[11:file.index('g')+1]
        if plot:
            plt.plot(x,y,label = f'{grams} (Up)')

    if show:
        plt.xlabel('Volts')
        plt.ylabel('Current (A)')
        plt.xticks(np.arange(0,x[-1]+1,1))
        plt.ylim(0, 0.04)
        plt.title('Current Drawn while Raising Weights')
        plt.grid()
        plt.legend()
        plt.show()

    return y_s

def all_together():
    all_downs(True)
    all_ups(True)

    plt.xlabel('Volts')
    plt.ylabel('Current (A)')
    plt.ylim(0, 0.04)
    plt.xticks(np.arange(0,16,1))
    plt.title('Current Drawn while Raising and Lowering Weights')
    plt.legend()
    plt.grid()
    plt.show()

def power_in_downs(plot = False, show = False):
    files = ['50gDownSpeed.csv','100gDownSpeed.csv','200gDownSpeed.csv']
    files = ['Data/Power/' + file for file in files]

    for i in range(len(files)):
        with open(files[i], 'r') as f:
            data = f.read()
            x = [0]+[int(line.split(',')[0]) for line in data.split('\n') if line]
            y = [0]+[round(float(line.split(',')[1]),4) for line in data.split('\n') if line]

        y = np.array(all_downs()[i+1][:11]) * np.array(x)
        grams = files[i][11:files[i].index('g')+1]

        print(y)

        if plot:
            plt.plot(x,y,label = f'{grams} (Down)')

    if show:
        plt.xlabel('Volts')
        plt.ylabel('Power (W)')
        plt.xticks(np.arange(0,x[-1]+1,1))
        plt.ylim(0, 0.35)
        plt.title('Power Drawn while Lowering Weights')
        plt.grid()
        plt.legend()
        plt.show()

def power_in_ups(plot = False, show = False):
    files = ['50gUpSpeed.csv','100gUpSpeed.csv','200gUpSpeed.csv']
    files = ['Data/Power/' + file for file in files]

    for i in range(len(files)):
        with open(files[i], 'r') as f:
            data = f.read()
            x = [0]+[int(line.split(',')[0]) for line in data.split('\n') if line]
            y = [0]+[round(float(line.split(',')[1]),4) for line in data.split('\n') if line]

        y = np.array(all_ups()[i+1][:11]) * np.array(x)
        grams = files[i][11:files[i].index('g')+1]

        if plot:
            plt.plot(x,y,label = f'{grams} (Up)')

    if show:
        plt.xlabel('Volts')
        plt.ylabel('Power (W)')
        plt.xticks(np.arange(0,x[-1]+1,1))
        plt.ylim(0, 0.35)
        plt.title('Power Drawn while Raising Weights')
        plt.grid()
        plt.legend()
        plt.show()

def power_in_all_together():
    power_in_downs(True)
    power_in_ups(True)
    plt.xlabel('Volts')
    plt.ylabel('Power (W)')
    plt.xticks(np.arange(0,11,1))
    plt.ylim(0, 0.35)
    plt.title('Power Drawn while Raising and Lowering Weights')
    plt.grid()
    plt.legend()
    plt.show()

def speed_fucntion():
    return np.polyval(constant_speed()[1],constant_speed()[0])

def power_out_downs(plot = False,show = False,constant = False):
    files = ['50gDownSpeed.csv','100gDownSpeed.csv','200gDownSpeed.csv']
    files = ['Data/Power/' + file for file in files]

    for i in range(len(files)):
        with open(files[i], 'r') as f:
            data = f.read()
            x = [0]+[int(line.split(',')[0]) for line in data.split('\n') if line]
            if constant:
                y = [0] + speed_fucntion()
            else:
                y = [0]+[round(float(line.split(',')[1]),4) for line in data.split('\n') if line]

        mass = int(files[i][11:files[i].index('g')])/1000
        y = np.array(y) * mass * 9.8

        grams = files[i][11:files[i].index('g')+1]
        if plot:
            plt.plot(x,y,label = f'{grams} (Down)')

    if show:
        plt.xlabel('Volts')
        plt.ylabel('Power (W)')
        plt.xticks(np.arange(0,x[-1]+1,1))
        plt.ylim(0, 0.04)
        plt.title('Power Output while Lowering Weights')
        plt.grid()
        plt.legend()
        plt.show()


def power_out_ups(plot = False,show = False,constant = False):
    files = ['50gUpSpeed.csv','100gUpSpeed.csv','200gUpSpeed.csv']
    files = ['Data/Power/' + file for file in files]

    for i in range(len(files)):
        with open(files[i], 'r') as f:
            data = f.read()
            x = [0]+[int(line.split(',')[0]) for line in data.split('\n') if line]
            if constant:
                y = [0] + speed_fucntion()
                print(y)
            else:
                y = [0]+[round(float(line.split(',')[1]),4) for line in data.split('\n') if line]

        mass = int(files[i][11:files[i].index('g')])/1000
        y = np.array(y) * mass * 9.8

        grams = files[i][11:files[i].index('g')+1]
        if plot:
            plt.plot(x,y,label = f'{grams} (Up)')

    if show:
        plt.xlabel('Volts')
        plt.ylabel('Power (W)')
        plt.xticks(np.arange(0,x[-1]+1,1))
        plt.ylim(0, 0.04)
        plt.title('Power Output while Raising Weights')
        plt.grid()
        plt.legend()
        plt.show()

def power_out_all_together(constant = False):
    power_out_downs(True,0,constant)
    power_out_ups(True,0,constant)
    plt.xlabel('Volts')
    plt.ylabel('Power (W)')
    plt.xticks(np.arange(0,11,1))
    plt.ylim(0, 0.04)
    plt.title('Power Output while Raising and Lowering Weights')
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # for y in np.polyval(constant_speed()[1],constant_speed()[0]):
    #     with open('bullshit.csv', 'a', newline='') as csvfile:
    #             # creating a csv writer object
    #             csvwriter = csv.writer(csvfile)
    #             # writing the data rows
    #             csvwriter.writerow([y.item()])

    # all_downs(True,True)
    # all_ups(True,True)
    # all_together()

    # power_in_downs(True,True)
    # power_in_ups(True,True)
    # power_in_all_together()

    # power_out_downs(True,True)
    # power_out_ups(True,True)
    power_out_all_together()


    pass
