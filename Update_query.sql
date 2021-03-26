#This query adds in 70% of records as "training" 
Update QA1 
set Data_Type= "Training"
order by rand()
limit 1650 offset 0
