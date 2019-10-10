"""
Clique Method Robustness Verification for Tree Ensembles and Gradient Boosted Decision Tree Classifiers
"""

from xgboost import XGBClassifier
import lightgbm
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier

from art.classifiers import XGBoostClassifier, LightGBMClassifier, SklearnClassifier
from art.utils import master_seed, load_dataset
from art.metrics import RobustnessVerificationTreeModelsCliqueMethod

import warnings
warnings.filterwarnings('ignore')

NB_TRAIN = 100
NB_TEST = 100

(x_train, y_train), (x_test, y_test), _, _ = load_dataset('mnist')

n_classes = 10
n_features = 28 * 28
n_train = x_train.shape[0]
n_test = x_test.shape[0]
x_train = x_train.reshape((n_train, n_features))
x_test = x_test.reshape((n_test, n_features))

x_train = x_train[:NB_TRAIN]
y_train = y_train[:NB_TRAIN]
x_test = x_test[:NB_TEST]
y_test = y_test[:NB_TEST]

master_seed(42)

# 1. XGBoost

model = XGBClassifier(n_estimators=4, max_depth=6)
model.fit(x_train, np.argmax(y_train, axis=1))

classifier = XGBoostClassifier(model=model, nb_features=n_features, nb_classes=n_classes)

rt = RobustnessVerificationTreeModelsCliqueMethod(classifier=classifier)
average_bound, verified_error = rt.verify(x=x_test, y=y_test, eps_init=0.3, nb_search_steps=10, max_clique=2,
                                          max_level=2)

print('Average bound:', average_bound)
print('Verified error at eps:', verified_error)
"""
Average bound: 0.035996093750000006
Verified error at eps: 0.96
"""

# 2. LightGBM

train_data = lightgbm.Dataset(x_train, label=np.argmax(y_train, axis=1))
test_data = lightgbm.Dataset(x_test, label=np.argmax(y_test, axis=1))

parameters = {'objective': 'multiclass',
              'num_class': n_classes,
              'metric': 'multi_logloss',
              'is_unbalance': 'true',
              'boosting': 'gbdt',
              'num_leaves': 5,
              'feature_fraction': 0.5,
              'bagging_fraction': 0.5,
              'bagging_freq': 0,
              'learning_rate': 0.05,
              'verbose': 0}

model = lightgbm.train(parameters,
                       train_data,
                       valid_sets=test_data,
                       num_boost_round=2,
                       early_stopping_rounds=10)

classifier = LightGBMClassifier(model=model)

rt = RobustnessVerificationTreeModelsCliqueMethod(classifier=classifier)
average_bound, verified_error = rt.verify(x=x_test, y=y_test, eps_init=0.3, nb_search_steps=10, max_clique=2,
                                          max_level=2)

print('Average bound:', average_bound)
print('Verified error at eps:', verified_error)
"""
[1]	valid_0's multi_logloss: 2.25471
Training until validation scores don't improve for 10 rounds.
[2]	valid_0's multi_logloss: 2.21845
Did not meet early stopping. Best iteration is:
[2]	valid_0's multi_logloss: 2.21845
Average bound: 0.07634765624999999
Verified error at eps: 0.85
"""

# 3. GradientBoosting

model = GradientBoostingClassifier(n_estimators=4, max_depth=6)
model.fit(x_train, np.argmax(y_train, axis=1))

classifier = SklearnClassifier(model=model)

rt = RobustnessVerificationTreeModelsCliqueMethod(classifier=classifier)
average_bound, verified_error = rt.verify(x=x_test, y=y_test, eps_init=0.3, nb_search_steps=10, max_clique=2, 
                                          max_level=2)

print('Average bound:', average_bound)
print('Verified error at eps:', verified_error)
"""
Average bound: 0.009234374999999996
Verified error at eps: 1.0
"""

# 4. RandomForest

model = RandomForestClassifier(n_estimators=4, max_depth=6)
model.fit(x_train, np.argmax(y_train, axis=1))

classifier = SklearnClassifier(model=model)

rt = RobustnessVerificationTreeModelsCliqueMethod(classifier=classifier)
average_bound, verified_error = rt.verify(x=x_test, y=y_test, eps_init=0.3, nb_search_steps=10, max_clique=2, 
                                          max_level=2)

print('Average bound:', average_bound)
print('Verified error at eps:', verified_error)
"""
Average bound: 0.019962890624999997
Verified error at eps: 1.0
"""

# 5. ExtraTrees

model = ExtraTreesClassifier(n_estimators=4, max_depth=6)
model.fit(x_train, np.argmax(y_train, axis=1))

classifier = SklearnClassifier(model=model)

rt = RobustnessVerificationTreeModelsCliqueMethod(classifier=classifier)
average_bound, verified_error = rt.verify(x=x_test, y=y_test, eps_init=0.3, nb_search_steps=10, max_clique=2, 
                                          max_level=2)

print('Average bound:', average_bound)
print('Verified error at eps:', verified_error)
"""
Average bound: 0.041332031250000026
Verified error at eps: 1.0
"""
