from sklearn.tree import DecisionTreeClassifier

skintype = input('skintype')
X = skinagenum.iloc[:, :2]
y = skinagenum.iloc[:, 2]
tree_clf = DecisionTreeClassifier(random_state=42)
tree_clf.fit(X, y)
X_new = [[le.transform([skintype]), 15]]
a = tree_clf.predict(X_new)
a
