# pyARC
[![Build Status](https://semaphoreci.com/api/v1/jirifilip/pyarc/branches/working/badge.svg)](https://semaphoreci.com/jirifilip/pyarc)
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

pyARC is an implementation of CBA (Classification Based on Assocation) algorithm introduced in


 ```Liu, B. Hsu, W. and Ma, Y (1998). Integrating Classification and Association Rule Mining. Proceedings KDD-98, New York, 27-31 August. AAAI. pp 80-86.```


The [pyFIM](http://www.borgelt.net/pyfim.html) package is used for the rule generation step. 


## Instalation
```
pip install pyarc
```

## Testing
```
python -m unittest discover -s pyarc/test  -p '*test_*.py'
```


## Examples

Simplest example

```python
from pyarc import CBA, TransactionDB
import pandas as pd

data_train = pd.read_csv("iris.csv")
data_test = pd.read_csv("iris.csv")

txns_train = TransactionDB.from_DataFrame(data_train)
txns_test = TransactionDB.from_DataFrame(data_test)


cba = CBA(support=0.20, confidence=0.5, algorithm="m1")
cba.fit(txns_train)

accuracy = cba.rule_model_accuracy(txns_test) 
```

Using top_rules function to mine the best rules possible

```python
from pyarc import TransactionDB
from pyarc.algorithms import (
    top_rules,
    createCARs,
    M1Algorithm
)
import pandas as pd


data_train = pd.read_csv("iris.csv")
data_test = pd.read_csv("iris.csv")

txns_train = TransactionDB.from_DataFrame(data_train)
txns_test = TransactionDB.from_DataFrame(data_test)

# get the best association rules
rules = top_rules(txns_train.string_representation)

# convert them to class association rules
cars = createCARs(rules)

classifier = M1Algorithm(cars, txns_train).build()

accuracy = classifier.test_transactions(txns_test)

```


