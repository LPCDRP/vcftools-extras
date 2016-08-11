% VCFTOOLS-EXTRAS(7)
%
%

# NAME

vcftools-extras - extra utilities for manipulating files in variant call format

# DESCRIPTION

Our **vcftools-extras** is a collection of scripts for operations on VCF files that are expected to be available in the vcftools/bcftools suites.
These scripts are developed for internal use so, despite attempts at generality, they may not be adequate for general needs.
*Use these programs at your own risk.*

It currently contains the following programs:

vcf-combine-variants
:	combine consecutive variants of the same type

vcf-consenpos
:	determine position of variants in the consensus sequence

# BUGS

We appreciate contributions.
Please submit bug reports to our issue tracker at <https://github.com/valafarlab/vcftools-extras/issues>.

# SEE ALSO

**bcftools**(1)
**vcftools**(1)
