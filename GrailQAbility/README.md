# GrailQAbility

- "GrailQAbility_dataset.zip" contains 3 dataset files.

    -  "GrailQAbility_v1.0_{split}_a_na_reference.json" contains answerable and unanswerable questions corresponding to different data splits (train, dev and test).

    - Answerable questions have same data format as GrailQA. While unanswerable questions are tagged with following new fields:

        - qType ["A", "U"]: indicates whether a questions is answerable (A) or unanswerable (U). 

        - Missing_KB_elements ["T" (Type),"E" (Entity),"F" (Fact),"R" (Relation),"none"]: A question is unanswerable due to what type of KG incompleteness. If qType is "A" then Missing_KB_elements will be "none". Otherwise it can take more than one value from ["T","E","F","R"].

        - answer:  For unanswerable questions it's NA. It can take two values, "0" for count questions and [] for others. Othewise it's same as answer field in GrailQA.

        - Organswer: non-empty ideal answers with respect to the ideal KB. And format is same as GrailQA.

        - s_expression: For unanswerable questions due to schema level incompleteness and missing mentioned entity it's NK ("no logical form") and valid logical form if questions is unanswerable due to data level incompleteness. For answerable questions it's same as valid logical form.

        - Orgs_expression: valid ideal logical form l* with respect to the ideal KB.

        - level: For answerable questions level  of generalization is same as defined in GrailQA. For unanswerable questions the generalization level of a question can be "iid" and "zero-shot". 

- Unanswerble Questions due to KB incompletness. Details of questions corresponding to different types of KB incompletness is present under respective folders.

    - entity_deletion: It contains qids of unanswerable questions due to "entity drop" and also include information about which question is part of which split (i.e., train, dev and test). And for dev and test whether it's part of iid or zero-shot.

    - entity_type_deletion: It contains qids of unanswerable questions due to "type drop" and also include information about which question is part of which split (i.e., train, dev and test). And for dev and test whether it's part of iid or zero-shot. And for zero-shot whether it's partial or full. 

    - fact_deletion: It contains qids of unanswerable questions due to "fact drop" and also include information about which question is part of which split (i.e., train, dev and test). And for dev and test whether it's part of iid or zero-shot.

    - relation_deletion: It contains qids of unanswerable questions due to "relation drop" and also include information about which question is part of which split (i.e., train, dev and test). And for dev and test whether it's part of iid or zero-shot. And for zero-shot whether it's partial or full. 