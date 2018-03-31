import time
import fim
from ..data_structures import Consequent, Item, Antecedent, ClassAssocationRule

"""
==============================================================================
GENERATE CARS
==============================================================================
"""
def generateCARs(transactionDB, support=1, confidence=50, maxlen=10, **kwargs):
    appear = transactionDB.appeardict
    
    rules = fim.apriori(transactionDB.string_representation, supp=support, conf=confidence, target="r", report="sc", appear=appear, **kwargs, zmax=maxlen)
    

    return createCARS(rules)
 



"""
==============================================================================
TOP RULES
==============================================================================
"""
def top_rules(transactions,
              appearance={},
              target_rule_count=1000,
              init_support=0.,
              init_conf=0.5,
              conf_step=0.05,
              supp_step=0.05,
              minlen=2,
              init_maxlen=3,
              iteration_timeout=2,
              total_timeout=100.,
              max_iterations=30,
              trim=True):
    
    starttime = time.time()
    
    MAX_RULE_LEN = len(transactions[0])
    
    support = init_support
    conf = init_conf
    
    maxlen = init_maxlen
    
    iterations_time_limit_exceeded = 0
    
    flag = True
    lastrulecount = -1
    maxlendecreased_due_timeout = False
    iterations = 0
    
    rules = None
    
    
    while flag:
        iterations += 1
            
        if iterations == max_iterations:
            print("Max iterations reached")
            break
                
                
        
        try:
            print("Running apriori with setting: confidence={}, support={}, minlen={}, maxlen={}, MAX_RULE_LEN={}".format(
                  conf, support, minlen, maxlen, MAX_RULE_LEN))
            
            rules_current = fim.arules(transactions, supp=support, conf=conf, report="sc", appear=appearance, zmax=maxlen, zmin=minlen)
            
            rules = rules_current
            
            rule_count = len(rules)
            
            print("Rule count: {}, Iteration: {}".format(rule_count, iterations))
            
            if (rule_count >= target_rule_count):
                flag = False
                print("Target rule count satisfied:", target_rule_count)
            else:
                exectime = time.time() - starttime
                
                if exectime > total_timeout:
                    print("Execution time exceeded:", total_timeout)
                    flag = False
                    
                elif maxlen < MAX_RULE_LEN and lastrulecount != rule_count and not maxlendecreased_due_timeout:
                     maxlen += 1
                     lastrulecount = rule_count
                     print("Increasing maxlen", maxlen)
                         
                elif maxlen < MAX_RULE_LEN and maxlendecreased_due_timeout and support <= 1 - supp_step:
                    support += supp_step
                    maxlen += 1
                    lastrulecount = rule_count
                    
                    print("Increasing maxlen to", maxlen)
                    print("Increasing minsup to", support)
                    
                    maxlendecreased_due_timeout = False
                
                elif conf > conf_step:
                    conf -= conf_step
                    print("Decreasing confidence to", conf)
                    
                else:
                    print("All options exhausted")
                    flag = False
        
        except:

            print("Iterations timeout")
            print("Maxlen", maxlen)
            
            iterations_time_limit_exceeded += 1
            
       
    return rules



"""
==============================================================================
CREATE CARS
==============================================================================
"""
def createCARs(rules):
    CARs = []
    
    for rule in rules:
        con_tmp, ant_tmp, support, confidence = rule

        con = Consequent(*con_tmp.split("="))

        ant_items = [ Item(*i.split("=")) for i in ant_tmp ]
        ant = Antecedent(ant_items)

        id_len = len(ant)

        CAR = ClassAssocationRule(ant, con, support=support, confidence=confidence, id_rule=id_len)
        CARs.append(CAR)

    CARs.sort(reverse=True)

    return CARs