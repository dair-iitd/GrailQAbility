import update_KG
import os,json

cur_dir=os.getcwd()
data_dir = os.path.join(cur_dir,"data")

file_name="GrailQAbility_v1.0"

def load_json(split):
    file_reader=open(data_dir+os.sep+file_name+"_"+split+".json","r",encoding="utf-8")
    list_of_questions=json.load(file_reader)
    file_reader.close()
    return list_of_questions



def dump_json(split,final_questions):
    file_writer=open(data_dir+os.sep+file_name+"_"+split+".json","w",encoding="utf-8")
    json.dump(final_questions,file_writer,indent=4)
    file_writer.close()

def KG_update(KB_elements_to_drop):
    for transformationType in ["T_E","T_R","R","E","F"]:
        KB_element_to_drop=KB_elements_to_drop[transformationType]
        if transformationType=="T_E":
            
            error=update_KG.drop_eType_from_KG(KB_element_to_drop,"eType")
            dump_json("error_et_e_KG_update",error)
        elif transformationType=="T_R":
            
            error=update_KG.drop_eType_from_KG(KB_element_to_drop,"rel")
            dump_json("error_et_r_KG_update",error)
        elif transformationType=="R":
            
            error=update_KG.drop_rels_from_KG(KB_element_to_drop)
            dump_json("error_r_KG_update",error)
        elif transformationType=="E":
            
            error=update_KG.drop_entities_from_KG(KB_element_to_drop)
            dump_json("error_e_KG_update",error)
        elif transformationType=="F":
            
            error=update_KG.drop_facts_from_KG(KB_element_to_drop)
            dump_json("error_f_KG_update",error)
        else:
            sys.exit(0)
    
    literals_to_drop=load_json("error_f_KG_update")
    if len(literals_to_drop)>0:
        error=update_KG.drop_literals_from_KG(literals_to_drop)
        dump_json("error_literal_KG_update",error)
    

if __name__=="__main__":
    KB_elements_to_drop=load_json("KB_elements_to_drop")
    KG_update(KB_elements_to_drop)
