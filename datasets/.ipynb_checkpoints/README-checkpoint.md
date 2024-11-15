# Datasets

Four datasets are used in the paper experiments. Two contain sentences of the form *A is-a B* and two other contain sentences of the form *A is to B what C is to D*.

## *A is-a B* datasets
___


### Origial paper reference
___
| Name       | Paper Citation    | Paper link | Dataset original link                                        |
| ---------: | :------- | :------------------------------ |-----------------------------------------: |
| `Cardillo` |       |  [Cardillo (2010)](https://link.springer.com/article/10.3758/s13428-016-0717-1) [Cardillo (2017)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2952404/ )     |  |
| `Jankowiak`|     |   [Jankowiak (2020)]( https://link-springer-com.abc.cardiff.ac.uk/article/10.1007/s10936-020-09695-7) | |


- **Licenses** :
  
    - Cardillo  :  [![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
    - Jankowiak : [![License: CC BY 4.0](https://licensebuttons.net/l/by/4.0/80x15.png)](https://creativecommons.org/licenses/by/4.0/)


### Examples
___

|  Name |  Stem | Sentences |Label|
|-------: |-------: | :------------------------------------- | :-------- |
|Cardillo | comet  | The astronomer's obssession was a comet. | 1 |
|          |  | The politician's career was a comet. | 2 | 
| Jankoviac |   harbour   | This banana is a harbour | 0 |
|          |         | A house is a harbour | 2|
|          |       | This area is a harbour | 1 |


- **Labels** : 

    - **0** : anomaly
    - **1** : literal
    - **2** : metaphor 
    

### Data fields
___
 
  
	
| Field| Description |	Type |
| -------------: | :------------ | :------------ |
| corpus | Name of the orgiginal dataset | str |
| id | Element id | str |
| set\_id | Id of the set containing the given instance in the multiple-choice task datasets | int |
| label | 0, 1, 2| int |
| A | first term | list(str) |
| B | second term | list(str) |
| 5-folds | frozen splits for cross validation | list(str) |	






## *A is to B what C is to D* datasets
___

The SAT analogy questions originally used in Turney(2005) are enriched with metaphoric/non-metaphoric analogy labels. 

The Green dataset is available in the supplementary material of the XX journal.

| Name       | Paper Citation    | Paper link | Dataset original link                                        |
| ---------: | :------- | :------------------------------ |-----------------------------------------: |
| `Green`    | Green, A. E., Kraemer, D. J. M., Fugelsang, J., Gray, J. R., & Dunbar, K. (2010). Connecting Long Distance: Semantic Distance in Analogical Reasoning Modulates Frontopolar Cortex Activity. Cerebral Cortex, 10, 70-76.    | [Green (2010)](https://academic.oup.com/cercor/article/20/1/70/413473) |[Paper supplementary material](https://academic.oup.com/cercor/article/20/1/70/413473#supplementary-data)|
| `SAT`  | Peter D. Turney. 2006. Similarity of semantic relations.
*Computational Linguistics*, 32(3):379–416.  |  [Turney (2005)](https://direct.mit.edu/coli/article/32/3/379/1915/Similarity-of-Semantic-Relations)   |On demand to the author|

- **Licenses**:
  

    - Green : [All rights reserved](https://s100.copyright.com/AppDispatchServlet?publisherName=OUP&publication=1460-2199&title=Connecting%20Long%20Distance%3A%20Semantic%20Distance%20in%20Analogical%20Reasoning%20Modulates%20Frontopolar%20Cortex%20Activity&publicationDate=2009-04-21&volumeNum=20&issueNum=1&author=Green%2C%20Adam%20E.%3B%20Kraemer%2C%20David%20J.%20M.&startPage=70&endPage=76&contentId=10.1093%2Fcercor%2Fbhp081&oa=&copyright=%C2%A9%20The%20Author%202009.%20Published%20by%20Oxford%20University%20Press.%20All%20rights%20reserved.%20For%20permissions%2C%20please%20e-mail%3A%20journals.permissions%40oxfordjournals.org&orderBeanReset=True)
    - SAT* : [![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

### Examples
___

|  Name |  Stem | Sentences |Label|
|-------: |-------: | :------------------------------------- | :-------- |
|Cardillo | comet  | The astronomer's obssession was a comet. | 1 |
|          |  | The politician's career was a comet. | 2 | 
| Jankoviac |   harbour   | This banana is like a harbour | 0 |
|          |         | A house is a harbour | 2|
|          |       | This area is a harbour | 1 |

- Labels ids :
    - **0** : anomaly
    - **1** : literal : an analogy but not a metaphor
    - **2** : metaphor

 
### Data fields
___
 
  
	
| Field| Description |	Type |
| -------------: | :------------ | :------------ |
| corpus | Name of the orgiginal dataset | str |
| id | Element id | str |
| set\_id | Id of the set containing the given instance in the multiple-choice task datasets | int |
| label | 0, 1, 2| int |
| AB | pair of terms | list(str) |
| CD | pair of terms | list(str) |
| 5-folds | frozen splits for cross validation | list(str) |	



