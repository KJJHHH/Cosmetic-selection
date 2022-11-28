from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
# Training

le = preprocessing.LabelEncoder()
le.fit(['乾性肌膚', '普通性肌膚', '混合性肌膚', '油性肌膚', '敏感性肌膚', '先天過敏性肌膚'])

skintype = input('請輸入：乾性肌膚, 普通性肌膚, 混合性肌膚, 油性肌膚, 敏感性肌膚, 先天過敏性肌膚')
whatage = float(input('age'))
a = 0
for index, product in enumerate(prediction):
    
    skinagenum = pd.DataFrame()
    skin = []
    age = []
    score = []
    for i in range(len(prediction['skintype'][index])):
        skin_person = prediction['skintype'][index][i]
        age_person = prediction['age'][index][i]
        score_person = prediction['score'][index][i]
        skin.append(le.transform([skin_person]))
        age.append(age_person)
        score.append(score_person)


    skinagenum['skin'] = skin
    skinagenum['age'] = age
    skinagenum['score'] = score

    X = skinagenum.iloc[:, :2]
    y = skinagenum.iloc[:, 2]
    tree_clf = DecisionTreeClassifier(random_state=42)
    tree_clf.fit(X, y)
    X_new = [[le.transform([skintype]), whatage]]
    a1 = float(tree_clf.predict(X_new)[0])
    if a == 0:
        output = product        
    if a1>a:
        a = a1
        output = prediction['productname'][index]

print(output)
