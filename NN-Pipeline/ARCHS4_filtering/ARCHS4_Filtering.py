import h5py
import archs4py as a4
import re
import numpy as np
import pandas as pd
import glob
import sys

def load_sample_names(txt_file_path):
    """Load sample names from a text file"""
    with open(txt_file_path, 'r') as f:
        sample_names = [line.strip() for line in f if line.strip()]
    return sample_names
    
class_sample_dict = dict()

# loop through all file paths in current directory to find files of interest
for filename in glob.glob("*3.txt"):
    file_path = "/scratch/by2372/pipeline/ARCHS4/" + filename
    # sample_names are within the text files and are the values of the class_sample_dict
    sample_names = load_sample_names(file_path)
    # class names are within the names of the text files
    class_name = filename.replace("3.txt","")

    class_sample_dict[class_name] = sample_names

# loop through each key value pairing in the dictionary and see if any source names have intersections with any other source name lists 
# in the dictionary. Print out the intersections if there are any
for key1, value1 in class_sample_dict.items():
    for key2, value2 in class_sample_dict.items():

        if key1 == key2:
            break 
        else:
            # Convert to sets and find intersection
            intersection_list = list(set(value1).intersection(set(value2)))
            if len(intersection_list) > 0:
                print(key1 + " and " + key2 + " classes have the following common source names: " + str(intersection_list))
                sys.stdout.flush()
            elif len(intersection_list) == 0:
                print("All source name lists are unique for each cell type!")
                sys.stdout.flush()
                
transcript_file_path = "/scratch/by2372/pipeline/ARCHS4/human_tpm_v2.2_NOSC.h5"

with h5py.File(transcript_file_path, "r") as fin, h5py.File('filtered_ARCHS4.h5', 'w') as fout:

    # copy the ensembl_ids and gene symbols to the new h5 file
    fin.copy("meta/transcripts/ensembl_id", fout)
    fin.copy("meta/transcripts/symbol", fout) 
    
    # Navigate to the metadata group for source names
    source_name_ds = fin['meta/samples/source_name_ch1']

    # Read all names and decode bytes to strings
    source_names = source_name_ds[:]
    if isinstance(source_names[0], bytes):
        source_names = [s.decode('utf-8') for s in source_names]

    # Get dataset info
    expr_dataset = fin['data/expression']
    n_genes, n_samples = expr_dataset.shape

    filtered_dataset = fout.create_dataset(
        "data/filtered_expression",
        (n_genes, 0),                    # start with 0 samples
        maxshape=(n_genes, None),        # allow dynamic extension
        dtype=expr_dataset.dtype,
        chunks=True
    )
    
    class_name_dataset = fout.create_dataset(
        "class_name",
        (0,),                            # start empty
        maxshape=(None,),                # allow appending
        dtype=source_name_ds.dtype,
        chunks=True
    )

    current_pos = 0

    for key, value in class_sample_dict.items():

        print("Matching indices for " + str(key))
        sys.stdout.flush()
        
        matched_indices = []
        class_names = []
        
        for filt_name in set(value): 
            matched_indices.extend([
                i for i, n in enumerate(source_names)
                if n.lower() == filt_name.lower()
            ])

        matched_indices.sort()
        n_new = len(matched_indices)
        print(str(n_new))
        cur_class_names = [key] * n_new
        class_names.append(cur_class_names)

        filtered_dataset.resize((n_genes, current_pos + n_new))
        class_name_dataset.resize((current_pos + n_new,))
        
        # Process in chunks of genes instead of loading all at once
        chunk_size = 1000  # Adjust based on your memory
        iteration = 0
        for start_gene in range(0, n_genes, chunk_size):
            end_gene = min(start_gene + chunk_size, n_genes)
            
            # Read chunk of data for matched samples only
            chunk_data = expr_dataset[start_gene:end_gene, matched_indices]
            
            # Write to output
            filtered_dataset[start_gene:end_gene, current_pos:current_pos + n_new] = chunk_data
            iteration = iteration + 1
            print("Iteration " + str(iteration)+ " is done.")
            sys.stdout.flush()


        class_name_dataset[current_pos:current_pos + n_new] = class_names
        
        current_pos += n_new