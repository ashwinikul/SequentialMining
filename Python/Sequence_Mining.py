# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 18:13:55 2017
Data Mining Project
Description:
Sequence Pattern Mining
    
@author: 
 
Ashwini Kulkarni


"""
import re
import pandas as  pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

from collections import defaultdict 
import time
start_time = time.time()




# Data Post Processing step II
def conver_page(str1):
    str1=str1.replace(" a ","Front-page")
    str1=str1.replace(" b ","News")
    str1=str1.replace(" c ","Tech")
    str1=str1.replace(" d ","Local")
    str1=str1.replace(" e ","Opinion")
    str1=str1.replace(" f ","on-air")
    str1=str1.replace(" g ","Misc")
    str1=str1.replace(" h ","Weather")
    str1=str1.replace(" i ","msn-news")
    str1=str1.replace(" j ","Health")
    str1=str1.replace(" k ","Living")
    str1=str1.replace(" l ","Business")
    str1=str1.replace(" m ","msn-sports")
    str1=str1.replace(" n ","Sports")
    str1=str1.replace(" o ","Summary")
    str1=str1.replace(" p ","Bbs")
    str1=str1.replace(" q ","Travel")
    return str1

    
def freq_seq_enum(sequences, min_support):
    freq_seqs = set()
    _freq_seq(sequences, tuple(), 0, min_support, freq_seqs)
    return freq_seqs


def _freq_seq(sdb, prefix, prefix_support, min_support, freq_seqs):
    #print("inside _freq_seq")
    #print("Prefix: ")
    #print(prefix)
    if prefix:
        freq_seqs.add((prefix, prefix_support))
    locally_frequents = _local_freq_items(sdb, prefix, min_support)
    #print("locally_frequents:") 
    #print(locally_frequents)
    if not locally_frequents:
        return
    for (item, support) in locally_frequents:
        new_prefix = prefix + (item,)
        new_sdb = _project(sdb, new_prefix)
        _freq_seq(new_sdb, new_prefix, support, min_support, freq_seqs)
    #print("End _freq_seq")

def _local_freq_items(sdb, prefix, min_support):
    items = defaultdict(int)
    freq_items = []
    for entry in sdb:
        visited = set()
        for element in entry:
            if element not in visited:
                items[element] += 1
                visited.add(element)
    # Sorted is optional. Just useful for debugging for now.
    for item in items:
        support = items[item]
        if support >= min_support:
            freq_items.append((item, support))
    return freq_items


def _project(sdb, prefix):
    new_sdb = []
    if not prefix:
        return sdb
    current_prefix_item = prefix[-1]
    for entry in sdb:
        j = 0
        projection = None
        for item in entry:
            if item == current_prefix_item:
                projection = entry[j + 1:]
                break
            j += 1
        if projection:
            new_sdb.append(projection)
    return new_sdb


# Data preprocessing

lines = []
F = open("Output/Proccessed.txt","w")
F2 = open("Output/Proccessed2.txt","w")
index_i =1 
#add FILE Location
#with open("Input/input.seq") as file:
with open("Input/msnbc990928.seq") as file:
    for line in file: 
        obj = line
        obj=obj.replace("10","j")
        obj=obj.replace("11","k")
        obj=obj.replace("12","l")
        obj=obj.replace("13","m")
        obj=obj.replace("14","n")
        obj=obj.replace("15","o")
        obj=obj.replace("16","p")
        obj=obj.replace("17","q")
        obj = obj.translate(str.maketrans({"1":"a","2":"b","3":"c", "4":"d","5":"e","6":"f","7":"g","8":"h","9":"i"}))
        obj= re.sub("[^a-z]+ ", "", obj)
        F.write(obj)
        #str(index_i) +" "+
        record = ""
        for ele in obj:
            page_ele =conver_page(" "+ele+" ")
            record =record+page_ele
        record=record.replace("   "," ")
        F2.write(record.strip()+"\n")
        obj= re.sub("[^a-z]+", "", obj)
        #print(obj)
        #line = line.strip() #or some other preprocessing
        lines.append(obj) #storing everything in memory!
        #rec = index_i +" "+obj 
        index_i=index_i+1
        

F.close()     
F2.close()   


#print (lines)
a= len(lines) * 0.1
str_data = str(lines)
print("min_suport:- "+str(a))      
freq_seqs = freq_seq_enum(lines, a)
result = str((sorted(freq_seqs)))
#print(result)
list_all_element = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q')
element_frequent_count =[]
for ele in list_all_element:
    #print(ele)
    page_ele =conver_page(" "+ele+" ")
    element_frequent_count.append(tuple((page_ele,str_data.count(ele))))
    

#print(list_all_element)
#print(element_frequent_count)
element_frequent_count.sort(key=lambda x: -x[1])
DF_Element_frequent_count =pd.DataFrame(element_frequent_count, columns=["Element","Frequency"])
#print(result)
#print(DF_Element_frequent_count)




# Data Post Processing step I
result=result.replace("((",";((")
result_list = result.split(";")
Large_Sequence =[]
set_freq_count =[]
j=1
for i in result_list: 
   if (i.find("[") == -1) :
       i=i.replace("'"," ")
       i=i.replace("]","")
       i=conver_page(i)  # Data Post Processing step II
       
       #Data Post Processing Step III
       cnt = re.findall(r'\b\d+\b', i)
       convert_to_int=str(cnt)
       convert_to_int=convert_to_int.replace("'"," ").replace("]","").replace("[","")
       pure_int = int(convert_to_int)
       page_itemset =re.sub('[^a-zA-Z  -]+', '', i)
       item_set_k_value = page_itemset.count(" ")
       page_itemset =page_itemset.replace(" ",",")
       page_itemset =page_itemset.replace(",,","")
       
       #most frequent (Item Set, Frequency)
       set_freq_count.append(tuple((page_itemset,pure_int)))
       
       #largest Itemset (Item Set, Item Set Size)
       Large_Sequence.append(tuple((page_itemset,item_set_k_value-1)))

# sorting in Descending Order (Largest to lowest) 
set_freq_count.sort(key=lambda x: -x[1])
Large_Sequence.sort(key=lambda x: -x[1])


#Graph Ploting

#graph 1
df=pd.DataFrame(set_freq_count, columns=["Item Set","Frequency"])

#Post_File1= ("Post_1.txt","w")

top_10_df = df[:10]
top_10_df.to_csv('Output/Frequenct_Sequence.txt', header=True, index=False, sep='\t', mode='a')
objects = top_10_df['Item Set']
y_pos = top_10_df.index.values
performance = top_10_df['Frequency']
#print(performance)

#graph 2

df_1 =pd.DataFrame(Large_Sequence, columns=["Item Set","Size"])
# Inner join between df_1, df => (Item Set, Item Set Size, Frequency)
df_join= pd.merge(df_1, df, on="Item Set", how='inner')
#df_join_sorted = df_join.sort(["Size", "Frequency"], ascending=[0, 0])

df_join_sorted_asc = df_join.sort(["Size", "Frequency"], ascending=[0, 0])
df_join_sorted_asc_top_10 =df_join_sorted_asc[:10]


df_join_sorted_asc_top_10=df_join_sorted_asc_top_10.reset_index(drop=True)
print(df_join_sorted_asc_top_10)
df_join_sorted_asc_top_10.to_csv('Output/Largest_Sequence.txt', header=True, index=False, sep='\t', mode='a')
top_10_df_join = df_join_sorted_asc_top_10[:10]
objects_2 = top_10_df_join['Item Set']
y_pos_2 = top_10_df_join.index.values
performance_2 = top_10_df_join['Frequency']


top_10_popular_element = DF_Element_frequent_count[:10]
top_10_popular_element.to_csv('Output/Most_Pupular.txt', header=True, index=False, sep='\t', mode='a')
objects_3 = top_10_popular_element['Element']
y_pos_3 = top_10_popular_element.index.values
performance_3 = top_10_popular_element['Frequency']

print("Execution Time --- %s Minutes ---" % ((time.time() - start_time)/60))
#Graph plotting
fig1 = plt.figure()
fig2 = plt.figure()
fig3 = plt.figure()

#graph1
g1 = fig1.add_subplot(111)
g1.bar(y_pos+1, performance, align='center')
fig1.suptitle('Most Frequent Sequence Pattern Graph I')
g1.set_xticks(y_pos+1)
g1.set_xticklabels(objects,rotation='vertical')


#graph2
g2 = fig2.add_subplot(111)
g2.bar(y_pos_2+1, performance_2, align='center')
fig2.suptitle('Largest Sequence Pattern Graph II')
g2.set_xticks(y_pos_2+1)
g2.set_xticklabels(objects_2,rotation='vertical')

#graph3

g3 = fig3.add_subplot(111)
g3.bar(y_pos_3+1, performance_3, align='center')
fig3.suptitle('Most Popular pages')
g3.set_xticks(y_pos_3+1)
g3.set_xticklabels(objects_3,rotation='vertical')


fig1.savefig('Graph/Graph1.png') 
fig2.savefig('Graph/Graph2.png') 
fig3.savefig('Graph/Graph3.png') 
plt.show() 
#code end
