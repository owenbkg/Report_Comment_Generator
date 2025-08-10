import pandas as pd
import numpy as np
import os
import math
class excel_reader():
    def __init__(self):
        pass
    def create_class_dict(self, filepath):
        try:
            #retrieve the class name, which is the name of the excel file 
            class_name = os.path.basename(filepath)
            #create a dataframe object containing only the relevant rows/columns
            dataframe = pd.read_excel(filepath, usecols=[0,1,2,3,4], skiprows = [1])
            class_dict = {}
            for row in range(len(dataframe)):
                student_name = dataframe.iloc[row,0]
                #since some of the grades contain decimal points, round it down
                #as this is the normal practice. 
                crit_values = dataframe.iloc[row, 1:5].apply(math.floor).tolist()
                crit_a, crit_b, crit_c, crit_d = crit_values

                class_dict[student_name] = [crit_a, crit_b, crit_c, crit_d]
            return class_name, class_dict
        except Exception as e:  
            print(e)
            return False
        
