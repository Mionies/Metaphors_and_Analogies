# Datasets

Four datasets are used in the paper experiments.

### Cardillo (2010&2017)


### Jankowiak (2020)

### SAT* Analogy Questions

The SAT analogy questions originally used in Turney(2005) are enriched with metaphoric/non-metaphoric analogy labels. 

### Green ()

The Green dataset is available in the supplementary material of the XX journal.


| Name       | Paper Citation    | Paper link | Dataset original link                                        |
| ---------: | :------- | :------------------------------ |-----------------------------------------: |
| `Cardillo` |       |  [Cardillo (2010)](https://link.springer.com/article/10.3758/s13428-016-0717-1) [Cardillo (2017)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2952404/ )     |  |
| `Jankowiak`|     |   [Jankowiak (2020)]( https://link-springer-com.abc.cardiff.ac.uk/article/10.1007/s10936-020-09695-7) | |
| `Green`    | Green, A. E., Kraemer, D. J. M., Fugelsang, J., Gray, J. R., & Dunbar, K. (2010). Connecting Long Distance: Semantic Distance in Analogical Reasoning Modulates Frontopolar Cortex Activity. Cerebral Cortex, 10, 70-76.    | [Green (20)]() ||
| `SAT`  |   |  [Turney (2005)](https://arxiv.org/pdf/cs/0508053.pdf)   | |



## Labels :

- Pairs

    - **0** : anomaly
    - **1** : literal
    - **2** : metaphor 
    
    
- Quadruples :
    - **0** : anomaly
    - **1** : literal : an analogy but not a metaphor
    - **2** : metaphor

### Examples :

|  Name |  Stem | Sentences |Label|
|-------: |-------: | :------------------------------------- | :-------- |
|Cardillo | comet  | The astronomer's obssession was a comet. | 1 |
|          |  | The politician's career was a comet. | 2 | 
| Jankoviac |   harbour   | This banana is like a harbour | 0 |
|          |         | A house is a harbour | 2|
|          |       | This area is a harbour | 1 |


### Data fields :
	
| Field| Description |	Type |
| -------------: | :------------ | :------------ |
| corpus | Name of the orgiginal dataset | str |
| id | Element id | str |
| set\_id | Id of the set containing the given instance in the multiple-choice task datasets | int |
| label | 0, 1, 2| int |
| AB | pair of terms | list(str) |
| CD | pair of terms | list(str) |
| 5-folds | frozen splits for cross validation | list(str) |	
	