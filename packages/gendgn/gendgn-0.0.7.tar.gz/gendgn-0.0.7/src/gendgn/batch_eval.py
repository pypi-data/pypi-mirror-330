import sys
import subprocess
import argparse
from time import perf_counter
from pathlib import Path

#===================================================================================================
# region: FUNCTIONS
#===================================================================================================
def parse_args():
    # create parser object
    parser = argparse.ArgumentParser(description = "Send all the variants to be evaluated")
 
    # defining arguments for parser object
    parser.add_argument('-v', '--var', type = str, 
                        metavar = 'DIR', 
                        help = 'The directory path containing all the design variants')
    
    parser.add_argument('-r', '--res', type = str, 
                        metavar = 'DIR', 
                        help = 'The directory path for the results')
    
    parser.add_argument('-e', '--epw', type = str,
                        metavar = 'FILE',
                        help = 'The file path of the weather file')
    
    parser.add_argument('-d', '--ddy', type = str,
                        metavar = 'FILE',
                        help = 'The file path of the ddy design day file')
    
    parser.add_argument('-m', '--measure', type = str, default=None,
                        metavar = 'FILE',
                        help = 'The file path of the json measures file that specify which measures to apply to the model')
    
    parser.add_argument('-p', '--process', action = 'store_true', default=False,
                        help = 'turn it on if piping in json filepath')
    
    # parse the arguments from standard input
    args = parser.parse_args()
    return args

def batch_eval_variants(var_dir: str, res_dir: str, epw_path: str, ddy_path: str, measure_path: str):
    '''
    Execute a parameteric model and generate a variant.

    Parameters
    ----------
    var_dir: str
        The directory path of the design variants.

    res_dir : str
        The path of the directory.
    
    epw_path : str
        The file path of the weather file.

    ddy_path : str
        The file path of the ddy design day file.

    measure_path : str
        The file path of the measures that will be applied to the model.
    
    '''
    filesx = Path(var_dir).glob('*.ifc')
    filesx = sorted(filesx)
    res_dir_pobj = Path(res_dir)
    call_list1 = ['ifcarch2osmod', '-i', '', '-o', '' ]
    call_list2 = ['add_sch2osmod', '-p', '-b', 'Small Office', '-c', '1A' ]
    call_list3 = ['execute_osmod', '-p', '-e', epw_path, '-d', ddy_path, '-m', measure_path, '-out', '']
    call_list4 = ['epsql2csv', '-s', '', '-r', '']

    t1 = perf_counter()
    for filex in filesx:
        t2 = perf_counter()
        filename = filex.stem
        this_res_dir = res_dir_pobj.joinpath(filename)
        this_res_dir.mkdir(parents=True, exist_ok=True)
        path_str = str(filex)
        call_list1[2] = path_str
        osm_path = this_res_dir.joinpath(f"{filename}.osm")
        call_list1[4] = str(osm_path)
        call_list3[9] = str(this_res_dir)
        
        sql_path = this_res_dir.joinpath(f"{filename}_wrkflw", 'run', 'eplusout.sql')
        csv_dir = this_res_dir.joinpath('csv')
        csv_dir.mkdir(parents=True, exist_ok=True)
        call_list4[2] = str(sql_path)
        call_list4[4] = str(csv_dir)
        print(f"executing openstudio model ... {filename}")
        try:
            process1 = subprocess.Popen(call_list1, stdout=subprocess.PIPE)
            process2 = subprocess.Popen(call_list2, stdin=process1.stdout, stdout=subprocess.PIPE)
            process3 = subprocess.Popen(call_list3, stdin=process2.stdout, stdout=subprocess.PIPE)
            output = process3.communicate()[0]
            print(output.decode())
        except subprocess.CalledProcessError as e:
            print("An error occurred:", e)

        res = subprocess.run(call_list4, capture_output=True, text=True)
        print(res.stdout)
        print(res.stderr)
        t3 = perf_counter()
        t32 = round((t3-t2)/60, 1)
        print(f"{t32} mins")

    t4 = perf_counter()
    t41 = round((t4 - t1)/60, 1)
    print(f"{t41} mins")
    
def main():
    args = parse_args()
    pipe_input = args.process
    if pipe_input == False:
        var_dir = args.var
    else:
        lines = list(sys.stdin)
        var_dir = lines[0].strip()

    var_dir = str(Path(var_dir).resolve())
    res_dir = args.res
    res_dir = str(Path(res_dir).resolve())
    epw_path = str(Path(args.epw).resolve())
    ddy_path = str(Path(args.ddy).resolve())
    mea_path = str(Path(args.measure).resolve())
    batch_eval_variants(var_dir, res_dir, epw_path, ddy_path, mea_path)
    # make sure this output can be piped into another command on the cmd
    print(res_dir)
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