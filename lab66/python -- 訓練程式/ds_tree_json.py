# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 19:09:49 2021

@author: g3863
"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pathlib
from sklearn.preprocessing import LabelEncoder
import json

def tree2json(clf, features, labels, node_index=0):    
    node = {}
    if clf.tree_.children_left[node_index] == -1:  # indicates leaf
        node['samples'] = clf.tree_.n_node_samples[node_index]
        node['impurity'] = clf.tree_.impurity[node_index]
        node['value'] = clf.tree_.value[node_index].tolist()[0]
        node['id'] = node_index
        node['criterion'] = 'gini'
    else:
        feature = features[clf.tree_.feature[node_index]]
        node['samples'] = clf.tree_.n_node_samples[node_index]
        node['id'] = node_index
        node['key'] = feature
        left_index = clf.tree_.children_left[node_index]
        right_index = clf.tree_.children_right[node_index]
        node['children'] = [tree2json(clf, features, labels, left_index),
                            tree2json(clf, features, labels, right_index)]
        node['gini'] = clf.tree_.impurity[node_index]
        node['value'] = clf.tree_.threshold[node_index]
    return node

def dataset2json(dataset, datasety, index, features):
    data_json = []
    for i in range(dataset.shape[0]):
        data = {}
        for j in range(len(features)):
            data[features[j]] = dataset[i][j]
            
        data['index'] = index[i]
        data['target'] = datasety[i]
        data_json.append(data)
    return data_json

def findMaxMin(dataset, featureIndex):
    values = []
    for data in dataset:
        values.append(data[featureIndex])
        
    if values == []:
        return 0,0
    else:
        return max(values), min(values)

def sortData(datasetX, datasety, dataIndex, threshold, featureIndex):
    left_side = {'index':[],'feature':[],'class':[], 'data':[]}
    right_side = {'index':[],'feature':[],'class':[], 'data':[]}

    for i in range(len(dataIndex)):
        index = dataIndex[i]
        data = datasetX[i]
        feature = datasetX[i]
        
        if featureIndex > -1:
            feature = feature[featureIndex]
        
        if feature <= threshold:
            left_side['index'].append(index)
            left_side['feature'].append(feature)
            left_side['data'].append(data)
            left_side['class'].append(datasety[i])
        else:  
            right_side['index'].append(index)
            right_side['feature'].append(feature)
            right_side['data'].append(data)
            right_side['class'].append(datasety[i])
            
    return left_side, right_side
    
def tree_state(datasetX, datasety, clf, features, dataIndex, node_index=0, nodes=None):
    node = {}
    
    if nodes == None:
        nodes=[]
    
    featureIndex = clf.tree_.feature[node_index]
    false_side, true_side = sortData(datasety, datasety, dataIndex, 0, -1)
                  
    if clf.tree_.children_left[node_index] == -1:  # indicates leaf
        node['data_rows'] = {
            'false':false_side['index'],
            'true':true_side['index']
            }
        node['has_children'] = 'false'
        node['node'] = node_index
        
        nodes.append(node)
    
    else:
        maxVal, minVal = findMaxMin(datasetX, featureIndex)
        left_side, right_side = sortData(datasetX, 
                                         datasety, 
                                         dataIndex, 
                                         clf.tree_.threshold[node_index],
                                         featureIndex)
            
        node['attribute'] = features[featureIndex]
        node['data_rows'] = {
            'false':false_side['index'],
            'true':true_side['index']
            }
        node['data_values'] = {
            'false':false_side['feature'],
            'true':true_side['feature']
            }
        node['has_children'] = 'true'        
        node['max_val'] = maxVal
        node['min_val'] = minVal
        node['node'] = node_index
                
        node['split_location'] = {
            'left_side':left_side['index'],
            'right_side':right_side['index']
            }
        node['split_point'] = clf.tree_.threshold[node_index]
        
        nodes.append(node)

        #下一節點
        left_index = clf.tree_.children_left[node_index]
        right_index = clf.tree_.children_right[node_index]

        tree_state(left_side['data'], left_side['class'], clf, features,
                   left_side['index'], left_index, nodes)
        tree_state(right_side['data'], right_side['class'], clf, features,
                   right_side['index'], right_index, nodes)
        
    return nodes

datacsv = pd.read_csv(str(pathlib.Path.cwd())+'\\rawData.csv')
datacsv = datacsv.fillna(0)
labelencoder = LabelEncoder()
datacsv['地區']= labelencoder.fit_transform(datacsv['地區'])

columns = datacsv.columns.tolist()

#資料內容
features = datacsv.columns[1:]

#資料類別
label = datacsv.columns[0]

#資料索引
index = list(range(datacsv.shape[0]))

data = datacsv.to_numpy()
X = data[:,1:]
y = data[:,0]

#73分拆
X_train, X_test, y_train, y_test, train_index, test_index = \
    train_test_split(X,y,index,train_size=0.7)

clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
result = clf.predict(X_train)
#tree.plot_tree(clf, fontsize=8)

tree_data = tree2json(clf, features, label)
training_set = dataset2json(X_train, y_train, train_index, features)

test_set = dataset2json(X_test, y_test, test_index, features)
test_stats = tree_state(X_test, y_test, clf, features, test_index)
tree_stats = tree_state(X_train, y_train, clf, features, train_index)


output = eval(str({
    "tree_data": tree_data,
    "tree_training_set": training_set,
    "tree_test_set": test_set,
    "test_stats": test_stats,
    "tree_stats": tree_stats
}))


with open('dataset.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(output, ensure_ascii=False, indent=4))





