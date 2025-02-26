import sys
import json
import argparse
from pathlib import Path

from pymoo.core.problem import Problem
from pymoo.operators.sampling.lhs import LHS
import jsonschema

from . import settings
#===================================================================================================
# region: FUNCTIONS
#===================================================================================================
def parse_args():
    # create parser object
    parser = argparse.ArgumentParser(description = "Generate design variants using sampling algorithm")
 
    # defining arguments for parser object
    parser.add_argument('-n', '--nsamples', type = int, 
                        metavar = 'NSAMPLES', 
                        help = 'The number of variants to generate')
    
    parser.add_argument('-j', '--json', type = str, 
                        metavar = 'FILE', 
                        help = 'The file path of the json parametric file')
    
    parser.add_argument('-r', '--res', type = str, 
                        metavar = 'FILE', default= None,
                        help = 'The file path for the result')
    
    parser.add_argument('-p', '--process', action = 'store_true', default=False,
                        help = 'turn it on if piping in json filepath')
    
    # parse the arguments from standard input
    args = parser.parse_args()
    return args

def sample_pmtrs(nsamples: int, pmtrc_path: str, res_path: str):
    '''
    Generate parameters for the model.

    Parameters
    ----------
    nsamples: int
        number of samples to generate

    pmtrc_path: str
        The file path of the json parametric model.

    ifc_path : str
        The file path of ifc.

    res_path : str
        The path of the result file.
    
    var_dir : str
        The directory to store the generated variants.

    '''
    with open(pmtrc_path) as pmtrc_file:
        pmtrc_mod = json.load(pmtrc_file)
    
    # validate the file and make sure it is compliant
    json_data_dir = settings.JSON_DATA_DIR
    pmtrc_mod_schema_path = Path(json_data_dir).joinpath('pmtrc_mod_schema.json')
    with open(pmtrc_mod_schema_path) as schema_file:
        pmtrc_schema = json.load(schema_file)

    try:
        is_mod_valid = jsonschema.validate(instance=pmtrc_mod, schema=pmtrc_schema)
    except jsonschema.ValidationError as e:
        print(e.schema.get("error_msg", e.message))
        return False 
    
    pmtrs_dict = pmtrc_mod['parameters']
    pmtrs_vals = pmtrs_dict.values()
    npmtrs = len(pmtrs_vals)
    problem = Problem(n_var=npmtrs, xl=0, xu=1)
    sampling = LHS()
    pmtrs_nrmlz = sampling(problem, nsamples).get("X")
    pmtrs_nrmlz = pmtrs_nrmlz.tolist()
    pmtrc_mod['parameter_normalized_values'] = pmtrs_nrmlz

    pretty_json_data = json.dumps(pmtrc_mod, indent=4)
    with open(res_path, 'w') as f:
        f.write(pretty_json_data)
    return True

def main():
    args = parse_args()
    pipe_input = args.process
    if pipe_input == False:
        pmtrc_path = args.json
    else:
        lines = list(sys.stdin)
        pmtrc_path = lines[0].strip()

    nsamples = args.nsamples
    res_path = args.res
    if res_path == None:
        res_path = pmtrc_path
        
    res_path = str(Path(res_path).resolve())

    is_executed = sample_pmtrs(nsamples, pmtrc_path, res_path)
    if is_executed:
        # make sure this output can be piped into another command on the cmd
        print(res_path)
        sys.stdout.flush()
#===================================================================================================
# endregion: FUNCTIONS
#===================================================================================================
#===================================================================================================
# region: Main
#===================================================================================================
if __name__=='__main__':
    main()
#===================================================================================================
# endregion: Main
#===================================================================================================