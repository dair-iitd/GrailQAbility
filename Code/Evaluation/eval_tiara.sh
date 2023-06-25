
python final_evaluation.py \
     --model 'tiara' \
     --data ../GrailQAbility/grailqa_v1.0_test_a_na_reference.json \
     --predict results/Tiara/train_A_U_threshold_Tiara_model_test_A_U.json \
     --fb_roles ontology/fb_roles \
     --fb_types ontology/fb_types \
     --reverse_properties ontology/reverse_properties \
     --partial_zero_shot_type_drop ../GrailQAbility/entity_type_deletion/test/zero-shot/partial/grailqa_v1.0_test_eType_npuua.json \
     --complete_zero_shot_type_drop ../GrailQAbility/entity_type_deletion/test/zero-shot/full/grailqa_v1.0_test_eType_ncuua.json \
     --partial_zero_shot_rel_drop ../GrailQAbility/relation_deletion/test/zero-shot/partial/grailqa_v1.0_test_rel_npuua.json \
     --complete_zero_shot_rel_drop ../GrailQAbility/relation_deletion/test/zero-shot/full/grailqa_v1.0_test_rel_ncuua.json \
