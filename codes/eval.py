import pandas as pd

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