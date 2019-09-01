# pyARC
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

pyARC is an implementation of CBA (Classification Based on Assocation) algorithm introduced in


 ```Liu, B. Hsu, W. and Ma, Y (1998). Integrating Classification and Association Rule Mining. Proceedings KDD-98, New York, 27-31 August. AAAI. pp 80-86.```

In addition, pyARC contains the implementation of QCBA (Quantitative CBA) algorithm introduced in 

 ```KLIEGR, Tomas. Quantitative CBA: Small and Comprehensible Association Rule Classification Models. arXiv preprint arXiv:1711.10166, 2017.```

The use of QCBA algorithm is demonstrated in [this jupyter notebook](https://github.com/jirifilip/pyARC/tree/master/notebooks/extensions/QCBA_demonstration.ipynb).


The [fim](http://www.borgelt.net/pyfim.html) package is used for the rule generation step. 

 If you find this package useful in your research, please consider citing ([EasyChair link](https://easychair.org/publications/preprint/5d6G)):

```
 @techreport{filip2018classification,
  title={Classification based on Associations (CBA)-a performance analysis},
  author={Filip, Ji{\v{r}}{\'\i} and Kliegr, Tom{\'a}{\v{s}}},
  year={2018},
  institution={EasyChair}
}
```


## Instalation
```
pip install pyarc
```

For using pyARC, the [fim](http://www.borgelt.net/pyfim.html) package needs to be installed (refer to http://www.borgelt.net/pyfim.html for installation guide).


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


