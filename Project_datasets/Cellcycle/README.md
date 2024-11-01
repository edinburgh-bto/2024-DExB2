# 2023_DEB_cellcycle

Data Exploration in Biology Yeast Cell Cycle Project Dataset

# `cell_cycle_gene_expression_intro.ipynb`

Notebook describing dataset and how to get started loading, cleaning, exploring.


# `GSE80474_Scerevisiae_normalized.txt`


From Supplementary data S1:

> Transcript quantification of annotated yeast genes was performed using alignment files output from STAR and Cufflinks2 [4]. Time point samples from the respective yeasts were then normalized together using the CuffNorm feature. The normalized FPKM gene expression outputs (“genes.fpkm_table”) were used in the analyses presented. To avoid fractional and zero values, 1 was added to every FPKM value in each dataset using the R statistical programming environment [5]. Fractions and zeros were found to interfere with the periodicity algorithms that involved log-transformation of data points (data not shown). Normalized gene expression data for each yeast are available in S1 and S2 Tables. Raw RNA-Sequencing data from this manuscript have been submitted to the NCBI Gene Expression Omnibus (GEO; http://www.ncbi.nlm.nih.gov/geo/) under accession number GSE80474.

# `yeast_gene_name_descriptions_2023-09-11.tsv`

Downloaded from https://yeastmine.yeastgenome.org/ by Edward Wallace, using the query:

```
<query name="" model="genomic" view="Gene.secondaryIdentifier Gene.symbol Gene.primaryIdentifier Gene.name Gene.description Gene.qualifier Gene.chromosome.primaryIdentifier Gene.chromosomeLocation.start Gene.chromosomeLocation.end Gene.chromosomeLocation.strand" longDescription="" sortOrder="Gene.primaryIdentifier asc" constraintLogic="(A or B) and C">
  <join path="Gene.chromosome" style="OUTER"/>
  <join path="Gene.chromosomeLocation" style="OUTER"/>
  <constraint path="Gene.status" code="B" op="IS NULL"/>
  <constraint path="Gene.status" code="A" op="=" value="Active"/>
  <constraint path="Gene" code="C" op="IN" value="ALL_Verified_Uncharacterized_Dubious_ORFs"/>
</query>
```

Note "Data Updated on: Sep-5-2023; GO-Release: 2023-07-27", so that's genome build R64-4-1 from 2023-08-30.

Gene.secondaryIdentifier	Gene.symbol	Gene.primaryIdentifier	Gene.name	Gene.description	Gene.qualifier	Gene.chromosome.primaryIdentifier	Gene.chromosomeLocation.start	Gene.chromosomeLocation.end	Gene.chromosomeLocation.strand

# `2014-04-21_Kelliher_ScerevisiaeBudCounts.xlsx`

Data on number of budded cells in S. cerevisiae synchronized with alpha factor, that underlies Figure 1A in Kelliher et al 2016.
