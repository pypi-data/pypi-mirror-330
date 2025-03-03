import os
import inspect

# Define named sections
CODE_SECTIONS = {
    "linear_regression": """
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
data = pd.read_csv('D:/TYCS-515/DS/DATASETS/Salary_Data.csv') 
x, y = data['YearsExperience'], data['Salary'] 
B1 = ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean())**2).sum() 
B0 = y.mean() - B1 * x.mean() 
Predict = lambda new_x: B0 + B1 * new_x 
print(f'Regression line: y = {round(B0, 3)} + {round(B1, 3)}X') 
print(f'Correlation coefficient: {np.corrcoef(x, y)[0, 1]:.4f}') 
print(f'Goodness of fit (R^2): {np.corrcoef(x, y)[0, 1]**2:.4f}') 
print('Predicted salary:', Predict(70)) 
plt.figure(figsize=(8, 5)) 
plt.scatter(x, y, color='blue', label='Data points') 
plt.plot(x, B0 + B1 * x, color='red', label='Regression line') 
plt.title('How Experience Affects Salary') 
plt.xlabel('Years of Experience') 
plt.ylabel('Salary') 
plt.legend() 
plt.show()
    """,

    "logistic_regression": """
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score, confusion_matrix 
data = pd.read_csv('D:/TYCS-515/DS/DATASETS/Admission_Data.csv') 
x = data[['gmat', 'gpa', 'work_experience']] 
y = data['admitted'] 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0) 
model = LogisticRegression().fit(x_train, y_train) 
y_pred = model.predict(x_test) 
print("Confusion Matrix:\\n", confusion_matrix(y_test, y_pred)) 
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    """
}

def get_importing_script():
    """Find the actual script that imports this package."""
    for frame in reversed(inspect.stack()):
        filename = frame.filename
        if filename.startswith("<") or "idlelib" in filename or "run.py" in filename:
            continue
        return os.path.abspath(filename)
    return None

def paste_code(section_name):
    """Pastes the specified section into the importing script."""
    if section_name not in CODE_SECTIONS:
        print(f"❌ Error: Section '{section_name}' not found.")
        return
    
    importing_script = get_importing_script()
    
    if importing_script and os.path.isfile(importing_script):
        with open(importing_script, "a") as target_file:
            target_file.write("\n\n# --- Pasted Code: {} ---\n".format(section_name))
            target_file.write(CODE_SECTIONS[section_name])
            target_file.write("\n# --- End of Pasted Code ---\n")
        print(f"✅ Code for '{section_name}' pasted successfully into {importing_script}")

