  library(arc)
  
  dataset_name = "heart-statlog";
  
  files_count = 10;
  
  accs <- c();
  
  accs <- sapply(0:(files_count - 1), function(i) {
    train_txt <- paste("c:/code/python/machine_learning/assoc_rules/train/", dataset_name, i, ".csv", sep="");
    test_txt <- paste("c:/code/python/machine_learning/assoc_rules/test/", dataset_name, i, ".csv", sep="");
    
    train <- read.csv(train_txt);
    test <- read.csv(test_txt);
    
    classatt <- colnames(train)[ncol(train)]
  
    rm <- cba(train, classatt)
    prediction <- predict(rm, test)
    acc <- CBARuleModelAccuracy(prediction, test[[classatt]])
    
    acc
  })
  
  mn = mean(accs);
  
  print(mn)