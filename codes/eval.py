import pandas as pd
import numpy as np

def data_competition_evaluation(phase="Phase 2", name=""):

 

   # Submission should be loaded from a .csv file.   

   submission = pd.read_csv(name)

   assert all(col in submission.columns for col in ["Client", "Warehouse", "Product"])

   submission = submission.set_index(["Client", "Warehouse", "Product"])

   submission.columns = pd.to_datetime(submission.columns)

   assert (~submission.isnull().any().any())

 

   # Load Objective

   objective = pd.read_csv(f"{phase} - Sales.csv").set_index(["Client", "Warehouse", "Product"])

   objective.columns = pd.to_datetime(objective.columns)

   assert (submission.index == objective.index).all()

   assert (submission.columns == objective.columns).all()

   

   abs_err = np.nansum(abs(submission - objective))

   err = np.nansum((submission - objective))

   score = abs_err + abs(err)
   
   score /= objective.sum().sum()

   print(f"{name}:,", score) #It's a percentage



def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2    
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)    
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df

# Custom error metric 
def custom_error(true, pred):
        
    abs_err = np.nansum(np.abs(pred - true))
    err = np.nansum((pred - true))
    score = abs_err + abs(err)
    score /= true.sum().sum()
    return score