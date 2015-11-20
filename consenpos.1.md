% CONSENPOS(1) 0.1
% Afif Elghraoui <aelghraoui@sdsu.edu>
% November 2015

# NAME

consenpos - get consensus positions for variants listed in VCF files

# SYNOPSIS

**consenpos** < *variants.vcf* > *out.vcf*

# DESCRIPTION

The Variant Call Format (VCF) shows the positions of variants with respect
to the reference, but does not provide information about the position of
the variant on the consensus sequence. **consenpos** adds a new INFO field
to the input VCF file with this information.

# SEE ALSO

**vcftools**(1)
