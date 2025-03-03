import os
import inspect

# Define named sections (grouped by subjects)
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
""",

    "decision_tree": """
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
data = pd.read_csv('D:/TYCS-515/DS/DATASETS/DecisionTree_Data.csv')
X = data[['Feature1', 'Feature2']]
y = data['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
clf = DecisionTreeClassifier().fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(f"Decision Tree Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
"""
}

# Mapping multiple names (aliases) to sections
SECTION_ALIASES = {
    "lin_reg": "linear_regression",
    "ds_p1": "linear_regression",
    "log_reg": "logistic_regression",
    "classification": "logistic_regression",
    "dt": "decision_tree",
    "dip_p1": "decision_tree"
}

# Define subject-wise organization
SUBJECT_SECTIONS = {
    "all1": {
        "name": "ds",
        "sections": ["linear_regression", "logistic_regression"]
    },
    "all2": {
        "name": "dip",
        "sections": ["decision_tree"]
    }
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
    """Pastes the specified section(s) into the importing script."""
    importing_script = get_importing_script()
    
    if not importing_script or not os.path.isfile(importing_script):
        print(f"❌ Error: Unable to find the target script.")
        return
    
    with open(importing_script, "a") as target_file:
        if section_name in SUBJECT_SECTIONS:
            # "all1" or "all2" detected, paste subject-wise
            subject_info = SUBJECT_SECTIONS[section_name]
            subject_name = subject_info["name"]
            sections = subject_info["sections"]
            
            target_file.write(f"\n\n# --- {subject_name} ---\n")
            for sec_name in sections:
                if sec_name in CODE_SECTIONS:
                    target_file.write("\n\n# --- Pasted Code: {} ---\n".format(sec_name))
                    target_file.write(CODE_SECTIONS[sec_name])
                    target_file.write("\n# --- End of Pasted Code ---\n")
            print(f"✅ All sections from '{subject_name}' pasted successfully into {importing_script}")

        else:
            # Check if section name is an alias
            actual_section = SECTION_ALIASES.get(section_name, section_name)

            if actual_section not in CODE_SECTIONS:
                print(f"❌ Error: Section '{section_name}' not found.")
                return
            
            # Paste the specific section
            target_file.write("\n\n# --- Pasted Code: {} ---\n".format(actual_section))
            target_file.write(CODE_SECTIONS[actual_section])
            target_file.write("\n# --- End of Pasted Code ---\n")
            print(f"✅ Code for '{actual_section}' pasted successfully into {importing_script}")
