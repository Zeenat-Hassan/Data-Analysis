import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database= "CSV_DB"
)


def find_pattern(Pattern):

 mycursor = mydb.cursor()
 sql = 'Select Processed_Data from QA_1 where Processed_Data like \"%{} %\"'.format(Pattern)
 mycursor.execute(sql)
 myresult = mycursor.fetchall()
 for x in myresult:

  txt= str(x)
  get_index_of_substring(Pattern,txt)
    #str.find() is case sensitive matches with exact case letters
    # y=txt.find(Pattern)
    # print(y)





def Call_Records_for_Removing_strings():
 print('Enter your string pattern :')
 Take_Input = input()
#Calling find_pattern function
 Call_function_find_pattern= find_pattern(Take_Input)




def get_index_of_substring(Pattern,string):
    pattern_length = len(Pattern)
    start_index= string.find(Pattern)
    end_index= start_index + pattern_length
#Calling slice_substring function
    slice_substring(start_index,end_index,string)



def slice_substring(start_index,end_index,string):
    txt=string

#if substring is in the middle
    if(start_index!=0 and end_index!=len(txt) ):
        sttr= txt[:start_index-1]+txt[end_index:]
        print(sttr)

#if substring is in the start

    if(start_index==0):
        sttr= txt[end_index:]
        print(sttr)
#if substring is in the end
    if(end_index==len(txt)):
        sttr= txt[:start_index-1]
        print(sttr)




Call_Records_for_Removing_strings()






