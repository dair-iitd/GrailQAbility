from typing import List, Tuple
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import urllib
from pathlib import Path
from tqdm import tqdm
import os
import sys
sparql = SPARQLWrapper("http://localhost:3001/sparql")
sparql.setReturnFormat(JSON)
file_name="GrailQAbility_v1.0"

def execute_query(query: str) -> List[str]:
    sparql.setQuery(query)
    try:
        results = sparql.query().convert()
        #print(results)
    except urllib.error.URLError as e:
        results="error"
    return results

def get_queries_fact_drop(s,p,o):
    prefix="http://rdf.freebase.com/ns/"
    if s.startswith("http://rdf.freebase.com/ns/"):
        s="<"+s+">"
    else:
        s=s
    if o.startswith("http://rdf.freebase.com/ns/"):
        o="<"+o+">"
    else:
        o=o
  
    p="<"+prefix+p+">"

    query="DELETE FROM  GRAPH <http://freebase.com> { ?s ?p ?o } from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?s ="+ s +" && ?p="+ p +" && ?o="+o +" ) }"
    return query

def get_literal_count(entity: str, relation: str):
    neighbors = set()

    query2 = ("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX : <http://rdf.freebase.com/ns/> 
        SELECT COUNT(?x1) AS ?value WHERE {
        SELECT DISTINCT ?x1  WHERE {
        """
              ':' + entity + ':' + relation + ' ?x1 . '
                                              """
                     }
                     }
                     """)
    # print(query2)

    sparql.setQuery(query2)
    try:
        results = sparql.query().convert()
    except urllib.error.URLError:
        print(query2)
        exit(0)
    for result in results['results']['bindings']:
        neighbors.add(result['value']['value'].replace('http://rdf.freebase.com/ns/', ''))

    return list(neighbors)[0]


def get_queries_fact_drop_literal(s,p,o):
    if s.startswith("http://rdf.freebase.com/ns/"):
        new_s=s.replace('http://rdf.freebase.com/ns/', '')
    else:
        new_s=s
    count = int(get_literal_count(new_s,p))

    prefix="http://rdf.freebase.com/ns/"
    if s.startswith("http://rdf.freebase.com/ns/"):
        s="<"+s+">"
    else:
        s=s
    if o.startswith("http://rdf.freebase.com/ns/"):
        o="<"+o+">"
    else:
        o=o
  
    p="<"+prefix+p+">"

    if count <=1:
        print(count)
    
        query="DELETE FROM  GRAPH <http://freebase.com> { ?s ?p ?o } from <http://freebase.com> WHERE { ?s ?p ?o. filter ( ?s ="+ s +" && ?p="+ p +" ) }"
    else:
        print(count)
        print(s,p,o)
        sys.exit()
    return query


def drop_literals_from_KG(fact_content):
    fact_error=[]	
    for index,fact in enumerate(fact_content):
        fact_content=fact.strip().split("\t")
        s=fact_content[0]
        p=fact_content[1]
        o=fact_content[2]
        query=get_queries_fact_drop_literal(s,p,o)
        result=execute_query(query)
        if result=="error":
            fact_error.append(fact)
            print("error in literal drop:",fact)
        elif "-- nothing to do" in result['results']['bindings'][0]['callret-0']['value']:
            fact_error.append(fact)
            print("literal is not present in the KG:",fact)
        else:
            continue
    return fact_error

def drop_facts_from_KG(fact_content):
    fact_error=[]	
    for index,fact in enumerate(fact_content):
        print(index)
        fact_content=fact.strip().split("\t")
        s=fact_content[0]
        p=fact_content[1]
        o=fact_content[2]
        query=get_queries_fact_drop(s,p,o)
        result=execute_query(query)
        if result=="error":
            fact_error.append(fact)
            print("error in fact drop:",fact)
        elif "-- nothing to do" in result['results']['bindings'][0]['callret-0']['value']:
            fact_error.append(fact)
            print("fact is not present in the KG:",fact)
        else:
            continue
    return fact_error


def get_queries_eType(e,itemType):
    if itemType=="eType":
        prefix="http://rdf.freebase.com/ns/"
        e="<"+prefix+e+">"
        query_1="DELETE FROM  GRAPH <http://freebase.com> {?s ?p ?o} from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?s ="+e+") }"
        query_2="DELETE FROM  GRAPH <http://freebase.com> {?s ?p ?o} from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?o ="+e+") }"
        return [query_1,query_2]
    
    else:
        prefix="http://rdf.freebase.com/ns/"
        e="<"+prefix+e+">"
        query="DELETE FROM  GRAPH <http://freebase.com> {?s ?p ?o} from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?p ="+e+") }"
        #query_2="DELETE FROM  GRAPH <http://freebase.com> {?s ?p ?o} from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?o ="+e+") }"
        return [query]

    

def drop_eType_from_KG(schemaElements,eleType):
    schemaElements_error=[]
    if eleType=="rel":
        schemaElement=list(set(schemaElements))
    for schemaElement in schemaElements:
        if eleType=="rel":
            queries=get_queries_eType(schemaElement,"rel")
        else:
            queries=get_queries_eType(schemaElement,"eType")
            
        for query in queries:
            result=execute_query(query)
            if result=="error":
                schemaElements_error.append(schemaElement)
                print("error in:",eleType)
            elif "-- nothing to do" in result['results']['bindings'][0]['callret-0']['value']:
                schemaElements_error.append(schemaElement)
                print("not present in the KG:",eleType)
            else:
                continue
    return schemaElements_error

def get_queries_for_rel_drop(rels):
    rel,rel_rev=rels[0],rels[1]    
    prefix="http://rdf.freebase.com/ns/"
    rel="<"+prefix+rel+">"
    rel_rev="<"+prefix+rel_rev+">"
    query_1="DELETE FROM  GRAPH <http://freebase.com> {?s ?p ?o} from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?p ="+rel+") }"
    query_2="DELETE FROM  GRAPH <http://freebase.com> {?s ?p ?o} from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?p ="+rel_rev+") }" 
    if len(set(rels))==2:
           
        return [query_1,query_2]
    else:
        return [query_1]

def drop_rels_from_KG(relationships):
    rel_error=[]
    for index,rels in enumerate(relationships):
        queries=get_queries_for_rel_drop(rels)
        for i,query in enumerate(queries):
            result=execute_query(query)
            if result=="error":
                rel_error.append(rels[i])
                print("error in rel drop:",rels[i])
            elif "-- nothing to do" in result['results']['bindings'][0]['callret-0']['value']:
                rel_error.append(rels[i])
                print("rel is not present in the KG:",rels[i])
            else:
                continue
            
        
    return rel_error


def get_queries_for_entity_drop(e):
    prefix="http://rdf.freebase.com/ns/"
    e="<"+prefix+e+">"
        

    
    query_1="DELETE FROM  GRAPH <http://freebase.com> {?s ?p ?o} from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?s ="+e+") }"

    query_2="DELETE FROM  GRAPH <http://freebase.com> {?s ?p ?o} from <http://freebase.com> WHERE { ?s ?p ?o . filter ( ?o ="+e+") }"

    return [query_1,query_2]


def drop_entities_from_KG(entities):
    entity_error=[]
    for index,entity in enumerate(entities):
        queries=get_queries_for_entity_drop(entity)
        for query in queries:
            result=execute_query(query)
            
            if result=="error":
                entity_error.append(entity)
                print("error in entity drop:",entity)
            elif "-- nothing to do" in result['results']['bindings'][0]['callret-0']['value']:
                entity_error.append(entity)
                print("entity is not present in the KG:",entity)
            else:
                continue
            
        
    return entity_error

