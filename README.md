# cs3235
CS3235 Final Project


## ML Algorithms

### Evaluation Metrics
The following Evaluation metrics I think could be helpful. These metrics assume some sort of username. So the algorithm would be trying to determine if it is or isn't that person. This means a False positive is more of a threat than a False negative. This is because a false positive would mean that someone who isn't the actual user has 'logged in' as the user. This would be a breach in security. Thus, evaluation metrics should try to make sure the algorithm is accurate but also minimizes the number of false positives. 

Definitions of some terms:

* True positive: In this case, true positive means if the user is correctly identified as themself. 
* False positive: In this case, false positive means if another user is identified as the user who's username it is.
* True negative: In this case, true negative means if another user is correctly identified as not the user who's username it is.
* False negative: In this case, false negative means if the user who's username it is identified as not the user who's username it is.


**Accuracy**

* Accuracy is an important one for this context because for a security system we want it to be able to match the person's eye movements to the correct person. If it matches to a different person, this would be a breach in the security system.
* Want it to be 1

**Precision**

* Precision is the proportion of actual positive instances to false positive and true positive instances. The ideal precision value is 1 because this means there are no false positives. A false positive in this case would mean that a person was identified incorrectly which would be a breach of security. In this calse, we want to reduce the amount of misclassifications of a person.
* precision = TP/(FP+TP)
* TP = True positive
* FP = False positive 


