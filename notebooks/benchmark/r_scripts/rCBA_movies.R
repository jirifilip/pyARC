moviesdf <- read.csv("c:/code/python/CBA/notebooks/data/movies_discr.csv", sep = ";", stringsAsFactors = TRUE)

# drop empty id column
drops <- c("")


train <- moviesdf[, !(names(moviesdf) %in% drops)]


txns <- as(train, "transactions") 


appearance = list(rhs=c("class=critical-success", "class=box-office-bomb", "class=main-stream-hit"),default="lhs")

rules = apriori(txns, parameter=list(support=0.01, confidence=0.05), appearance = appearance)



rulesFrame <- as(rules, "data.frame")

prunedRulesFrame <- rCBA::pruning(train, rulesFrame, method="m1cba")





prunedRulesFrame
