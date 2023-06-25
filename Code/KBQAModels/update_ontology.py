import os,json
from collections import defaultdict
cur_dir=os.getcwd()
data_dir = os.path.join(cur_dir,"data")
file_name="grailqa_v1.0"
#domain="conferences"
def load_json(split):
    file_reader=open(data_dir+os.sep+file_name+"_"+split+".json","r",encoding="utf-8")
    list_of_questions=json.load(file_reader)
    file_reader.close()
    return list_of_questions



def dump_json(split,final_questions):
    #unique_caption_list={}
    file_writer=open(data_dir+os.sep+file_name+"_"+split+".json","w",encoding="utf-8")
    json.dump(final_questions,file_writer,indent=4)
    file_writer.close()

def load_json_v1(fname):
    with open(fname) as f:
        return json.load(f)

def dump_json_v1(obj, fname, indent=None):
    with open(fname, 'w') as f:
        return json.dump(obj, f, indent=indent)


def get_rels():
    schema_items_to_drop=load_json("schema_items_to_drop")
    et_e=schema_items_to_drop["T_E"]
    et_r=schema_items_to_drop["T_R"]
    r=schema_items_to_drop["R"] 
    all_dropped_rels=[]
    et_r=list(set(et_r))
    all_dropped_rels.extend(et_r)
    for rel in r:
        rel=list(set(rel))
        all_dropped_rels.extend(rel)
    all_dropped_rels=list(set(all_dropped_rels))
    print(len(all_dropped_rels))
    return all_dropped_rels,list(set(et_e))

def update_rel_freq(dropped_rels):
    rel_freq=load_json_v1("ontology/relation_freq.json")
    rel_freq_updated={}
    print(len(rel_freq))
    rel_dropped_from_rel_freq=[]
    for rel,count in rel_freq.items():
        if rel in dropped_rels:
            rel_dropped_from_rel_freq.append(rel)
            continue
        else:
            rel_freq_updated[rel]=count
    print(len(rel_freq_updated))
    print(len(set(dropped_rels).difference(set(rel_dropped_from_rel_freq))))
    dump_json_v1(rel_freq_updated, "ontology/relation_freq_updated.json", indent=None)


def update_fb_types(dropped_types):
    #fb_roles=load_json_v1("ontology/fb_roles")
    with open('ontology/fb_types', 'r') as f:
        contents = f.readlines()
    print(len(contents))
    fb_types_updated=[]
    fb_types_dropped_from_fb_types=[]
    for line in contents:
        fields = line.split()
        eType1=fields[0]
        eType2=fields[2]
        if eType1 in dropped_types :
            fb_types_dropped_from_fb_types.append(eType1)
        elif eType2 in dropped_types:
            fb_types_dropped_from_fb_types.append(eType2) 
            
        else:
            fb_types_updated.append(line)
    print(len(fb_types_updated))
    print(set(dropped_types).difference(set(fb_types_dropped_from_fb_types)))
    with open('ontology/fb_types_updated', 'w') as f:
        f.writelines(fb_types_updated)


def update_fb_roles(dropped_rels):
    #fb_roles=load_json_v1("ontology/fb_roles")
    with open('ontology/fb_roles', 'r') as f:
        contents = f.readlines()
    print(len(contents))
    fb_roles_updated=[]
    fb_roles_dropped_from_fb_roles=[]
    for line in contents:
        fields = line.split()
        rel=fields[1]
        if rel in dropped_rels:
            fb_roles_dropped_from_fb_roles.append(rel)
            
        else:
            fb_roles_updated.append(line)
    print(len(fb_roles_updated))
    print(set(dropped_rels).difference(set(fb_roles_dropped_from_fb_roles)))
    with open('ontology/fb_roles_updated', 'w') as f:
        f.writelines(fb_roles_updated)
    #dump_json_v1(fb_roles_updated, "ontology/fb_roles_updated", indent=None)

def update_full_reverse_properties(dropped_rels):
    rels=load_json_v1("ontology/full_reverse_properties.json")
    print(len(rels))
    full_reverse_properties_updated={}
    full_reverse_properties_dropped_from_full_reverse_properties=set()
    for rel,rel_rev in rels.items():
        if rel in dropped_rels or rel_rev in dropped_rels:
            full_reverse_properties_dropped_from_full_reverse_properties.add(rel)
            full_reverse_properties_dropped_from_full_reverse_properties.add(rel_rev)
            
        else:
            full_reverse_properties_updated[rel]=rel_rev
    print(len(full_reverse_properties_updated))
    print(len(set(dropped_rels).difference(set(full_reverse_properties_dropped_from_full_reverse_properties))))
    #with open('ontology/fb_roles_updated', 'w') as f:
    #    f.writelines(fb_roles_updated)
    dump_json_v1(full_reverse_properties_updated, "ontology/full_reverse_properties_updated.json", indent=None)

def update_reverse_properties(dropped_rels):
    #rels=load_json_v1("ontology/reverse_properties.json")
    with open('ontology/reverse_properties', 'r') as f:
        contents = f.readlines()
    print(len(contents))
    reverse_properties_updated=[]
    reverse_properties_dropped_from_reverse_properties=set()
    for line in contents:
        content=line.split("\t")
        rel,rel_rev=content[0],content[1]
        if rel in dropped_rels or rel_rev in dropped_rels:
            reverse_properties_dropped_from_reverse_properties.add(rel)
            reverse_properties_dropped_from_reverse_properties.add(rel_rev)
            
        else:
            reverse_properties_updated.append(line)
    print(len(reverse_properties_updated))
    print(len(set(dropped_rels).difference(set(reverse_properties_dropped_from_reverse_properties))))
    with open('ontology/reverse_properties_updated', 'w') as f:
        f.writelines(reverse_properties_updated)
    #dump_json_v1(reverse_properties_updated, "ontology/full_reverse_properties_updated.json", indent=None)

def update_domain_info(dropped_rels,dropped_types):
    #with open('ontology/domain_info', 'r') as f:
    #    contents = f.readlines()
    contents=load_json_v1("ontology/domain_info")
    print(len(contents))
    domain_info_updated={}
    domain_info_dropped_from_domain_info=set()
    for item,domain in contents.items():
        if item in dropped_rels or item in dropped_types:
            domain_info_dropped_from_domain_info.add(item)
            
            
        else:
            domain_info_updated[item]=domain
    print(len(domain_info_updated))
    #print(len(set(dropped_rels).difference(set(reverse_properties_dropped_from_reverse_properties))))
    #with open('ontology/reverse_properties_updated', 'w') as f:
    #    f.writelines(reverse_properties_updated)
    dump_json_v1(domain_info_updated, "ontology/domain_info_updated", indent=None)


def update_domain_dict(dropped_rels,dropped_types):
    #with open('ontology/domain_info', 'r') as f:
    #    contents = f.readlines()
    contents=load_json_v1("ontology/domain_dict")
    print(len(contents))
    domain_dict_updated=defaultdict(list)
    domain_dict_dropped_from_domain_dict=set()
    domain_org=set()
    domain_now=set()
    for domain,values in contents.items():
        domain_org.add(domain)
        for value in values:
            if value in dropped_rels or value in dropped_types:
                domain_dict_dropped_from_domain_dict.add(value)
            
            
            else:
                domain_now.add(domain)
                domain_dict_updated[domain].append(value)
    print(len(domain_dict_updated))
    print(domain_org.difference(domain_now))
    #print(len(set(dropped_rels).difference(set(reverse_properties_dropped_from_reverse_properties))))
    #with open('ontology/reverse_properties_updated', 'w') as f:
    #    f.writelines(reverse_properties_updated)
    dump_json_v1(domain_dict_updated, "ontology/domain_dict_updated", indent=None)

        
print("========================================")
dropped_rels,dropped_types=get_rels()
print("========================================")
update_rel_freq(dropped_rels)
print("========================================")
update_fb_roles(dropped_rels)
print("========================================")
update_fb_types(dropped_types)
print("========================================")
update_full_reverse_properties(dropped_rels)
print("========================================")
update_reverse_properties(dropped_rels)
print("========================================")
update_domain_info(dropped_rels,dropped_types)
print("========================================")
update_domain_dict(dropped_rels,dropped_types)
