# Freebase Setup
- Please follow the steps mentioned on https://github.com/dki-lab/Freebase-Setup for freebase download and setup.

- Once virtuoso is up, run the following commands so that KG can be updated via program.
```
cd virtuoso-opensource/bin 
./isql 13001
grant SPARQL_UPDATE to "SPARQL";
exit();
```

## Introduce incompletness in Freebase by dropping KB elements
```
python update_KG_main.py
```
## Update files presents in the ontology folder
```
python update_ontology.py 
```

## Validate the updated KG
- Copy GrailQAbility_v1.0_split_a_na_reference.json from GrailQAbility corresponding to all splits (train, dev and test) to data folder and run following command for KG validation.
```
python validate_updated_KG.py
```
# Experiments on GrailQAbility with different KBQA models
- Pls refer to ReTraCk, RnG-KBQA and TIARA folder for this.
