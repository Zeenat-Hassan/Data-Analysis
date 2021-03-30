---TO SEARCH FOR POSITION AND SBSTRING THAT IS TO BE REMOVED--
SELECT Original_text,POSITION("--- Device" IN Original_text),length(Original_text),SUBSTRING(Original_text, POSITION("---- Device" IN Original_text), length(Original_text)) 
from QA_1 
where Original_text like "%---% Device%"

---Query to remove unanted string---
Update QA_1
set Processed_Data= REPLACE(Original_text,SUBSTRING(Original_text, POSITION("---- Device" IN Original_text), length(Original_text))," " )
where Original_text like '%---- Device %'
