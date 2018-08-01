library(stringr)
library(rCBA)

file_regex_extract <- '(anneal|australian|autos|breast-w|diabetes|glass|heart-h|hypothyroid|ionosphere|lymph|tic-tac-toe|vehicle)[0-9].csv'



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



run_cba <- function(i) {
  dataset_name <- as.character(as.data.frame(datasets_train_split[i])[1,2])
  
  
  
  
  files <- as.list(as.data.frame(datasets_train_split[i])[,1])
  files <- lapply(files, as.character)
  
  trainSet <- lapply(files, function (filename) {
    file <- paste('c:\\code\\python\\machine_learning\\assoc_rules\\train\\', filename, sep = "")
    read.csv(file = file)
  })
  
  testSet <- lapply(files, function (filename) {
    file <- paste('c:\\code\\python\\machine_learning\\assoc_rules\\test\\', filename, sep = "")
    read.csv(file = file)
  })
  
  
  
  
  classatt <- tail(colnames(trainSet[1]), n = 1)

  
  accuracies <- lapply(1:length(trainSet), function (i) {
    
    train <- as.data.frame(trainSet[i])
    test <- as.data.frame(testSet[i])
    
    classatt <- tail(colnames(as.data.frame(trainSet[1])), n = 1)
    
    appearance <- arc::getAppearance(train, classatt)
    txns <- as(train, "transactions")
    txns_test <- as(test, "transactions")
    
    
    rules <- apriori(txns, parameter =
                       list(confidence = 0.5, support= 0.01, minlen=1, maxlen=20), appearance=appearance)
    
    
    rmRCBA <- rCBA::pruning(train, rules, method="m2cba")
    
    rcba_prediction = rCBA::classification(txns_test, rmRCBA)
    acc_rcba <-  arc::CBARuleModelAccuracy(rcba_prediction, train[classatt])
    
    acc_rcba
  })
  
  
  accs <- unlist(accuracies)
  mn <- mean(accs)
  
  paste(dataset_name, mn, sep = ' ')
} 


accuracies_list <- lapply(1:length(datasets_train_split), run_cba)

print(accuracies_list)

splitted <- lapply(accuracies_list, function (x) unlist(strsplit(x, " ")))

rounded <- lapply(splitted, function (x) {
  dname <- x[1]
  acc <- round(as.double(x[2]), 2)
  (c(dname, acc))
})

df <- data.frame(matrix((rounded), nrow=length(datasets_test_split), byrow=T))

colnames(df) <- c("default")

df$dataset <- apply(df[c('default')], 1, function (x) {
  unlist(x)[1]
})

df$accuracy <- apply(df[c('default')], 1, function (x) {
  unlist(x)[2]
})


df <- df[-1]

write.csv(df, "rCBA_accs.csv")
df


