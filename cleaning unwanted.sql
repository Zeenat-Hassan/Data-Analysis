---TO SEARCH FOR POSITION AND SBSTRING THAT IS TO BE REMOVED--
SELECT Original_text,POSITION("--- Device" IN Original_text),length(Original_text),SUBSTRING(Original_text, POSITION("---- Device" IN Original_text), length(Original_text)) 
from QA_1 
where Original_text like "%---% Device%"

---Query to remove unanted string---
Update QA_1
set Processed_Data= REPLACE(Processed_Data,SUBSTRING(Original_text, POSITION("---- Device" IN Original_text), length(Original_text))," " )
where Processed_Data like '%---- Device %'

-----------
Update QA_1
set Processed_Data= REPLACE(Processed_Data,"Hello Admin ,"," " )
where Processed_Data like '%Hello Admin ,%'
                                                    
SELECT Processed_Data FROM `QA_1` WHERE Processed_Data like '%--------- Device:%'
                                                    
