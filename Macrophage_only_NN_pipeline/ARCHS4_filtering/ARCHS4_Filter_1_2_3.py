import h5py
import sys

file = "/scratch/by2372/pipeline/ARCHS4_Macrophages/human_tpm_v2.latest.h5"

with h5py.File(file, "r") as fin, h5py.File('human_tpm_v2.2_NOSC.h5', 'w') as fout:

    # copy over the transcript IDs and gene symbols to the new h5 file
    fin.copy("meta/transcripts/ensembl_id", fout, name="meta/transcripts/ensembl_id")
    fin.copy("meta/transcripts/symbol", fout, name="meta/transcripts/symbol")

    # define a variable containing the expression data
    expr_data = fin['data/expression']

    # import source names
    source_names = fin['meta/samples/source_name_ch1'][:]

    # import library source labels
    library_source = fin['meta/samples/library_source'][:]

    # import the molecule name
    molecule = fin['meta/samples/molecule_ch1'][:]

    # import the sample characteristics
    characteristics = fin['meta/samples/characteristics_ch1'][:]

    # import the single cell probability values
    SC_prob = fin['meta/samples/singlecellprobability'][:]
    
    # import the single cell probability values
    geo_num = fin['meta/samples/geo_accession'][:]

    print("Finding matched indices for transcriptomic samples and non-single cell samples")
    sys.stdout.flush()

    # Define the needed metrics to find samples of interest for new H5 file
    n_genes, n_samples = expr_data.shape
    chunk_size = 2000


    # Create an empty dataset for the filtered expression in fout
    new_expr_data = fout.create_dataset(
        "data/expression",
        (n_genes, 0),                    # start with 0 samples
        maxshape=(n_genes, None),        # allow dynamic extension
        dtype=expr_data.dtype,
        chunks=True
    )

    # Create an empty dataset for the source_name in fout
    new_source = fout.create_dataset(
        "meta/samples/source_name_ch1",
        (0,),                            # start empty
        maxshape=(None,),                # allow appending
        dtype=source_names.dtype,
        chunks=True
    )

    # Create an empty dataset for characteristics_ch1 in fout
    new_char = fout.create_dataset(
        "meta/samples/characteristics_ch1",
        (0,),                            # start empty
        maxshape=(None,),                # allow appending
        dtype=characteristics.dtype,
        chunks=True
    )
    
    # Create an empty dataset for geo_num in fout
    new_geo = fout.create_dataset(
        "meta/samples/geo_accession",
        (0,),                            # start empty
        maxshape=(None,),                # allow appending
        dtype=geo_num.dtype,
        chunks=True
    )

    sample = 0
    for start_sample in range(0, n_samples, chunk_size):
        end_sample = min(start_sample+chunk_size, n_samples)
        chunk_lib = library_source[start_sample:end_sample]
        chunk_molecule = molecule[start_sample:end_sample]
        chunk_SC_prob = SC_prob[start_sample:end_sample]

        for i in range(end_sample - start_sample):
            lib = chunk_lib[i].lower()
            mole = chunk_molecule[i].lower()
            if (chunk_SC_prob[i] < 0.5):
                if (b"transcriptomic" in lib) and (b"single" not in lib):
                    if (b'total rna' in mole) or (b'cytoplasmic rna' in mole) or (b'polya rna' in mole) or (b'nuclear rna' in mole):
                        idx = start_sample+i
                        matched_source = source_names[idx]
                        new_source.resize((sample + 1,))
                        new_source[sample] = matched_source

                        matched_char = characteristics[idx]
                        new_char.resize((sample + 1,))
                        new_char[sample] = matched_char
                        
                        matched_geo = geo_num[idx]
                        new_geo.resize((sample + 1,))
                        new_geo[sample] = matched_geo

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