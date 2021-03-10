
import pandas as pd
import copy as cp
from typing import List, Tuple
import statistics as sts
import numpy as np

f = open("Paraxel/iris-flowers.txt","w")
data_iris = pd.read_csv("Paraxel/irisdata.txt")

Setosa = data_iris.query("NameIris == 'Iris-setosa'") 
Versicolor = data_iris.query("NameIris == 'Iris-versicolor'") 
Virginica = data_iris.query("NameIris == 'Iris-virginica'") 

def stat_data(func, name_columns:str)->Tuple[float]:
    """
    DOCSTRING:This function counts the func for each type iris 
    INPUT: func - function, name_columns - this is axis for counting
    OUTPUT: list that contains the row data from the table 
    """
    tpl = []

    tpl.append(round(func(Setosa[:][name_columns]),1))
    tpl.append(round(func(Versicolor[:][name_columns]),1))
    tpl.append(round(func(Virginica[:][name_columns]),1))
    tpl.append(round(func(data_iris[:][name_columns]),1))
    return tpl

def stat_data_per(ax:str,N:Tuple[int],l_bound:float,r_bound:float,flag = -1)->Tuple: #0-left bound; 1-right bound;
    """
    DOCSTRING:This function,stat_data , only counts percentages 
    INPUT: ax - axis for counting, N- massive that contains number iris, l_bound, r_bound- left and right bound, flag =0 left bound step in, flag = 1 -right bound step in
    OUTPUT: list that contains the row data from the table 
    """
    tpl = []
    if flag == 0:
        St = len(Setosa.query('{} > {} and {} < {}'.format(ax, l_bound, ax, r_bound)))
        Vsr = len(Versicolor.query('{} > {} and {} < {}'.format(ax, l_bound, ax, r_bound)))
        Vgc = len(Virginica.query('{} > {} and {} < {}'.format(ax, l_bound, ax, r_bound)))
        All = len(data_iris.query('{} > {} and {} < {}'.format(ax, l_bound, ax, r_bound)))

    elif flag == 1:
        St = len(Setosa.query('{} > {} and {} <= {}'.format(ax,l_bound, ax, r_bound)))
        Vsr = len(Versicolor.query('{} > {} and {} <= {}'.format(ax,l_bound, ax, r_bound)))
        Vgc = len(Virginica.query('{} > {} and {} <= {}'.format(ax,l_bound, r_bound,ax)))
        All = len(data_iris.query('{} > {} and {} <= {}'.format(ax,l_bound, r_bound,ax)))

    
    tpl.append(str(St)+"("+str(round(100*St/N[0],1))+")")
    tpl.append(str(Vsr)+"("+str(round(100*Vsr/N[1],1))+")")
    tpl.append(str(Vgc)+"("+str(round(100*Vgc/N[2],1))+")")
    tpl.append(str(All)+"("+str(round(100*All/sum(N),1))+")")
    return tpl

if __name__ == '__main__':

    N = dict()

    f.writelines(["            Iris Flowery Summary\n", "\n","            All Flowers\n", " ","------------------------------------------------------------------------\n"])

    counter = data_iris.groupby(["NameIris"])["NameIris"].count()

    f.write("                   ")

    for i in counter.index:
        f.write("{}   ".format(i))
        N[i] = int(counter[i]) 

    f.write("Total")
    f.write("\n")
    f.write("                   ")

    for i in counter:
        f.write("   N = {}      ".format(i))

    f.write("    N = {}".format(sum(counter)))
    f.write("\n")
    f.write("-------------------------------------------------------------------------")

    # This is the first table 
    ALL_N = list((N.values()))
    ALL_N.append(sum(counter))

    ALL_MEAN = stat_data(sts.mean,"Length1")
    ALL_MIN = stat_data(min,"Length1")
    ALL_MEDIAN =stat_data(sts.median,"Length1")
    ALL_MAX = stat_data(max,"Length1")
    ALL_STD_DEV = stat_data(np.std,"Length1")

    SEPAL_LENGTH_CM = pd.DataFrame([ALL_N,
                                    ALL_MEAN,
                                    ALL_MIN,
                                    ALL_MEDIAN,
                                    ALL_MAX,
                                    ALL_STD_DEV],
                                    index = ["N","MEAN","MIN","MEDIAN","MAX","STANDARD DEVIATION"])
    SEPAL_LENGTH_CM.index.name = "SEPAL_LENGTH(cm)"

    col = {} # Remove names columns
    for i in SEPAL_LENGTH_CM.columns:
        col[i] = ""
    SEPAL_LENGTH_CM.rename(columns = col,inplace = True)  

    f.write(str(SEPAL_LENGTH_CM) + "\n")

    # The second table 
    Comp5 = stat_data_per("Length1",list(N.values()),0,5,0)
    Comp56 = stat_data_per("Length1",list(N.values()),5,6,1)
    Comp67 = stat_data_per("Length1",list(N.values()),6,7,1)
    Comp7 = stat_data_per("Length1",list(N.values()),7,50,1)

    SEPAL_LENGTH_PER = pd.DataFrame([Comp5,
                                     Comp56,
                                     Comp67,
                                     Comp7],
                                     index = ["< 5","<=5 AND <6",">=6 AND <7", ">= 7"])
    
    SEPAL_LENGTH_PER.index.name = "SEPAL_LENGTH(%)"

    col = {} # Remove names columns
    for i in SEPAL_LENGTH_PER.columns:
        col[i] = ""
    SEPAL_LENGTH_PER.rename(columns = col,inplace = True)  

    f.write(str(SEPAL_LENGTH_PER) + "\n")

    # The third table
    ALL_MEAN = stat_data(sts.mean,"Width1")
    ALL_MIN = stat_data(min,"Width1")
    ALL_MEDIAN =stat_data(sts.median,"Width1")
    ALL_MAX = stat_data(max,"Width1")
    ALL_STD_DEV = stat_data(np.std,"Width1")

    SEPAL_WIDTH_CM = pd.DataFrame([ALL_N,
                                   ALL_MEAN,
                                   ALL_MIN,
                                   ALL_MEDIAN,
                                   ALL_MAX,
                                   ALL_STD_DEV],
                                   index = ["N","MEAN","MIN","MEDIAN","MAX","STANDARD DEVIATION"])
    SEPAL_WIDTH_CM.index.name = "SEPAL_WIDTH(cm)"

    col = {} # Remove names columns
    for i in SEPAL_WIDTH_CM.columns:
        col[i] = ""
    SEPAL_WIDTH_CM.rename(columns = col,inplace = True)  

    f.write(str(SEPAL_WIDTH_CM) + "\n")

    #The fours table
    Comp5 = stat_data_per("Width1",list(N.values()),0,5,0)
    Comp56 = stat_data_per("Width1",list(N.values()),5,6,1)
    Comp67 = stat_data_per("Width1",list(N.values()),6,7,1)
    Comp7 = stat_data_per("Width1",list(N.values()),7,50,1)

    SEPAL_WIDTH_PER = pd.DataFrame([Comp5,
                                    Comp56,
                                    Comp67,
                                    Comp7],
                                    index = ["< 5","<=5 AND <6",">=6 AND <7", ">= 7"])
    
    SEPAL_WIDTH_PER.index.name = "SEPAL_WIDTH(%)"

    col = {} # Remove names columns
    for i in SEPAL_WIDTH_PER.columns:
        col[i] = ""
    SEPAL_WIDTH_PER.rename(columns = col,inplace = True)  

    f.write(str(SEPAL_WIDTH_PER) + "\n")

    print("The program worked successfully ")
    f.close()
    
    