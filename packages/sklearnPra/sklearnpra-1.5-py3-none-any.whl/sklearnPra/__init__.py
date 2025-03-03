import os
import inspect

# Define named sections (grouped by subjects)
CODE_SECTIONS = {
    "linear_convolution": """

disp('Practical 1a')

x = [4,5,6;7,8,9];
h = [1;1;1];

disp(conv2(x,h))
""",

    "circular_convolution": """
 disp('Practical 1b')
x = [1, 2; 3, 4];
h = [5, 6; 7, 8];

disp('x='), disp(x)
disp('h='), disp(h)

n = max(length(x), length(h));
y = cconv(reshape(x', 1, []), reshape(h', 1, []), n);
disp('Circular convoluted vector Y='), disp(y)
""",

    "log_transform": r"""
p2a
img1 = imread('C:\Users\Neeraj\OneDrive\Desktop\call-icon.png');
img = rgb2gray(img1);

subplot(1,2,1);
imshow(img);
title('Original Image');

L = 255;
c = L / log10(1 + L);
d = c * log10(1 + double(img));
a = uint8(d);

subplot(1,2,2);
imshow(a);
title('Log Transform');

""",

    "image_negation": r"""
    p2b
img1 = imread('D:\TYCS_509\DIS\sunder.jpg');
img = rgb2gray(img1);  

subplot(1,2,1);  
imshow(img);  
title('Original Image');  

s = size(img);  

for x = 1:s(1)  
    for y = 1:s(2)  
        img_neg(x, y) = 255 - img(x, y);  
    end  
end  

img_n = uint8(img_neg);  

subplot(1,2,2);  
imshow(img_n);  
title('Image Negation');  


""",

    "power_low": r"""

p2c
img1 =imread(‘C:\Users\Neeraj\OneDrive\Pictures\Me\neeraj2.jpg');
img = rgb2gray(img1);  

subplot(1,2,1);  
imshow(img);  
title('Original Image');  

s = size(img);  
C = 1;  
gamma = 3;  
img = double(img);  

for x = 1:s(1)  
    for y = 1:s(2)  
        j(x, y) = C * (img(x, y) ^ gamma);  
    end  
end  

subplot(1,2,2);  
imshow(j, []);  
title('Power Law Transformation');  



""",

    "brightness_adjustment": r"""

p3a
img1 = imread('D:\TYCS_509\DIS\sunder.jpg');
img = rgb2gray(img1);  

subplot(1,3,1);  
imshow(img);  
title('Original Image');  

B = double(img) - 140;  
subplot(1,3,2);  
imshow(uint8(B));  
title('Brightness Decreased');  

B = double(img) + 140;  
subplot(1,3,3);  
imshow(uint8(B));  
title('Brightness Increased');  



""",

    "contrast_stretching": r"""
p3b
img1 = imread('D:\TYCS_509\DIS\sunder.jpg');
img = rgb2gray(img1);  

subplot(1,3,1);  
imshow(img);  
title('Original Image');  

B = double(img) * 0.5;  
subplot(1,3,2);  
imshow(uint8(B));  
title('Contrast Decreased');  

B = double(img) * 2;  
subplot(1,3,3);  
imshow(uint8(B));  
title('Contrast Increased');  



""",

    "thresholding": r"""

    p3c
p = imread('D:\TYCS_509\DIS\sunder.jpg');
pl = rgb2gray(p);  

subplot(1,2,1);  
imshow(pl);  
title('Original Image');  

T = input('Enter the value for Threshold: ');  

[row, col] = size(pl);  

for x = 1:row  
    for y = 1:col  
        if pl(x, y) < T  
            pl(x, y) = 0;  
        else  
            pl(x, y) = 255;  
        end  
    end  
end  

subplot(1,2,2);  
imshow(pl);  
title('Threshold Image');  

""",

    "splitting_rgb": r"""

    p4a
img = imread('C:\My Folder\Wallpaper\demon-slayer-3840x2160-16945.jpg');

subplot(1,4,1);
imshow(img);
title('Original Image');

s = size(img);

redp = img(:,:,1);
greenp = img(:,:,2);
bluep = img(:,:,3);  % Fixed missing '=' in assignment

subplot(1,4,2);
imshow(greenp);
title('Green Plane');

subplot(1,4,3);
imshow(redp);
title('Red Plane');

subplot(1,4,4);
imshow(bluep);
title('Blue Plane');

""",

    "pseudo_coloring": r"""
p4b
img = imread('D:\TYCS_509\DIS\sunder.jpg');

subplot(1,2,1);
imshow(img);
title('Original Image');

s = size(img);

% Extract color planes
redp = img(:,:,1);
greenp = img(:,:,2);
bluep = img(:,:,3);

OP(:,:,1) = greenp;  
OP(:,:,2) = bluep;   
OP(:,:,3) = redp;   

subplot(1,2,2);
imshow(OP);
title('Pseudo Coloring');


""",

    "brightness_2": r"""
p5a
img1 =imread('D:\TYCS_509\DIS\sunder.jpg');
img = rgb2gray(img1);

subplot(1,3,1);
imshow(img1);

title('Original Image');
B = double(img1) - 140;
subplot(1,3,2);

imshow(uint8(B));
title('Brightness Decreased');
B = double(img1) + 140;

subplot(1,3,3);
imshow(uint8(B));
title('Brightness Increased');


""",

    "contrast_2": r"""
p5b
img1 = imread("D:\TYCS_509\sunder.jpg");
subplot(1,2,1);

imshow(img1);
title('Original Image');
B = double(img1) * 3;

subplot(1,2,2);
imshow(uint8(B));
title('Contrast Adjusted');

""",

    "thresholding_2": r"""
p5c
pl = imread('D:\TYCS_509\sunder.jpg');

subplot(1,2,1);
imshow(pl);

title('Original Image');
T = input('Enter the value for Threshold: ');
[row, col] = size(pl);

for x = 1:row
    for y = 1:col
        if pl(x, y) < T
            p1(x, y) = 0;
        else
            p1(x, y) = 255;
        end
    end
end
subplot(1,2,2);
imshow(p1);
title('Threshold Image');


""",

    "histogram": r"""
p6
a = imread('C:\My Folder\vijay.jpg');
al = double (a);
a2 = rgb2gray (uint8(a1));

subplot (1,2,1);
imshow (uint8(a2));
title('Original Image');

[row, col] = size (a2);
h= zeros(1, 256);

for m = 1:row
    for n = 1:col
        t = a2(m, n);
        h(t+1)=h(t+1) + 1;
    end
end

subplot (1,2,2);
bar(h);
title('Histogram of Original Image');


""",

    "equalization_histogram": r"""
p7
a =imread('D:\TYCS_509\sunder.jpg');
a1 = double(a);
a2 = rgb2gray(uint8(a1));
[row, col] = size(a2);
c = row * col;
h = zeros(1, 256);
z = zeros(1, 256);

for m = 1:row
    for n = 1:col
        t = a2(m, n);
        h(t + 1) = h(t + 1) + 1;
    end
end

pdf = h / c;
cdf = zeros(1, 256);
cdf(1) = pdf(1);

for x = 2:256
    cdf(x) = pdf(x) + cdf(x - 1);
end

new = round(cdf * 255);
b = zeros(row, col);

for p = 1:row
    for q = 1:col
        temp = a2(p, q) + 1;
        b(p, q) = new(temp);
        t = b(p, q);
        z(t + 1) = z(t + 1) + 1;
    end
end

subplot(2,2,1);
imshow(uint8(a2));
title('Original Image');

subplot(2,2,2);
bar(h);
title('Histogram of Original Image');

subplot(2,2,3);
imshow(uint8(b));
title('Histogram Equalized Image');

subplot(2,2,4);
bar(z);
title('Equalized Histogram');


""",

    "erosion": """
p8

w = [0 0 0 0 0 0 0 0 0 0 0 0 0 0 ;
0 1 1 1 1 0 0 0 0 1 1 1 1 0;
0 1 1 1 1 0 0 0 0 1 1 1 1 0;
0 1 1 1 1 1 1 1 1 1 1 1 1 0;
0 1 1 1 1 1 1 1 1 1 1 1 1 0;
0 1 1 1 1 0 0 0 0 1 1 1 1 0;
0 1 1 1 1 0 0 0 0 1 1 1 1 0;
0 0 0 0 0 0 0 0 0 0 0 0 0 0];
disp(w);
 se1 = strel('square',3);
 disp(se1);
 im1 = imerode(w,se1);
 i2 = imdilate(w,se1);
 subplot(1,3,1);
 imshow(w);
 title('original');
subplot(1,3,2);
 imshow(im1);
 title('erorde img');
 subplot(1,3,3);
 imshow(i2);
title('dilated img');



""",

    "smoothing": r"""
    p9
a =imread('D:\TYCS_509\sunder.jpg');
i = rgb2gray(a);

b = imnoise(i, 'gaussian');

h1 = (1/9) * ones(3, 3); % 3x3 averaging filter
h2 = (1/25) * ones(5, 5); % 5x5 averaging filter

output1 = conv2(double(b), h1, 'same');
output2 = conv2(double(b), h2, 'same');

subplot(2, 2, 1);
imshow(i);
title('Original Image');

subplot(2, 2, 2);
imshow(b);
title('Image with Noise');

subplot(2, 2, 3);
imshow(uint8(output1));
title('Smoothed Image with 3x3 Filter');

subplot(2, 2, 4);
imshow(uint8(output2));
title('Smoothed Image with 5x5 Filter');


""",

    "sharpening": r"""

p10
a =imread('D:\TYCS_509\sunder.jpg');
 i = rgb2gray(a);
 h = fspecial('unsharp');
 b = imfilter(i,h);
 subplot(1,2,1);
 imshow(i);
 title('Original Img');
subplot(1,2,2);
imshow(b);
title('high pass filtered img')


""",

    "linear_regression": r"""
    p1
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
data = pd.read_csv('D:/TYCS-515/DS/DATASETS/Salary_Data.csv') 
x, y = data['YearsExperience'], data['Salary'] 
# Calculate coefficients 
B1 = ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean())**2).sum() 
B0 = y.mean() - B1 * x.mean() 
# Predict and display results 
Predict = lambda new_x: B0 + B1 * new_x 
print(f'Regression line: y = {round(B0, 3)} + {round(B1, 3)}X') 
print(f'Correlation coefficient: {np.corrcoef(x, y)[0, 1]:.4f}') 
print(f'Goodness of fit (R^2): {np.corrcoef(x, y)[0, 1]**2:.4f}') 
print('Predicted salary:', Predict(70)) 
# Plot 
plt.figure(figsize=(8, 5)) 
plt.scatter(x, y, color='blue', label='Data points') 
plt.plot(x, B0 + B1 * x, color='red', label='Regression line') 
plt.title('How Experience Affects Salary') 
plt.xlabel('Years of Experience') 
plt.ylabel('Salary') 
plt.legend() 
plt.show() 
""",

    "logistics_regression": r"""
p2
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score, confusion_matrix 
data = pd.read_csv('D:/TYCS-515/DS/DATASETS/Admission_Data.csv') 
x = data[['gmat', 'gpa', 'work_experience']] 
y = data['admitted'] 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0) 
model = LogisticRegression().fit(x_train, y_train) 
y_pred = model.predict(x_test) 
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred)) 
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%") 


""",

    "time_serise": r"""
    p3
import seaborn as sn 
data = pd.read_csv('D:/TYCS-515/DS/DATASETS/AirPassengers.csv', parse_dates=['Month'], 
index_col='Month') 
plt.figure(figsize=(10, 5)) 
sn.lineplot(data=data, x=data.index, y='#Passengers') 
plt.title('Monthly Air Passengers') 
plt.xlabel('Month') 
plt.ylabel('Number of Passengers') 
plt.show() 
""",

    "native_bayes": """

p4
from sklearn.preprocessing import LabelEncoder 
weather = ['sunny', 'sunny', 'overcast', 'rainy', 'rainy'] 
temp = ['hot', 'mild', 'cool', 'cool', 'hot'] 
play = ['no', 'yes', 'yes', 'no', 'yes'] 
le = LabelEncoder() 
weather_encoded = le.fit_transform(weather) 
temp_encoded = le.fit_transform(temp) 
label = le.fit_transform(play) 
print('Weather:', weather_encoded) 
print('Temp:', temp_encoded) 
print('Play:', label) 

""",

    "k_means": r"""
p5
from sklearn.cluster import KMeans data = pd.read_csv('D:/TYCS-515/DS/DATASETS/Countryclusters.csv') 
kmeans = KMeans(3).fit(data[['Longitude', 'Latitude']]) 
data['Clusters'] = kmeans.labels_ 
plt.scatter(data['Longitude'], data['Latitude'], c=data['Clusters'], cmap='rainbow') 
plt.title('Clustering by Location') 
plt.xlabel('Longitude') 
plt.ylabel('Latitude') 
plt.show() 



""",

    "principle_component": r"""
p6
from sklearn.decomposition import PCA
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]]) 
pca = PCA(n_components=2).fit(X) 
print("Explained Variance Ratio:", pca.explained_variance_ratio_) 
print("Singular Values:", pca.singular_values_) 
# Practical 7: Decision Tree 
from sklearn.tree import DecisionTreeClassifier, plot_tree 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score 
iris = pd.read_csv('D:/TYCS-515/DS/DATASETS/Iris.csv') 
x = iris.iloc[:, 1:5] 
y = iris['Species'] 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0) 
model = DecisionTreeClassifier(criterion='entropy', random_state=0).fit(x_train, y_train) 
print(f"Accuracy: {accuracy_score(y_test, model.predict(x_test)) * 100:.2f}%") 
plt.figure(figsize=(12, 8)) 
plot_tree(model, feature_names=x.columns, class_names=model.classes_, filled=True) 
plt.show() 

""",

    "decision_tree": r"""
    p7
from sklearn.preprocessing import StandardScaler 
diabetes = pd.read_csv('D:/TYCS-515/DS/DATASETS/diabetes.csv') 
x = diabetes.iloc[:, :-1] 
y = diabetes.iloc[:, -1] 
x_train, x_test, y_train, y_test = train_test_split(StandardScaler().fit_transform(x), y, test_size=0.2, 
random_state=0) 
model = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=0).fit(x_train, y_train) 
print(f"Test Accuracy: {accuracy_score(y_test, model.predict(x_test)) * 100:.2f}%") 
plt.figure(figsize=(20, 10)) 
plot_tree(model, feature_names=diabetes.columns[:-1], class_names=['No Diabetes', 'Diabetes'], 
f
 illed=True) 
plt.show() 
""",

    "contrast_stretching": r"""
    p8 
from apyori import apriori 
data = pd.read_csv('D:/TYCS-515/DS/DATASETS/store_data.csv', header=None) 
records = data.applymap(str).values.tolist() 
rules = list(apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)) 
print(f"Generated {len(rules)} rules.") 
for rule in rules[:5]: 
print(rule)

"""

}

# Mapping multiple names (aliases) to sections
SECTION_ALIASES = {
    "dip_1a": "linear_convolution",
    "convolution": "linear_convolution",
    "linear": "linear_convolution",
    "dip_1b": "circular_convolution",
    "circular": "circular_convolution",
    "dip_2a": "log_transform",
    "log": "log_transform",
    "dip_2b": "image_negation",
    "negation": "image_negation",
    "dip_2c": "power_low",
    "power": "power_low",
    "dip_3a": "brightness_adjustment",
    "clor_1": "brightness_adjustment",
    "brightness1": "brightness_adjustment",
    "dip_3b": "contrast_stretching",
    "clor_1": "contrast_stretching",
    "contrast1": "contrast_stretching",
    "dip_3c": "thresholding",
    "clor_1": "thresholding",
    "threshold1": "thresholding",
    "dip_4a": "splitting_rgb",
    "splitting": "splitting_rgb",
    "rgb": "splitting_rgb",
    "dip_4b": "pseudo_coloring",
    "pseudo": "pseudo_coloring",
    "dip_5a": "brightness_2",
    "dip_5b": "contrast_2",
    "dip_5c": "thresholding_2",
    "dip_6": "histogram",
    "plot": "histogram",
    "dip_7": "equalization_histogram",
    "dip_8": "erosion",
    "dip_9": "smoothing",
    "dip_10": "sharpening",




    "ds_1": "linear_regression",
    "regression": "linear_regression",
    "ds_2": "logistic_regression",
    "logistic": "logistic_regression",
    "ds_3": "time_serise",
    "line_plot": "time_serise",
    "ds_4": "native_bayes",
    "label_encoder": "native_bayes",
    "ds_5": "k_means",
    "clustring": "k_means",
    "k-means": "k_means",
    "ds_6": "principle_component",
    "pca": "principle_component",
    "PCA": "principle_component",
    "ds_7": "decision_tree",
    "decision": "decision_tree",
    "tree": "decision_tree",
    "iris": "decision_tree",
    "ds_8": "contrast_stretching",
    "apriori": "contrast_stretching"

}
# Define subject-wise organization
SUBJECT_SECTIONS = {
    "dip_all": {
        "sections": ["linear_convolution","circular_convolution","log_transform","image_negation","power_low",
                     "brightness_adjustment","contrast_stretching","thresholding","splitting_rgb","pseudo_coloring",
                      "brightness_2", "thresholding_2", "histogram", "equalization_histogram", "erosion","smoothing", "sharpening","contrast_2"]
    },
    "ds_all": {
        "sections": ["linear_regression","logistic_regression","time_serise","native_bayes","k_means","principle_component",
                     "decision_tree","contrast_stretching"]
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
            sections = subject_info["sections"]
            
            for sec_name in sections:
                if sec_name in CODE_SECTIONS:
                    target_file.write("\n\n#  {} ---\n".format(sec_name))
                    target_file.write(CODE_SECTIONS[sec_name])
        else:
            # Check if section name is an alias
            actual_section = SECTION_ALIASES.get(section_name, section_name)

            if actual_section not in CODE_SECTIONS:
                print(f"❌ Error: Section '{section_name}' not found.")
                return
            
            # Paste the specific section
            target_file.write(CODE_SECTIONS[actual_section])