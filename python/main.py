import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import numpy as np
from Function import *
# %matplotlib qt
# %matplotlib inline

if __name__ == '__main__':
    data = load_dataset()
    df = data['data']
    optionData = [printInfoDataframe, plot_Data, add_Data, search_Data, save_Data]
    option = {str(i): v for i, v in enumerate(optionData, 1)}
    while True:
        showOption()
        command = input('Enter option: ')
        if isExit(command):
            print('Thank')
            break
        if not command in option.keys():
            print('not found option')
            continue
        else:
            print(f'Select option: '+ command)
            if command in ['3']: # command update df
                df, e = option[command](df)
                if not e:
                    if input('Enter any key to save data option: '):
                        save_Data(df)
            else:
                option[command](df, cat=data['cols_category'], unique=data['unique_col'])
    cv2.destroyAllWindows()