library(stringr)

file_regex_extract <- '([A-z0-9_-]+?)[0-9].csv'



datasets_train <- as.data.frame(list.files("c:\\code\\python\\machine_learning\\assoc_rules\\train"))
datasets_test <- as.data.frame(list.files("c:\\code\\python\\machine_learning\\assoc_rules\\test"))

names(datasets_train) <- c('filename')
names(datasets_test) <- c('filename')

datasets_train$group <- apply(datasets_train[c('filename')], 1, function (x) {
  str_match(x, file_regex_extract)[1, 2]
})

datasets_test$group <- apply(datasets_test[c('filename')], 1, function (x) {
  str_match(x, file_regex_extract)[1, 2]
})

datasets_train_split <- split(datasets_train, datasets_train$group)
datasets_test_split <- split(datasets_test, datasets_test$group)

datasets_train_split <- lapply(datasets_train_split, function (x) {
  names(x) <- c("filename", "group")
  x
})

datasets_test_split <- lapply(datasets_test_split, function (x) {
  names(x) <- c("filename", "group")
  x
})


anneals_train <- as.list(datasets_train[1:10,1])
anneals_test <- as.list(datasets_test[1:10,1])


run_cba_partially <- function(trainFiles, testFiles) {
  
  
  trainSet <- lapply(trainFiles, function (filename) {
    file <- paste('c:\\code\\python\\machine_learning\\assoc_rules\\train\\', filename, sep = "")
    read.csv(file = file)
  })
  
  testSet <- lapply(testFiles, function (filename) {
    file <- paste('c:\\code\\python\\machine_learning\\assoc_rules\\test\\', filename, sep = "")
    read.csv(file = file)
  })
  
  
  classatt <- tail(colnames(trainSet[1]), n = 1)
  print(classatt)
  
  accuracies <- lapply(1:length(trainSet), function (i) {
    train <- as.data.frame(trainSet[i])
    test <- as.data.frame(testSet[i])
    
    classatt <- tail(colnames(as.data.frame(trainSet[1])), n = 1)
    
    rm <- cba(train, classatt)
    prediction <- predict(rm, test)
    
    acc <- CBARuleModelAccuracy(prediction, test[[classatt]])
    
  })
  
  
  accs <- unlist(accuracies)
  mn <- mean(accs)
  
  paste("mean: ", mn, sep = ' ')
} 



run_cba_partially(datasets_train_split$`breast-cancer`[,1], datasets_test_split$`breast-cancer`[,1])





