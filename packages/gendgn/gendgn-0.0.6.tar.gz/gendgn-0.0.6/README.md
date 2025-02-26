# gendgn

## Getting Started
- This tutorial uses Ubuntu 24.04 OS
- install openstudio application 1.8.0 (https://github.com/openstudiocoalition/OpenStudioApplication/releases/tag/v1.8.0)

### FreeCAD example
1. Download FreeCAD (https://www.freecad.org/downloads.php)
2. Download the example files from this url https://github.com/chenkianwee/ifc2osmod_gendgn_egs/archive/refs/heads/main.zip
3. Unzip the folder and you will see this folder structure.
    ```
    ifc2osmod_gendgn_egs
        |----- epw
        |----- freecad
        |----- ifc
        |----- json
        |----- measure
    ```
3. Open the file in ifc2osmod_gendgn_egs/freecad/small_office.FCStd with FreeCAD. In Ubuntu, right click -> choose FreeCAD to open it
4. Once you open the file. You can export the model as IFC. Select SmallOffice on the Model Tab. Go to File -> Export. At the Files of type parameter choose Industry Foundation Classes (*.ifc). Export it to the ifc folder ifc2osmod_gendgn_egs/ifc/small_office.ifc
![image](https://github.com/user-attachments/assets/9ac68f15-eee5-443a-b442-862ad9ff65e5)

5. Reopen the IFC file in FreeCAD to check the export. File -> Open and choose the exported IFC file. You should be able to open the file as shown below.
![image](https://github.com/user-attachments/assets/a9de568c-fdcb-4a51-8407-58b434d2d8fc)

6. Now that we have successfully exported an IFC file we will use the file in gendgn module to generate variants of this design.

### gendgn 
1. Create a virtual environment called gendgn
    ```
    python3 -m venv venv/gendgn
    ```
2. Activate the virtual environment.
    ```
    source venv/gendgn/bin/activate
    ```
3. Install the gendgn python library.
    ```
    pip install gendgn
    ```
4. Go to the directory where you have downloaded the example files for this tutorial.
    ```
    cd ifc2osmod_gendgn_egs
    ```
5. Once installed we will parameterized the IFC that was generated in the previous section by running this command on the terminal
    ```
    pmtrz_wwr_constr -i ifc/small_office.ifc -r json/pmtrz_wwr_constr.json
    ```
6. Open the file ifc2osmod_gendgn_egs/json/pmtrz_wwr_constr.json. You will see the following. The file describes the parameterization. There are 8 parameters each with a range.
    ```
    {
    "exe_script": "exe_wwr_constr",
    "parameters": {
            "wall_thermal_resistance": {"range": [0.5, 3]},
            "roof_thermal_resistance": {"range": [3, 6]},
            "floor_thermal_resistance": {"range": [3, 6]},
            "glazing_uvalue": {"range": [0.5, 3]},
            "north_wwr": {"range": [0.1, 0.4]},
            "south_wwr": {"range": [0.1, 0.4]},
            "east_wwr": {"range": [0.1, 0.4]},
            "west_wwr": {"range": [0.1, 0.4]}
        }
    }
    ```
7. With the pmtrz_wwr_constr.json. We can use the next command to generate a sample of options. Specify the number variants to generate with the -n variable. In this tutorial we will only generate 5 variants. 
    ```
    sample_variants -n 5 -j json/pmtrz_wwr_constr.json -r json/sample_variants.json
    ```
8. Open the file ifc2osmod_gendgn_egs/json/sample_variants.json. You will see a new section "parameter_normalized_values". You will see 5 sets of 8 values for 5 design variants and each having 8 parameters. 
    ```
    "parameter_normalized_values": [
        [
            0.2428181727019519,
            0.22216051440303392,
            0.3179248195128799,
            0.1822885785823198,
            0.11343437238467262,
            0.4284061572769124,
            0.724093446021713,
            0.07539211757349876
        ],
        ...
        ...
        ...
    ```
9. With the sample_variants.json file. We can generate 5 variants with the following command.
    ```
    exe_wwr_constr -j json/sample_variants.json -i ifc/small_office.ifc -r ifc/small_office_variants
    ```
10. Go to ifc/small_office_variants folder. You will see that there will be 5 variants generated. You can open them with FreeCAD to see the variants.
    ```
    Note: API not available due to missing dependencies: geometry.add_representation - No module named 'bpy'
    Note: API not available due to missing dependencies: grid.create_axis_curve - No module named 'bpy'
    ```

### ifc2osmod
1. Once you have generated the IFC files. We can convert those files to Openstudio models and run the simulation with this batch simulation command:
    ```
    batch_eval -v ifc/small_office_variants/ -r res/small_office/ -e epw/miami/USA_FL_Miami.Intl.AP.722020_TMY3.epw -d epw/miami/USA_FL_Miami.Intl.AP.722020_TMY3.ddy -m json/measure_sel.json
    ```
2. Once done you can go to the res/small_office/small_office_0/csv/small_office_0_wrkflw_1_1_to_12_31_between_0_and_23_at1.csv and look at the simulation results.

## Development
1. Download the example files from this url https://github.com/chenkianwee/ifc2osmod_gendgn_egs/archive/refs/heads/main.zip

### cd to the right folder 
```
cd gendgn/src
```

### execute pmtrz_wwr_constr.py
```
python -m gendgn.pmtrz_wwr_constr -i path_to/ifc2osmod_gendgn_egs/ifc/small_office.ifc -r path_to/ifc2osmod_gendgn_egs/json/pmtrz_wwr_constr.json
```

### execute sample_variants.py
```
python -m gendgn.sample_variants -n 5 -j path_to/ifc2osmod_gendgn_egs/json/pmtrz_wwr_constr.json
```

### execute exe_wwr_constr.py
```
python -m gendgn.exe_wwr_constr -j path_to/ifc2osmod_gendgn_egs/json/pmtrz_wwr_constr.json -i path_to/ifc2osmod_gendgn_egs/ifc/small_office.ifc -r path_to/ifc2osmod_gendgn_egs/ifc/small_office_variants
```

### execute batch_eval.py
```
python -m gendgn.batch_eval -v path_to/ifc2osmod_gendgn_egs/ifc/small_office_variants -r path_to/ifc2osmod_gendgn_egs/res/batch_small_offices -e path_to/ifc2osmod_gendgn_egs/epw/miami/USA_FL_Miami.Intl.AP.722020_TMY3.epw -d path_to/ifc2osmod_gendgn_egs/epw/miami/USA_FL_Miami.Intl.AP.722020_TMY3.ddy -m path_to/ifc2osmod_gendgn_egs/json/measure_sel.json
```
