library("rCBA")
data("iris")

train <- read.csv("C:/code/python/machine_learning/assoc_rules/train/anneal0.csv") 
test <- read.csv("C:/code/python/machine_learning/assoc_rules/test/anneal0.csv")

output <- rCBA::build(train)
model <- output$model
predictions <- rCBA::classification(test, model)
table(predictions)
actual <- test[,ncol(test)]
sum(actual==predictions, na.rm=TRUE) / length(predictions)
