--This query adds in 70% of records as "training" 
Update QA1 
set Data_Type= "Training"
order by rand()
limit 1650 offset 0

--This query finds the records ("with the required substring that can be removed/trimed")
Select * 
from QA1 
where Processed_Data like '%kind regards%'
