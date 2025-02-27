import ViennaRNA

rna_seq = "GAAAGGCGGCGAGGGGTGGACCCGACCAAAGGCGAGGCCGAGGGCAAAGCACCTCTACGGAAACCGAAGACCGCGAGGCGCAAGAAAAAAAAAAAAAAAAA"
strcuture = ".....(((.(..(.(((((.((((.((...)))).))))((((((...)).))))..(((...)))...))).)..).)))...................."


pred_rna_seq = "CGAAAGGCACGACGACCGGCGGCGACCAAAGGCGACCCCGCGCCCAACGGAGCGCAACCCAAAGGGAAAGGTGGGAGGGCCAAAAAAAAAAAAAGAAAAAG"

# wrong_rna_seq = "AAAAAGGTCCAGGCAAGCAACACGAGACAACCGGGCAGAGCAGGGGTCGGTGGGCGGCGGGACCAAAAAAAAAAAAAAAAAAAAA"
wrong_strcuture = ".....(((....(.(((((.((((.((...)))).))))((((((...)).))))..(((...)))...))).)....)))...................."


ViennaRNA.svg_rna_plot(rna_seq, strcuture, f"rna_structure.svg")
ViennaRNA.svg_rna_plot(pred_rna_seq, strcuture, f"predicted_structure.svg")
ViennaRNA.svg_rna_plot(rna_seq, wrong_strcuture, f"wrong_structure.svg")
