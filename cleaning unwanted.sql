---TO SEARCH FOR POSITION AND SBSTRING THAT IS TO BE REMOVED--
SELECT Original_text,POSITION("--- Device" IN Original_text),length(Original_text),SUBSTRING(Original_text, POSITION("---- Device" IN Original_text), length(Original_text)) 
from QA_1 
where Original_text like "%---% Device%"
