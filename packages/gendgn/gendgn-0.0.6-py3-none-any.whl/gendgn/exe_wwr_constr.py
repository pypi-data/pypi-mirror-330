import sys
import json
import argparse
from pathlib import Path

from ifc_utils import ifcopenshell_utils
import numpy as np
import ifcopenshell
import ifcopenshell.geom
import geomie3d
from geomie3d import geom
import geomie3d.viz
import ifc_utils
import jsonschema

from . import settings
#===================================================================================================
# region: FUNCTIONS
#===================================================================================================
def parse_args():
    # create parser object
    parser = argparse.ArgumentParser(description = "Execute Window-Wall Ratio & Cosntruction parametric model")
 
    # defining arguments for parser object
    parser.add_argument('-j', '--json', type = str, 
                        metavar = 'FILE', 
                        help = 'The file path of the json parametric file')
    
    parser.add_argument('-i', '--ifc', type = str, 
                        metavar = 'FILE', 
                        help = 'The file path of the original IFC')
    
    parser.add_argument('-r', '--res', type = str, 
                        metavar = 'DIR', 
                        help = 'The directory path for the results')
    
    parser.add_argument('-p', '--process', action = 'store_true', default=False,
                        help = 'turn it on if piping in json filepath')
    
    # parse the arguments from standard input
    args = parser.parse_args()
    return args

def open_ifc_file(ifc_path: str):
    '''
    Open ifc path and extract all the objects.

    Parameters
    ----------
    ifc_path : str
        The file path of ifc.

    Returns
    -------
    np.ndarray
        np.ndarray[shape(nvariants, nparameters)] the mapped parameters.

    '''
    ifcmodel = ifcopenshell.open(ifc_path)
    ifc_wall_ls = ifcmodel.by_type('IfcWall')
    ifc_roof_ls = ifcmodel.by_type('IfcRoof')
    ifc_slab_ls = ifcmodel.by_type('IfcSlab')
    ifc_win_ls = ifcmodel.by_type('IfcWindow')
    ifc_door_ls = ifcmodel.by_type('IfcDoor')
    ifc_gls_door_ls = []
    for ifc_door in ifc_door_ls:
        psets = ifcopenshell.util.element.get_psets(ifc_door, psets_only=True)
        pset_names = list(psets.keys())
        if 'Pset_OsmodUfactor' in pset_names:
            ifc_gls_door_ls.append(ifc_door)

    return ifcmodel, ifc_wall_ls, ifc_roof_ls, ifc_slab_ls, ifc_win_ls, ifc_gls_door_ls

def extract_srfs_frm_envlp_dicts(envlp_dicts: dict) -> list[geomie3d.topobj.Face]:
    '''
    Extract surfaces from envlp_dicts.

    Parameters
    ----------
    envlp_dicts: dict
        dictionary generated from ifc_utils.ifcopenshell_utils.get_ifc_envlp_info
    
    Returns
    --------
    list[geomie3d.topobj.Face]
        surfaces from the dictionary
    '''
    envlp_vals = envlp_dicts.values()
    envlp_srf_ls = []
    for envlp_val in envlp_vals:
        envlp_srfs = envlp_val['surfaces']
        envlp_srf_ls.extend(envlp_srfs)
    return envlp_srf_ls

def map_nrmlz_vals(pmtrs_meta: dict, nmlz_pmtrs: list[list[float]]) -> np.ndarray:
    '''
    Map the normalized values to the actual parameters value.

    Parameters
    ----------
    pmtrs_meta: dict
        Dictionary of the parameters meta data.
    
    nmlz_pmtrs: list[list[float]
        list of normalize parameters.

    Returns
    -------
    np.ndarray
        np.ndarray[shape(nvariants, nparameters)] the mapped parameters.

    '''
    pmtr_vals = pmtrs_meta.values()
    npmtrs = len(pmtr_vals)
    val_mn_mxs = []
    for pmtr_val in pmtr_vals:
        val_mn_mx = pmtr_val['range']
        val_mn_mxs.append(val_mn_mx)
    val_mn_mxs = np.array(val_mn_mxs)
    val_mn_mxsT = val_mn_mxs.T
    val_mns = val_mn_mxsT[0]
    val_ranges = val_mn_mxsT[1] - val_mns
    val_ranges = np.reshape(val_ranges, (npmtrs,1))

    nmlz_pmtrs = np.array(nmlz_pmtrs)
    nrmlz_valsT = nmlz_pmtrs.T
    actl_vals = nrmlz_valsT*val_ranges
    val_mns_rshp = np.reshape(val_mns, (npmtrs,1))
    actl_vals = actl_vals + val_mns_rshp
    actl_valsT = actl_vals.T
    actl_valsT = np.round(actl_valsT, decimals=2)
    return actl_valsT

def find_host_of_win(ifc_wins: list[ifcopenshell.entity_instance], spacezn_srfs: list[geomie3d.topobj.Face]):
    '''
    Find the host of the window. This function will add window attribute to the spacezn_surfs.

    Parameters
    ----------
    ifc_wins: list[ifcopenshell.entity_instance]
        The windows in the ifc file.

    spacezn_srfs: list[geomie3d.topobj.Face]
        The surfaces with the ifc wall guid attribute. 
    
    '''
    for win in ifc_wins:
        win_info = win.get_info()
        win_guid = win_info['GlobalId']
        # find the center point of the window
        verts3d, face_idx3d = ifc_utils.ifcopenshell_utils.get_ifc_facegeom(win)
        bbox = geomie3d.calculate.bbox_frm_xyzs(verts3d)
        center_xyz = geomie3d.calculate.bboxes_centre([bbox])[0]
        center_vert = geomie3d.create.vertex(center_xyz)
        # find the closest surface to the center pont of this window
        closest_srf, closest_ptxyz = ifc_utils.ifcopenshell_utils.find_srf_closest2this_pt(center_vert, spacezn_srfs, intx_pt=True)
        clse_attr = closest_srf.attributes
        if 'wins' in clse_attr.keys():
            clse_attr['wins'].append(win_guid)
        else:
            clse_attr['wins'] = [win_guid]

def map_spzn_srfs2ifcwall(ifcmodel:ifcopenshell.file, wall_srf_ls: list[geomie3d.topobj.Face]) -> list[geomie3d.topobj.Face]:
    '''
    Find the wall that correspond to the surface from the spatial zone.

    Parameters
    ----------
    ifcmodel:ifcopenshell.file
        The file path of the json parametric model.

    wall_srf_ls: list[geomie3d.topobj.Face]
        list generated from extract_srfs_frm_envlp_dicts
    
    Returns
    --------
    list[geomie3d.topobj.Face]
        list of face with the 'id' attribute = guid of ifc wall
    '''
    up_vec = [0,0,1]
    ifc_spacezones = ifcmodel.by_type('IfcSpatialZone')
    spacezn_srfs = []
    for spacez in ifc_spacezones:
        space_info = spacez.get_info()
        if space_info['Representation'] != None:
            srfs = ifc_utils.ifcopenshell_utils.ifcopenshell_entity_geom2g3d(spacez)
            for srf in srfs:
                nrml = geomie3d.get.face_normal(srf)
                angle = geomie3d.calculate.angle_btw_2vectors(up_vec, nrml)
                if 180 > angle >= 90:
                    closest_wall_srf = ifc_utils.ifcopenshell_utils.find_srf_closest2this_srf(srf, wall_srf_ls)
                    ifcwall_guid = closest_wall_srf.attributes['id']
                    geomie3d.modify.update_topo_att(srf, {'id': ifcwall_guid})
                    # region: for viz
                    # cmp = geomie3d.create.composite(wall_srf_ls)
                    # edges = geomie3d.get.edges_frm_composite(cmp)
                    # geomie3d.viz.viz([{'topo_list': [closest_wall_srf], 'colour': 'red'},
                    #                 {'topo_list': edges, 'colour': 'white'},
                    #                 {'topo_list': [srf], 'colour': 'blue'}])
                    # geomie3d.viz.viz([{'topo_list': [closest_wall_srf], 'colour': 'red'}])
                    # endregion: for viz
            spacezn_srfs.extend(srfs)
    return spacezn_srfs

def create_open_win_geom(ifc_obj: ifcopenshell.entity_instance, wall_srf: geomie3d.topobj.Face, height: float, width: float, wall_height: float, 
                         nrml: list[float], y_dir: list[float], extrusion: float, movement: float, ifcmodel:ifcopenshell.file, 
                         body: ifcopenshell.entity_instance, ray_mid: bool = False):
    '''
    Change the wwr of the wall.

    Parameters
    ----------
    ifc_obj: ifcopenshell.entity_instance
        ifcopening or ifcwindow.
    
    wall_srf: geomie3d.topobj.Face
        the srf of the hosting wall.
        
    height: float
        height of the new object

    width: float
        width of the new object.

    wall_height: float
        the height of the wall the object is hosted.

    nrml: list[float]
        nrml of the wall.
    
    y_dir: list[float]
        ydir of the wall.

    extrusion: float
        the thickness of the new geometry.

    movement: float
        move back before extrusion.

    ifcmodel: ifcopenshell.file
        The ifc model.

    body: ifcopenshell.file
        the IFCGEOMETRICREPRESENTATIONSUBCONTEXT of the ifcmodel

    '''
    buffered_wall_height = wall_height-0.5
    if height >= buffered_wall_height:
        height = buffered_wall_height
    ifc_geom = ifc_utils.ifcopenshell_utils.ifcopenshell_entity_geom2g3d(ifc_obj)
    cmp = geomie3d.create.composite(ifc_geom)
    bbox = geomie3d.calculate.bbox_frm_topo(cmp)
    mid_pt = geomie3d.calculate.bboxes_centre([bbox])[0]
    if ray_mid == True:
        rev_nrml = geomie3d.calculate.reverse_vectorxyz(nrml)
        mv_midpt = geomie3d.calculate.move_xyzs([mid_pt], [nrml], [1])[0]
        ray = geomie3d.utility.Ray(mv_midpt, rev_nrml)
        ray_res = geomie3d.calculate.rays_faces_intersection([ray], [wall_srf])
        hit_ray = ray_res[0][0]
        ray_attr = hit_ray.attributes
        mid_pt = ray_attr['rays_faces_intersection']['intersection'][0]

    face = geomie3d.create.polygon_face_frm_midpt(mid_pt, width, height)
    orig_xdir = geomie3d.get.face_normal(face)
    orig_ydir = [0,1,0]
    orig_cs = geomie3d.utility.CoordinateSystem(mid_pt, orig_xdir, orig_ydir)
    dest_cs = geomie3d.utility.CoordinateSystem(mid_pt, nrml, y_dir)
    face = geomie3d.modify.trsf_topo_based_on_cs(face, orig_cs, dest_cs)
    verts = geomie3d.get.bdry_vertices_frm_face(face)
    xyzs = np.array([v.point.xyz for v in verts])
    mesh = ifcopenshell_utils.mv_extrude_srf(xyzs, extrusion, movement)
    repr = ifcopenshell.api.run("geometry.add_mesh_representation", ifcmodel, context=body, 
                                vertices=[mesh['vertices'].tolist()], faces=[mesh['indices']])
    return repr #face, ifc_geom
    
def change_wwr(wwr: float, srf_with_wins: list[geomie3d.topobj.Face], ref_vec: list[float], ifcmodel: ifcopenshell.file, body: ifcopenshell.file):
    '''
    Change the wwr of the wall.

    Parameters
    ----------
    wwr: float
        the desired wwr.
    
    srf_with_wins: list[geomie3d.topobj.Face]
        the spatial zone surfaces from map_spzn_srfs2ifcwall and find_host_of_win. Need to have attributes 'id' and 'wins'

    ref_vec: list[float]
        list[shape(3)] specifying the direction of the surface to look for.

    ifcmodel: ifcopenshell.file
        The file path of the json parametric model.

    body: ifcopenshell.file
        the IFCGEOMETRICREPRESENTATIONSUBCONTEXT of the ifcmodel

    wall_srf_ls: list[geomie3d.topobj.Face]
        list generated from extract_srfs_frm_envlp_dicts
    
    Returns
    --------
    list[geomie3d.topobj.Face]
        list of face with the 'id' attribute = guid of ifc wall
    '''
    for srf in srf_with_wins:
        nrml = geomie3d.get.face_normal(srf)
        angle = geomie3d.calculate.angle_btw_2vectors(ref_vec, nrml)
        # for calc height and width of vertical obj
        y_dir = [0,0,1]
        z_dir = geomie3d.calculate.cross_product(nrml, y_dir)
        if angle <= 45: # it is facing the specified direction
            farea = geomie3d.calculate.face_area(srf)
            fverts = geomie3d.get.bdry_vertices_frm_face(srf)
            fxyzs = np.array([v.point.xyz for v in fverts])
            wall_height, wall_width = ifc_utils.ifcopenshell_utils.calc_vobj_height_width(fxyzs, z_dir, y_dir)
            # print(f"wallheight = {wall_height}, wallwidth={wall_width}")
            attr = srf.attributes
            win_guids = attr['wins']
            ifc_wins = []
            win_geoms = []
            win_midpts = []
            widths = []
            ttl_win_area = 0
            for win_guid in win_guids:
                ifc_win = ifcmodel.by_guid(win_guid)
                ifc_win_geom = ifc_utils.ifcopenshell_utils.ifcopenshell_entity_geom2g3d(ifc_win)
                win_cmp = geomie3d.create.composite(ifc_win_geom)
                win_verts = geomie3d.get.vertices_frm_composite(win_cmp)
                win_verts = geomie3d.modify.fuse_vertices(win_verts)
                win_xyzs = np.array([v.point.xyz for v in win_verts])
                win_midpt = geomie3d.calculate.xyzs_mean(win_xyzs)
                # calc the win width and height
                height, width = ifc_utils.ifcopenshell_utils.calc_vobj_height_width(win_xyzs, z_dir, y_dir)
                win_area = height*width
                ttl_win_area+=win_area
                # get all the dimensions and geometry info
                ifc_wins.append(ifc_win)
                win_geoms.append(ifc_win_geom)
                win_midpts.append(win_midpt)
                widths.append(width)
            
            # calc the change in window dimensions
            nwins = len(win_guids)
            req_win_area = farea*wwr
            req_win_area_each = req_win_area/nwins
            widths = np.array(widths)
            widths = widths + 0.5
            req_height = req_win_area_each/widths
            # curr_wwr = ttl_win_area/farea
            # print(f"req_height = {req_height}")
            # print(f"curr_wwr = {curr_wwr}, wwr = {wwr}")
            wall_guid = attr['id']
            ifc_wall = ifcmodel.by_guid(wall_guid)
            ifcopenings = ifc_utils.ifcopenshell_utils.find_objs_in_relvoidselement(ifcmodel, ifc_wall)
            opencnt = 0
            for ifcopen in ifcopenings:
                open_info = ifcopen.get_info()
                open_name = open_info['Name']
                open_name = open_name.lower()
                if 'window' in open_name:
                    open_height = req_height[opencnt]
                    open_width = widths[opencnt]
                    open_extrude = 0.8
                    open_mve = 0.4
                    open_repr = create_open_win_geom(ifcopen, srf, open_height, open_width, wall_height, nrml, y_dir, open_extrude, open_mve, ifcmodel, body)
                    # ifcopenshell.api.run("geometry.assign_representation", ifcmodel, product=ifcopen, representation=open_repr)
                    pdt_def = open_info['Representation']
                    pdt_def.Representations = [open_repr]
                    opencnt+=1

            win_faces = []
            win_geoms = []
            for wcnt,ifc_win in enumerate(ifc_wins):
                win_height = req_height[wcnt]
                win_width = widths[wcnt]
                win_extrude = 0.01
                win_mve = 0.005
                win_repr = create_open_win_geom(ifc_win, srf, win_height, win_width, wall_height, nrml, y_dir, win_extrude, win_mve, ifcmodel, body, 
                                                ray_mid=True)
                winfo = ifc_win.get_info()
                pdt_def = winfo['Representation']
                pdt_def.Representations = [win_repr]
                # win_faces.append(win_face)
                # win_geoms.extend(ifcgeoms)
            
            # geomie3d.viz.viz([{'topo_list': win_faces, 'colour': 'blue'},
            #                   {'topo_list': win_geoms, 'colour': 'red'}])

def exe_pmtrc_wwr_constr(pmtrc_path: str, ifc_path: str, res_dir: str):
    '''
    Execute a parameteric model and generate a variant.

    Parameters
    ----------
    pmtrc_path: str
        The file path of the json parametric model.

    ifc_path : str
        The file path of ifc.

    res_dir : str
        The path of the directory.
    
    '''
    with open(pmtrc_path) as pmtrc_file:
        pmtrc_mod = json.load(pmtrc_file)
    
    # validate the file and make sure it is compliant
    json_data_dir = settings.JSON_DATA_DIR
    pmtrc_mod_schema_path = Path(json_data_dir).joinpath('pmtrc_mod_schema.json')
    with open(pmtrc_mod_schema_path) as schema_file:
        pmtrc_schema = json.load(schema_file)

    if pmtrc_mod['exe_script'] != 'exe_wwr_constr':
        print('This is not the right parametric model json for this execution script')
        return False

    try:
        jsonschema.validate(instance=pmtrc_mod, schema=pmtrc_schema)
    except jsonschema.ValidationError as e:
        print(e.schema.get("error_msg", e.message))
        return False 
    
    pmtr_metas = pmtrc_mod['parameters']
    nmlz_pmtrs = pmtrc_mod['parameter_normalized_values']
    actl_pmtr_val_ls = map_nrmlz_vals(pmtr_metas, nmlz_pmtrs)

    # generate ifc variants
    ifcmodel = ifcopenshell.open(ifc_path)
    ifc_bldgs = ifcmodel.by_type('IfcBuilding')
    nbldgs = len(ifc_bldgs)
    if nbldgs == 1:
        ifc_filename = Path(ifc_path).stem
        res_dir = Path(res_dir)
        if not res_dir.exists():
            res_dir.mkdir(parents=True)

        pmtr_metakeys = list(pmtr_metas.keys())
        for acnt,pmtr_vals in enumerate(actl_pmtr_val_ls):
            ifcmodel, ifc_wall_ls, ifc_roof_ls, ifc_slab_ls, ifc_win_ls, ifc_gls_door_ls = open_ifc_file(ifc_path)
            # get the body context 
            bodies = ifcmodel.by_type('IfcGeometricRepresentationSubContext')
            chosen_body = None
            for body in bodies:
                body_info = body.get_info()
                body_name = body_info['ContextIdentifier']
                if body_name == 'Body':    
                    chosen_body = body
            wall_dicts = ifc_utils.ifcopenshell_utils.get_ifc_envlp_info(ifc_wall_ls)
            wall_srf_ls = extract_srfs_frm_envlp_dicts(wall_dicts)
            spacezn_srfs = map_spzn_srfs2ifcwall(ifcmodel, wall_srf_ls)
            find_host_of_win(ifc_win_ls, spacezn_srfs)
            # get all the surfs with windows
            srf_with_wins = []
            for srf in spacezn_srfs:
                if 'wins' in srf.attributes.keys():
                    srf_with_wins.append(srf)
            
            for cnt,pmtr_val in enumerate(pmtr_vals):
                pmtr_name = pmtr_metakeys[cnt]
                if pmtr_name == 'north_wwr':
                    vec = [0,1,0]
                    change_wwr(pmtr_val, srf_with_wins, vec, ifcmodel, chosen_body)
                elif pmtr_name == 'south_wwr':
                    vec = [0,-1,0]
                    change_wwr(pmtr_val, srf_with_wins, vec, ifcmodel, chosen_body)
                elif pmtr_name == 'east_wwr':
                    vec = [1,0,0]
                    change_wwr(pmtr_val, srf_with_wins, vec, ifcmodel, chosen_body)
                elif pmtr_name == 'west_wwr':
                    vec = [-1,0,0]
                    change_wwr(pmtr_val, srf_with_wins, vec, ifcmodel, chosen_body)

            for cnt,pmtr_val in enumerate(pmtr_vals):
                pmtr_name = pmtr_metakeys[cnt]
                if pmtr_name == 'wall_thermal_resistance':
                    for ifc_wall in ifc_wall_ls:
                        rval = ifcmodel.createIfcThermalResistanceMeasure(pmtr_val)
                        ifc_utils.ifcopenshell_utils.edit_pset_val(rval, ifcmodel, ifc_wall, 'Pset_OsmodThermalResistance')
                elif pmtr_name == 'roof_thermal_resistance':
                    for ifc_roof in ifc_roof_ls:
                        rval = ifcmodel.createIfcThermalResistanceMeasure(pmtr_val)
                        ifc_utils.ifcopenshell_utils.edit_pset_val(rval, ifcmodel, ifc_roof, 'Pset_OsmodThermalResistance')
                elif pmtr_name == 'floor_thermal_resistance':
                    for ifc_slab in ifc_slab_ls:
                        rval = ifcmodel.createIfcThermalResistanceMeasure(pmtr_val)
                        ifc_utils.ifcopenshell_utils.edit_pset_val(rval, ifcmodel, ifc_slab, 'Pset_OsmodThermalResistance')
                elif pmtr_name == 'glazing_uvalue':
                    for ifc_win in ifc_win_ls:
                        uval = ifcmodel.createIfcThermalTransmittanceMeasure(pmtr_val)
                        ifc_utils.ifcopenshell_utils.edit_pset_val(uval, ifcmodel, ifc_win, 'Pset_OsmodUfactor')
                    for ifc_gls_door in ifc_gls_door_ls:
                        uval = ifcmodel.createIfcThermalTransmittanceMeasure(pmtr_val)
                        ifc_utils.ifcopenshell_utils.edit_pset_val(uval, ifcmodel, ifc_gls_door, 'Pset_OsmodUfactor')
                
            res_path = str(res_dir.joinpath(f"{ifc_filename}_{acnt}.ifc"))
            # print(res_path)
            ifcmodel.write(res_path)

        pmtrc_mod['parameter_values'] = actl_pmtr_val_ls.tolist()
        pretty_json_data = json.dumps(pmtrc_mod, indent=4)
        with open(pmtrc_path, 'w') as f:
            f.write(pretty_json_data)

    else:
        raise Exception("Unexpected number of buildings", nbldgs, "only 1 building allowed")
    
    return True
    
def main():
    args = parse_args()
    pipe_input = args.process
    if pipe_input == False:
        pmtrc_path = args.json
    else:
        lines = list(sys.stdin)
        pmtrc_path = lines[0].strip()

    ifc_path = args.ifc
    res_dir = args.res

    ifc_path = str(Path(ifc_path).resolve())
    res_dir = str(Path(res_dir).resolve())
    is_executed = exe_pmtrc_wwr_constr(pmtrc_path, ifc_path, res_dir)
    # print(is_executed)
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