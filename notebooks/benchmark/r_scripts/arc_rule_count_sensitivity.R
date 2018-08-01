#library(devtools)
#install_github('ianjjohnson/arulesCBA', ref="time-trials", force=TRUE)
#install_github('jaroslav-kuchar/rCBA', ref="develop")
#install_github('kliegr/arc', force=TRUE)
library(arc)
library(rCBA)
library(arulesCBA)
dataset_path_train="C:/code/python/machine_learning/assoc_rules/train/lymph0.csv"
dataset_path_test="C:/code/python/machine_learning/assoc_rules/test/lymph0.csv"
#data with discretization applied by external preprocessing
trainFold <- utils::read.csv(dataset_path_train, header = TRUE, check.names = FALSE)
testFold <- utils::read.csv(dataset_path_test, header = TRUE, check.names = FALSE)
data <- rbind(trainFold,testFold)
data[,9] <- discretize(data[,9], "frequency", categories=3)
data[,10] <- discretize(data[,10], "frequency", categories=3)
data[,18] <- discretize(data[,18], "frequency", categories=3)
disc.data <- lapply(data, levels)
trainFold <- data[1:nrow(trainFold),]
testFold <-data[(nrow(trainFold)+1):nrow(data),]
classAtt <- "class"
outputFileName<-"arc-rule-sensitivity.csv"
appearance <- arc::getAppearance(trainFold, classAtt)
txns_discr <- as(trainFold, "transactions")
txns_discr_test <- as(testFold, "transactions")
#this returns a lot of rules (4187880) to choose from
#rule learning is performed on discretized datlibrary(microbenchmark::microbenchmark)a
rules <- apriori(txns_discr, parameter =
                   list(confidence = 0, support= 0.01, minlen=1, maxlen=20), appearance=appearance)
write(paste("dataset,input rules,output_rules_arc,output_rules_rcba,output_rules_acba,time_arc,time_rcba,time_acba,acc_arc,acc_rcba,acc_acba"), file = outputFileName,
      ncolumns = 1,
      append = FALSE, sep = ",")
number_of_iterations = 10
#we gradually increase number of input rules and observe how run time changes
for (i in c(10:19,seq(20,100,by=10),seq(200,1000,by=100),seq(2000,10000,by=1000),seq(20000,100000,by=10000)))
{
  message(paste("input rules:",i))
  # we do ten iterations to have a more robust estimate
  
  # arc
  ptm <- proc.time()
  for (j in 1:number_of_iterations)
  {
    rmCBA <- cba_manual(trainFold,rules[0:i], txns_discr, appearance$rhs,
                        classAtt, cutp= list(), pruning_options=NULL)
  }
  proctime<- proc.time() - ptm
  dur_arc<-proctime[3]/number_of_iterations # proctime[3] returns cumulative sum of user times (https://stat.ethz.ch/R-manual/R-devel/library/base/html/proc.time.html)
  arc_prediction = predict(rmCBA,testFold,discretize=FALSE)
  acc_arc <- arc::CBARuleModelAccuracy(arc_prediction,testFold$class) # sum(testFold$class == arc_prediction)/length(arc_prediction)        
  message(paste("acc arc:", acc_arc))
  # end of arc
  #rCBA start        
  ptm <- proc.time()
  for (j in 1:number_of_iterations)
  {
    rmRCBA <- rCBA::pruning(trainFold, rules[0:i], method="m2cba")
  }
  proctime<- proc.time() - ptm
  dur_rcba<-proctime[3]/number_of_iterations
  rcba_prediction = rCBA::classification(txns_discr_test,rmRCBA)
  acc_rcba <-  arc::CBARuleModelAccuracy(rcba_prediction,testFold$class)  #sum(testFold$class == rcba_prediction)/length(rcba_prediction)
  message(paste("acc arc:", acc_rcba))
  #rCBA end
  
  # start of arulesCBA
  ptm <- proc.time()
  for (j in 1:number_of_iterations)
  {
    message("starting arulesCBA")
    rmArulesCBA <- arulesCBA::CBA.internal(rules[0:i], txns_discr, classAtt, disc.data, method="CBA",sort.rules = TRUE)
    message(paste("number of input rules:",i,", pruned rules in arulesCBA model:", length(rmArulesCBA$rules)))
    message("arulesCBA finished") 
  }
  proctime<- proc.time() - ptm
  acba_prediction = predict(rmArulesCBA, txns_discr_test, method="first")
  acc_acba <-  arc::CBARuleModelAccuracy(acba_prediction,testFold$class)  #sum(testFold$class == acba_prediction)/length(acba_prediction)
  message(paste("acc arc:", acc_acba))
  dur_acba<-proctime[3]/number_of_iterations
  message(paste("acba finished"))
  
  # end of arulesCBA           
  
  write(paste(dataset_path_test, i, length(rmCBA@rules),  nrow(rmRCBA), length(rmArulesCBA$rules)+1, dur_arc, dur_rcba, dur_acba, acc_arc,acc_rcba,acc_acba, sep = ","), file = outputFileName,
        ncolumns = 1,
        append = TRUE, sep = ",")
}