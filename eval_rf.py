import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
df = pd.read_csv('data/consultancies_dataset.csv').fillna('')
y = df['label'].astype(int).values
sbert = SentenceTransformer('all-MiniLM-L6-v2')
name_emb = sbert.encode(df['name'].tolist(), convert_to_numpy=True)
desc_emb = sbert.encode(df['description'].tolist(), convert_to_numpy=True)
fee = df['asks_fee'].replace('',0).astype(float).values.reshape(-1, 1)
X = np.concatenate([name_emb, desc_emb, fee], axis=1)
clf = joblib.load('models/fake_consultancy_rf.pkl')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
y_pred = clf.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%')
print(f'Precision: {precision_score(y_test, y_pred, average=\'weighted\')*100:.2f}%')
print(f'Recall: {recall_score(y_test, y_pred, average=\'weighted\')*100:.2f}%')
print(f'F1: {f1_score(y_test, y_pred, average=\'weighted\')*100:.2f}%')
