# ML-For-Macrophage-Master-TFs

Identifying novel master transcription factors and confirming studied cell
 type markers in macrophages using machine learning

---

## Project Overview

This project investigates whether machine learning models trained on transcription 
factor expression profiles can distinguish the gene regulatory networks of 
different cell types and find the master transcription factors for macrophages.

This project was done in collaboration with Dr. David Truong's lab at NYU 
Tandon School of Engineering, Department of Biomedical Engineering. 

There are three parts to this project: 
1. Training L1 Logistic Regression, Random Forest, and XGBoost models on the 
Truong Lab's database of bulk RNA-sequenced immune cells.
2. Training Neural Network model on bulk RNA-seq data of immune cells from 
ARCHS4. This includes transcription factor perturbation analysis to investigate 
key macrophage markers. 
3. Training Neural Network model on bulk RNA-seq data of macrophage subtypes 
from ARCHS4. This includes transcription factor perturbation analysis to 
investigate key macrophage markers. 

**Contents**

- Research Question and Motivation
- Methodology
- Data Curation
- Results
- Feature Selection and TF Perturbation Results
- Repository Structure
- Limitations and Next Steps
- References   

---

## Research Question and Motivation

I am investigating whether trained machine learning models can identify novel 
and known master transcription factors using feature selection functionalities. 
In the Truong Lab there is a need for identifying key transcription factors to 
be used in forward programming of iPSCs to macrophages. Macrophages have central 
functions in the human immune system that include metabolic functions, 
tissue repair, and clearing debris. This is an affected cell type in a variety of 
immune disorders and conditions, and is a major focus in immunology in general. 
Through the harmonization of the results from the three parts of this project, 
I was able to distinguish ZNF385A, CEBPA, CEBPB, and TSC22D1 as commonly 
recurring transcription factors that arose from feature selection or feature 
perturbations. With these results, the Truong lab will investigate the efficacy 
of these factors within the forward programming of their iPSC cultures.

---

## Methodology

The three parts of this project had differing methodologies:

### Part 1: Training Logreg, Random Forest, XGBoost on internal RNA-Seq database:

* The contents of this part of the project are within the Non-NN-Pipeline folder of this repository

Part 1 started with the curation of data through the Sequence Read Archive or SRA from the
NIH. An extensive literature search was performed to find the SRA IDs of wildtype, non-diseased, 
and unedited cells that were sourced from primary cells or iPSCs. These samples belonged to the 
myeloid, lymphoid, and non-mesodermal lineages which also included macrophages. There were 122 
compiled SRA ID numbers that were subsequently Kallisto pseudoaligned to generate gene expression 
values. It is important to note that the macrophage category of samples was split into M0, M1, and 
M2 polarized samples, and that the this curated database was heavily imbalanced in regard to the 
number of samples for each included cell type. 

Prior to model training, the gene expression data was processed by normalizing the cell 
type class labels and by filtering for the expression values of known transcription factor genes. 
We wanted the trained models to learn how the expression of transcription factor genes related 
to the given cell type classifications. The data was then split into training and testing data 
via a 75:25 split, and the training data was log2 transformed and scaled using the StandardScaler 
object in python. The testing data was also log2 transformed and scaled using the StandardScaler 
object that was fit to the training data. Four different training datasets were generated using 
 methods of data oversampling to generate balanced datasets. I used Random Oversampler, 
SMOTE, and BorderlineSMOTE as the oversampling methods while the unbalanced dataset was the fourth 
training dataset. I created python functions to perform Bayesian Optimzation on the L1 Logreg, 
Random Forest, and XGBoost models for each of the four training datasets. Each instance of 
parameter optimization and model training was evaluated on the AUCs of the individual classes, 
micro-averaged AUC, micro-averaged F1 score, and accuracy. 

Once the models with the best evaluation metrics were found, I performed feature selection or 
feature importance evalutions to find the top 20 transcription factors that impacted the model 
classifications the most. From these top 20 lists, I performed literature searches to find out 
if the lists contained existing master transcription factors for macrophages, or undiscovered 
candidates. 

### Part 2: Training Neural Network model on bulk RNA-seq data from ARCHS4 (Immune Cells):


### Part 3: Training Neural Network model on bulk RNA-seq data from ARCHS4 (Macrophage Subtypes):


---

## Data Curation


---

## Results

---

## Feature Selection and TF Perturbation Results

---

## Repository Structure

---

## Limitations and Next Steps

---

## References


