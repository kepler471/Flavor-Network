'''Classify recipes into regional cuisines based on ingredients or flavors, using logistic regresion, SVM, randomforest, MultinomialNB, and plot confusion_matrix
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
# from sklearn import cross_validation, grid_search
# from sklearn.cross_validation import KFold, train_test_split
from sklearn.model_selection import KFold, train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix, classification_report


def logistic_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print('First round:', metrics.accuracy_score(y_test, y_pred))
    # tune parameter C
    crange = [0.01, 0.1, 1, 10, 100]
    for num in crange:
        model = LogisticRegression(C=num)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print('C=', num, ',score=', metrics.accuracy_score(y_test, y_pred))


def svm_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
    model = svm.LinearSVC(C=1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print('First round:', metrics.accuracy_score(y_test, y_pred))
    # tune parameter C
    crange = [0.01, 0.1, 1, 10, 100]
    for num in crange:
        model = svm.LinearSVC(C=num)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print('C=', num, ',score=', metrics.accuracy_score(y_test, y_pred))


def nb_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    model = MultinomialNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(metrics.accuracy_score(y_test, y_pred))


def rf_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
    rf_model = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)
    print(metrics.accuracy_score(y_test, y_pred))


# plot confusion_matrix, 'col' is the y target
def plot_confusion_matrix(cm, col, title, cmap=plt.cm.viridis):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    for i in range(cm.shape[0]):
        plt.annotate("%.2f" % cm[i][i], xy=(i, i),
                     horizontalalignment='center',
                     verticalalignment='center')
    plt.title(title, fontsize=18)
    plt.colorbar(fraction=0.046, pad=0.04)
    tick_marks = np.arange(len(col.unique()))
    plt.xticks(tick_marks, sorted(col.unique()), rotation=90)
    plt.yticks(tick_marks, sorted(col.unique()))
    plt.tight_layout()
    plt.ylabel('True label', fontsize=18)
    plt.xlabel('Predicted label', fontsize=18)
    plt.show()


if __name__ == '__main__':
    # read pickled dataframe
    yum_clean = pd.read_pickle('data/yummly_clean.pkl')

    # create a set of all ingredients in the dataframe
    yum_ingredients = set()
    yum_clean['clean ingredients'].map(lambda x: [yum_ingredients.add(i) for i in x])
    print(len(yum_ingredients))
    # create one column for each ingredient, True or False
    yum = yum_clean.copy()
    for item in yum_ingredients:
        yum[item] = yum['clean ingredients'].apply(lambda x: item in x)
    yum_X = yum.drop(yum_clean.columns, axis=1)
    # test various classification models
    logistic_test(yum_X, yum['cuisine'])
    # C=1 gave the best result, accuracy 0.69
    svm_test(yum_X, yum['cuisine'])
    # linear svm C=0.1 gave the best result, accuracy 0.70
    nb_test(yum_X, yum['cuisine'])
    # accuracy is 0.64
    rf_test(yum_X, yum['cuisine'])
    # accuracy is 0.64

    # plot confusion_matrix with svm
    X = yum_X.values
    y = yum['cuisine']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
    model = svm.LinearSVC(C=0.1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(10, 10))
    plot_confusion_matrix(cm_normalized, yum['cuisine'], title='Confusion Matrix based on ingredients')

    # read pickled dataframe
    yum_ingr = pd.read_pickle('data/yum_ingr.pkl')
    yum_tfidf = pd.read_pickle('data/yum_tfidf.pkl')
    # plot confusion matrix for flavor-based classification
    X = yum_tfidf.values
    y = yum_ingr['cuisine']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(10, 10))
    plot_confusion_matrix(cm_normalized, yum_ingr['cuisine'], title='Confusion Matrix based on flavor')
