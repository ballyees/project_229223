import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import numpy as np

# all function
def load_dataset():
    cols_cat = {'Name': 'category', 'Platform': 'category', 'Genre': 'category', 'Publisher': 'category'}
    df = pd.read_csv('vgsales.csv', dtype=cols_cat)
    cols = df.columns
    cols_cat_info = {i:df[i].cat.categories for i in cols_cat.keys()}
    
    # clean data 
    df['Year'] = df['Year'].fillna(1960).astype('int') #Mark NaN with 1960
    df['Publisher'] = df['Publisher'].fillna('Unknown') # fill unknown(?) values with Unknown

    unique = ['Rank', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales', 'Name']
    return {'data': df, 'cols_category': cols_cat.keys(), 'cols_category_info': cols_cat_info, 'unique_col': unique}

def getDataInfo_column(df, column):
    print(f'Select column: {column}')
    values = df[column].value_counts()
    indexs = list(df[column].value_counts().index)
    dl = {}
    for i in indexs:
        dl[i] = values[i]
    return dl

def notColumns(df, col_index):
    not_col = col_index not in range(len(df.columns)) 
    if not_col:
        print(f'{col_index} not index columns in data')
    return not_col

def addData(maxRank):
    try:
        name = input('Enter name:')
        platform = input('Enter platform:')
        year = int(input('Enter year:'))
        genre = input('Enter genre:') 
        publisher = input('Enter publisher:')
        na_sales = float(input('Enter NA sales:'))
        eu_sales = float(input('Enter EU sales:'))
        jp_sales = float(input('Enter JP sales:'))
        other_sales = float(input('Enter  Other sales:'))
        global_sales = na_sales + eu_sales + jp_sales + other_sales
    except Exception as e:
        print('Invalid input !!')
        return (None, e)
    # data model
    data = pd.DataFrame({
        'Rank': [maxRank+10], #mark not update
        'Name': [name],
        'Platform': [platform],
        'Year': [year],
        'Genre': [genre],
        'Publisher': [publisher],
        'NA_Sales': [na_sales],
        'EU_Sales': [eu_sales],
        'JP_Sales': [jp_sales],
        'Other_Sales': [other_sales],
        'Global_Sales': [global_sales]
    })
    return (data, None)

def UpdateRank(update, df, replace_rank=True):
    df = pd.concat([df, update], ignore_index=True)
    df = df.sort_values(['Global_Sales'], ascending=False, ignore_index=True)
    if replace_rank:
        df['Rank'] = df.index + 1
    else:
        df['newRank'] = df.index + 1
    return df

def search_column(df, key):
    col = list(map(lambda x: x.upper(), list(df.columns).copy()))
    return col.index(key.upper())
    
def plot_hist(df, column):
    plt.figure(figsize=(15, 8), clear=True)
    plt.title(f'Frequency of {column}')
    plt.xlabel(column)
    plt.hist(df[column], len(df[column].unique()), edgecolor = (0,0,0))
    plt.grid(True)
    plt.xticks(rotation='vertical')
    plt.show()
        
def isExit(command):
    command = command.upper()
    listExit = ['EXIT', 'E', 'Q']
    return (command in list(map(lambda x: x.upper(), listExit)))

def printInfoDataframe(df, **kwargs):
    print(df.info())
    
def plot_Data(df, **kwargs):
    columns_plot = list(filter(lambda x: x not in kwargs['unique'], df.columns))
    for i, v in enumerate(columns_plot):
        print(f'{i} : {v}')
    col = int(input('Select columns: '))
    if col not in range(len(columns_plot)):
        return
    else:
        col = list(df.columns).index(columns_plot[col])
    if notColumns(df, col):
        return
    plot_hist(df, df.columns[col])
    
    column_info = getDataInfo_column(df, df.columns[col])
    fcol = np.array([len(str(i))+1 for i in column_info.keys()]).max()
    fval = np.array([len(str(i))+1 for i in column_info.values()]).max()
    endline = 3
    counter = 0
    for k, v in column_info.items():
        counter += 1
        print(f'%{fcol}s : %{fval}s'%(k, str(v)), end=','+' '*5)
        if counter > endline:
            print()
            counter = 0
    
def add_Data(df, **kwargs):
    data, error = addData(df['Rank'].max())
    if not error:
        df = UpdateRank(data, df)
    return (df, error)

def save_Data(df, **kwargs):
    ow = input('Will you overwrite the original file? (Y/n): ').upper()
    if ow in ['Y', 'YES']:
        filename = 'vgsales'
    else:
        filename = input('Enter name of file: ')
    df.to_csv(f'{filename}.csv', index=False)
    
def search_Data(df, **kwargs):
    cols = df.columns.to_numpy()
    for i, v in enumerate(cols):
        print(f'{i} : {v}')
    col_index = int(input('Select column for search: '))
    if notColumns(df, col_index):
        return
    result = None
    if cols[col_index] in kwargs['cat'] or cols[col_index] in ['Year']:
        s = input('Enter search: ')
        result = df[df[cols[col_index]].map(lambda x: str(x).upper()).map(lambda x: s.upper() in x)] # boolean index
    else:
        feature = int(input('Enter 0(<=) or 1(>=): '))
        s = input('Enter search: ')
        if feature:
            result = df[df[cols[col_index]] >= float(s)]
        else:
            result = df[df[cols[col_index]] <= float(s)]
    print('search result: ')
    if not len(result):
        return
    limit = 5
    counter = 0
    max_format = np.array([len(str(result.to_numpy()[:,i].max()))+1 for i in range(len(df.columns))])
    for i, v  in enumerate(result.to_numpy()):
        if counter == limit:
            break
        for j, c in enumerate(df.columns):
            print(f'{c}: %{max_format[j]}s'%format(str(v[j])), end=', ')
        print()
        counter += 1
    return

def showOption():
    print(f'''
    Menu Option
    1 : show info of Data,
    2 : plot Data(histogram),
    3 : add Data,
    4 : search Data,
    5 : save Data
    e, exit, q : end program !!!
    ''')