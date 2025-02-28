from bycon import BYC, BYC_PARS, ByconResultSets, prdbug, print_uri_rewrite_response
from byconServiceLibs import PGXbed


def variantsbedfile():
    """
    The `variantsbedfile` function provides a BED file with the matched genomic
    variants from a Beacon query or a sample id. Since the UCSC browser only
    displays one reference (chromosome) this methos is intended to be used upon
    specific variant queries, though.

    #### Examples

    * http://progenetix.org/services/variantsbedfile/pgxbs-kftvjv8w ... not very good since multiple chromosomes...
    """
    # 
    f_d = ByconResultSets().get_flattened_data()
    BED = PGXbed(f_d)
    if "ucsc" in BYC_PARS.get("output", "bed").lower():
        print_uri_rewrite_response(BED.bed_ucsc_link())
    print_uri_rewrite_response(BED.bedfile_link())

