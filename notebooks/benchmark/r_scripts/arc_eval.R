library(arc)



train <- read.csv("c:/code/python/machine_learning/assoc_rules/train/iris0.csv")
test <- read.csv("c:/code/python/machine_learning/assoc_rules/test/iris0.csv")
classatt <- "class"


rm <- cba(train, classatt)
prediction <- predict(rm, test)

acc <- CBARuleModelAccuracy(prediction, test[[classatt]])
print(acc)


inspect(rm@rules)