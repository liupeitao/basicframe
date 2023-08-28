import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# 假设你有一个已标记好的数据集，包含链接和标签
data = pd.read_csv('labeled_link_data.csv')  # 根据实际数据路径修改

# 特征工程 - 使用链接本身作为特征
X = data['link']
y = data['label']

# 将链接转换为计数特征向量
count_vectorizer = CountVectorizer()
X_count = count_vectorizer.fit_transform(X)

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_count, y, test_size=0.2, random_state=42)

# 选择模型并训练
model = MultinomialNB()  # 选择朴素贝叶斯作为示例模型
model.fit(X_train, y_train)

# 预测并评估模型
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", classification_rep)
