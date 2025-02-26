import sys
import json
import argparse
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom

import ifc_utils
#===================================================================================================
# region: FUNCTIONS
#===================================================================================================
def parse_args():
    # create parser object
    parser = argparse.ArgumentParser(description = "Parameterize IFC model")
 
    # defining arguments for parser object
    parser.add_argument('-i', '--ifc', type = str, 
                        metavar = 'FILE', 
                        help = 'The file path of the IFC to convert')
    
    parser.add_argument('-r', '--res', type = str, 
                        metavar = 'FILE', 
                        help = 'The file path of the resultant json file')
    
    parser.add_argument('-p', '--process', action = 'store_true', default=False,
                        help = 'turn it on if piping in ifc filepath')
    
    # parse the arguments from standard input
    args = parser.parse_args()
    return args

def pmtrz_wwr_constr(ifc_path: str, res_path: str):
    '''
    Parameterize an ifc file.

    Parameters
    ----------
    ifc_path : str
        The file path of ifc.

    res_path : str
        The file path of the resultant json file.
    
    '''
    ifcmodel = ifcopenshell.open(ifc_path)
    bldg_dict = ifc_utils.ifcopenshell_utils.get_ifc_building_info(ifcmodel, envlp_pset_name='Pset_OsmodThermalResistance')
    ifc_bldgs = list(bldg_dict.values())
    nbldgs = len(ifc_bldgs)
    if nbldgs == 1:
        pmtrc_mod = {}
        pmtrc_mod['exe_script'] = 'exe_wwr_constr'
        pmtrs = {}
        pmtrs['wall_thermal_resistance'] = {'range': [0.5, 3]}
        pmtrs['roof_thermal_resistance'] = {'range': [3, 6]}
        pmtrs['floor_thermal_resistance'] = {'range': [3, 6]}
        pmtrs['glazing_uvalue'] = {'range': [0.5, 3]}
        pmtrs['north_wwr'] = {'range': [0.1, 0.4]}
        pmtrs['south_wwr'] = {'range': [0.1, 0.4]}
        pmtrs['east_wwr'] = {'range': [0.1, 0.4]}
        pmtrs['west_wwr'] = {'range': [0.1, 0.4]}
        pmtrc_mod['parameters'] = pmtrs

        # pretty json
        pretty_json_data = json.dumps(pmtrc_mod, indent=4)
        with open(res_path, 'w') as f:
            f.write(pretty_json_data)
    else:
        raise Exception("Unexpected number of buildings", nbldgs, "only 1 building allowed")

def main():
    args = parse_args()
    pipe_input = args.process
    if pipe_input == False:
        ifc_path = args.ifc
    else:
        lines = list(sys.stdin)
        ifc_path = lines[0].strip()

    res_path = args.res
    res_path = str(Path(res_path).resolve())
    ifc_path = str(Path(ifc_path).resolve())
    pmtrz_wwr_constr(ifc_path, res_path)
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