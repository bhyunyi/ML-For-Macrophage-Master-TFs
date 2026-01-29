import archs4py as a4
import h5py
import sys

file = "/scratch/by2372/pipeline/ARCHS4/human_tpm_v2.2.h5"

with h5py.File(file, "r") as fin, h5py.File('human_tpm_v2.2_NOSC.h5', 'w') as fout:

    fin.copy("meta/transcripts/ensembl_id", fout, name="meta/transcripts/ensembl_id")
    fin.copy("meta/transcripts/symbol", fout, name="meta/transcripts/symbol")

    expr_data = fin['data/expression']
    
    # Navigate to the metadata group for source names
    source_name_ds = fin['meta/samples/source_name_ch1']

    # Read all names and decode bytes to strings
    source_names = source_name_ds[:]
    if isinstance(source_names[0], bytes):
        source_names = [s.decode('utf-8') for s in source_names]

    library_source_ds = fin['meta/samples/library_source']

    # Read all names and decode bytes to strings
    library_source = library_source_ds[:]
    if isinstance(library_source[0], bytes):
        library_source = [s.decode('utf-8') for s in library_source]

    print("Finding matched indices for transcriptomic samples")
    sys.stdout.flush()
    
    n_genes, n_samples = expr_data.shape
    sample_idx = range(n_samples)
    chunk_size = 2000

    # Create an empty dataset for the filtered expression in fout
    new_expr_data = fout.create_dataset(
        "data/expression",
        (n_genes, 0),                    # start with 0 samples
        maxshape=(n_genes, None),        # allow dynamic extension
        dtype=expr_data.dtype,
        chunks=True
    )

    # Create an empty dataset for the class_names in fout
    new_source = fout.create_dataset(
        "meta/samples/source_name_ch1",
        (0,),                            # start empty
        maxshape=(None,),                # allow appending
        dtype=source_name_ds.dtype,
        chunks=True
    )

    sample = 0
    for start_sample in range(0, n_samples, chunk_size):
        end_sample = min(start_sample+chunk_size, n_samples)
        chunk_lib = library_source[start_sample:end_sample]

        for i, lib in enumerate(chunk_lib):
            if ("transcriptomic" in lib.lower()) and ("single" not in lib.lower()):
                idx = start_sample + i
                matched_source = source_names[idx]
                new_source.resize((sample + 1,))
                new_source[sample] = matched_source
                new_expr_data.resize((n_genes, sample + 1))
                for start_gene in range(0, n_genes, chunk_size):
                    end_gene = min(start_gene + chunk_size, n_genes)
                    chunk_expr = expr_data[start_gene:end_gene, idx]
                    new_expr_data[start_gene:end_gene,sample] = chunk_expr

                sample += 1
                print("Sample " + str(sample) + " is done.")
                sys.stdout.flush()

                    
                
    print("Matched indices for transcriptomic samples have been found")
    sys.stdout.flush()