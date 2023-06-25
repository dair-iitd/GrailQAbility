# Evaluate KBQA models on GrailQAbility
- Create a folder corresponding to a new KBQA model inside evaluate/results/kbqa_new and put four prediction files inside it, two for each of the following setting i.e.,
## Scenario-1
- Training 
    - On answerable questions only
- Inference
    - without thresholding
    - Adaptation for answerability via thresholding on entity linking and logical form
## Scenario-2
- Training
    - on answerable and unanswerable quetions
- Inference
    - without thresholding
    - Adaptation for answerability via thresholding on entity linking and logical form

## To get the results reported in the paper for different KBQA models on GrailQAbility pls run the following commands
```
- RnG-KBQA
    - bash eval_rng.sh
- ReTraCk
    - bash eval_retrack.sh
- TIARA
    - bash eval_tiara.sh
```
