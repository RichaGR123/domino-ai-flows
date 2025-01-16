import os
import pickle
import pandas as pd
import shutil
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Read inputs
named_input_1 = "processed_data"
processed_data_path = "/workflow/inputs/{}".format(named_input_1)

named_input_2 = "num_estimators"
num_estimator_value = Path(f"/workflow/inputs/{named_input_2}").read_text()


# Load data
df = pd.read_csv(processed_data_path) 

# Separate features and labels
X = df.drop(columns=['Species'])
y = df['Species']

# Encode labels as integers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)
print('\nTraining set size:', X_train.shape)
print('Testing set size:', X_test.shape)

# Train a model (e.g., Random Forest Classifier)
model = RandomForestClassifier(random_state=42, n_estimators=int(num_estimator_value))
model.fit(X_train, y_train)

# Evaluate the model on the testing set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print('\nModel Accuracy on Test Set:', accuracy)
print('\nClassification Report:')
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Write the mode as output
output_location = f"/workflow/outputs/model"
with open(output_location, 'wb') as file:
    pickle.dump(model, file)
