

#@author: mhl


import os
import codecs
import re
import rename_html_files
import pandas as pd
from read_names import female_list, male_list
import numpy as np




directory = os.getcwd() + '/scripts_html'
def rename_and_read_files(directory):
    for filename in os.listdir(directory):
        filename_new = filename.replace(' ', "")
        filename_new = filename_new.replace('-', '_')
        
        os.rename(directory + '/'+ filename,directory + '/'+filename_new)   
        

    
    all_docs = []
    movie_titles =[]
    
    for filename in   os.listdir(directory):
        print(filename)
        
        file = codecs.open(directory + '/' + filename, "r", "utf-8")
        file1 = file.read()
        file3 = file1.split("\n")
        all_docs.append(file3)
        movie_titles.append(os.path.splitext(filename)[0])
    
    return all_docs, movie_titles
        
    




  

def filter_names(all_docs):
    bTags =[]  
    for index in range(len(all_docs)):
    
        for string_index , i in enumerate(all_docs[index]):
    
            if  ('<b>' in i ) and ('</b>' not in i):
    
                        bTags.append([index, string_index ,i])
                    
    new_list =[]

    for index, item in enumerate(bTags):
        #print(index)

        string = item[2].replace('<b>', "").lower() #removes unecessary characters, splits the string in its elemtns and selects the overal between the names and the string
        string = re.sub("[^\w' ]", "", string).split()


        intersect_female = set.intersection(set(female_list), set(string))
        intersetct_male = set.intersection(set(male_list), set(string))
        intersect  = intersect_female.union(intersetct_male)
        intersect = ''.join(map(str,intersect))
        #print(intersect)

    
        if len(intersect)==0:
            
            continue
    
        else: 
          
            new_list.append([item[0], item[1], intersect])
            

    return new_list

          

def filter_males(all_docs):
    
    
    text =[]  
    for index in range(len(all_docs)):
    
        for string_index , i in enumerate(all_docs[index]):

            if  ('</b>'  or 'br/'in i) and ('<b>' not in i):

                        text.append([index, string_index ,i]) 
    
    clean_text =[]
    
    for index, item in enumerate(text):
    
        
    
        string = item[2].replace('</b>', "").lower()
        string = re.sub("[^\w' ]", "", string).split()
    
        intersetct_male = set.intersection(set(male_list), set(string))
      
        if len(intersetct_male)==0:
           
            continue
     
        else: 
         
            clean_text.append([item[0], item[1], list(intersetct_male)])
    return clean_text





def female_female_speak(all_names):

    female_dialogue =[]
    
    previous_person = 1
    
    for index, value in enumerate(all_names): #selects tow females that are different but in the same script. if they have been already added in the conversation list, meaning the speakers exchange turns the two speakers are onlt added once.
    
    
            if index ==0:
                pass
            
            elif (not female_dialogue) and (all_names[index][0]==all_names[index-1][0]) and (all_names[index][2] in female_list) and (all_names[index-1][2] in female_list) and (all_names[index][2] != all_names[index-1][2])\
                and (previous_person != 0):
                    
                    female_dialogue.append([all_names[index][0], all_names[index][1], all_names[index-1][1], all_names[index][2], all_names[index-1][2],1])
                    previous_person == 0
       
    
            elif (all_names[index][0]==all_names[index-1][0]) and (all_names[index][2] in female_list) and (all_names[index-1][2] in female_list) and (all_names[index][2] != all_names[index-1][2])\
                and (previous_person != 0) and (all_names[index][2] and all_names[index-1][2] not in female_dialogue[-1]):
       
                    female_dialogue.append([all_names[index][0], all_names[index][1], all_names[index-1][1], all_names[index][2], all_names[index-1][2],1])
                    previous_person == 0
        
                    
            else:
                    previous_person = value[2]
                    #print(previous_person)
    return female_dialogue


        

            

def female_female_male(females_speak): #selects where the male person wan mentioned by comparing the indexes
    
    female_dialogue_male = []
    
    for female_index, female_value in enumerate(females_speak):   
        #print(female_index)
        for male_index, male_value in enumerate(filtered_males):
            #print(male_index)
    
    
            
            if ( male_value[1] in range(female_value[2],female_value[1])) and (male_value[0] == female_value[0]):
                
                #merged  = female_value + [male_value[1] , male_value[2]]
                #print(male_value[1],female_value[2],female_value[1])
                female_dialogue_male.append(female_value + [male_value[1] , male_value[2]])
    return female_dialogue_male



def analytics(movie_titles, female_dialogue_male): #all above data saved in a df for futher analysis. Many analytics could be trief and plotted. Some shown here only for reference.
    movie_titles = pd.DataFrame(movie_titles).reset_index()
    df = pd.DataFrame(female_dialogue_male, columns = ['movie_id','index1', 'index2', 'female1', 'female2', 'del', 'index3', 'males'])
    df.drop('del', axis=1,inplace=True)
    
    s = df['movie_id'].replace(movie_titles.set_index('index')[0])
    df['movie_titles'] = s
    
    
    most_frequent_males = df['males'].value_counts().index.tolist()
    
    
    print('The most frequent names talked by women in movies are {}'.format(most_frequent_males[:10]))
    
    
    most_frequent_female_comb = df.groupby(['female1', 'female2']).size().sort_values(ascending=False).index.tolist()
    
    print('The most frequent female combinations are {}'.format(most_frequent_female_comb[:10]))
    
    movie_with_most_female_dialogue = df.groupby(['movie_titles']).size().sort_values(ascending=False).index.tolist()
    
    print('The movies with the most female dialogue are {}'.format(movie_with_most_female_dialogue[:10]))
    







    
if __name__ == "__main__":
    all_docs, movie_titles = rename_and_read_files(directory)
    all_names = filter_names(all_docs)
    filtered_males  = filter_males(all_docs)
    
    females_speak = female_female_speak(all_names)
    female_dialogue_male  = female_female_male(females_speak)
    analytics(movie_titles, female_dialogue_male)
    
    
    
    
