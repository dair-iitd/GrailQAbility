from typing import List, Tuple
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import urllib
from pathlib import Path
from tqdm import tqdm
import os,sys

sparql = SPARQLWrapper("http://localhost:3001/sparql")
sparql.setReturnFormat(JSON)


cur_dir=os.getcwd()
data_dir = os.path.join(cur_dir,"data")

file_name="GrailQAbility_v1.0"

def load_json(split):
    file_reader=open(data_dir+os.sep+file_name+"_"+split+".json","r",encoding="utf-8")
    list_of_questions=json.load(file_reader)
    file_reader.close()
    return list_of_questions


def execute_query(qid,query: str) -> List[str]:
    sparql.setQuery(query)
    rtn = []
    try:
        results = sparql.query().convert()
        
        for result in results['results']['bindings']:
            assert len(result) == 1  # only select one variable
            for var in result:
                rtn.append(result[var]['value'].replace('http://rdf.freebase.com/ns/', '').replace("-08:00", ''))

    except urllib.error.URLError:
        print("================================")
        print(qid,query)
        print("================================")
        #results['results']['bindings']=[]
        exit(0)
    
    return rtn

def get_f1_score(gt_answer,predict_answer):
    if len(predict_answer)==0 and len(gt_answer)==0:
        return 1
    
    gt_answer_list=set()
    
    for a in gt_answer:
        gt_answer_list.add(a['answer_argument'])
    
    precision = len(predict_answer.intersection(gt_answer_list)) / len(predict_answer)
    recall = len(predict_answer.intersection(gt_answer_list)) / len(gt_answer_list)
    if recall==0 or precision==0:
        return 0
    f1=2 * recall * precision / (recall + precision)
    return f1

def validate_KG(questions):
    nacount=0
    acount=0
    wrongCount=0
    for index,que in enumerate(questions):
        qType=que['qType']
        sparql=que['sparql_query']
        gt_answer=que['answer']
        qid=que['qid']			
        pred_answer=execute_query(qid,sparql)
        
        
        
        f1=get_f1_score(gt_answer,set(pred_answer))
        if f1==1 and qType=="NA":
            nacount+=1
        elif f1==1 and qType=="A":
            acount+=1
        else:
            wrongCount+=1
        
    return nacount,acount

for split in ["dev"]:
    list_of_all_questions_with_updated_answer=load_json(split+"_a_na_reference")
    nacount,acount=validate_KG(list_of_all_questions_with_updated_answer)
    if len(list_of_all_questions_with_updated_answer)==acount+nacount:
        print("KG validation successfull for "+split)
    else:
        print("KG validation unsuccessfull for "+split)
