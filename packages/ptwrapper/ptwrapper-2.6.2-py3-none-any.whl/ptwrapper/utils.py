import json
import os
import shutil
import re


def copy_with_full_permissions(src, dest):
    """
    Copies a file from `src` to `dest` and ensures that the copied file
    has full permissions (read, write, and execute for all users).
    """
    # Copy the file
    shutil.copy(src, dest)

    # Set full permissions for the copied file
    os.chmod(dest, 0o777)  # Full read, write, and execute permissions for all users


def create_structure(temp_parent_path, metakernel_path='input_mk.tm', ptr_content='input_ptr.ptx', step=5, power=False,
                     sa_ck=False, mga_ck=False, quaternions=False):
    """
    Create the structure and contents for an OSVE session folder.

    Parameters
    ----------
    temp_parent_path : TemporaryDirectory[str]
        Path to the parent folder where the structure will be created.

    metakernel_path : str, optional
        Path to an existing and valid metakernel file (default is 'input_mk.tm').

    ptr_content : str, optional
        Content for the PTR file (default is 'input_ptr.ptx').

    step : int, optional
        Time step for the simulation configuration (default is 5).

    power : bool, optional
        If True, enables power-related configurations in the session file (default is False).

    sa_ck : bool, optional
        If True, enables Solar Array CK file output (default is False).

    mga_ck : bool, optional
        If True, enables MGA CK file output (default is False).

    quaternions : bool, optional
        If True, includes attitude quaternion data in the output (default is False).

    Returns
    -------
    str
        The absolute path to the generated session file.

    Note
    ----
    This function organizes files and creates necessary configurations for an OSVE session,
    including the kernel and input/output file structures. It also adjusts the session JSON
    based on the provided options.
    """
    crema_id = crema_identifier(metakernel_path)

    session_json_filepath = os.path.join(
        os.path.dirname(__file__), "config", "session_file.json"
    )

    agm_config_filepath = os.path.join(
        os.path.dirname(__file__), "config", "age", "cfg_agm_jui.xml"
    )

    fixed_definitions_filepath = os.path.join(
        os.path.dirname(__file__), "config", "age", "cfg_agm_jui_fixed_definitions.xml"
    )

    predefined_blocks_filepath = os.path.join(
        os.path.dirname(__file__), "config", "age", "cfg_agm_jui_predefined_block.xml"
    )

    event_definitions_filepath = os.path.join(
        os.path.dirname(__file__), "config", "age", "cfg_agm_jui_event_definitions.xml"
    )

    bit_rate_filepath = os.path.join(
        os.path.dirname(__file__), "config", "ise", "BRF_MAL_SGICD_2_1_300101_351005.brf"
    )

    eps_config_filepath = os.path.join(
        os.path.dirname(__file__), "config", "ise", "eps.cfg"
    )

    eps_events_filepath = os.path.join(
        os.path.dirname(__file__), "config", "ise", "events.juice.def"
    )

    sa_cells_count_filepath = os.path.join(
        os.path.dirname(__file__), "config", "ise", "phs_com_res_sa_cells_count.asc"
    )

    sa_cells_efficiency_filepath = os.path.join(
        os.path.dirname(__file__), "config", "ise", "RES_C50_SA_CELLS_EFFICIENCY_310101_351003.csv"
    )

    eps_units_filepath = os.path.join(
        os.path.dirname(__file__), "config", "ise", "units.def"
    )

    itl_downlink_filepath = os.path.join(
        os.path.dirname(__file__), "input", "itl", "downlink.itl"
    )

    itl_platform_filepath = os.path.join(
        os.path.dirname(__file__), "input", "itl", "platform.itl"
    )

    itl_tbd_filepath = os.path.join(
        os.path.dirname(__file__), "input", "itl", "TBD.itl"
    )

    itl_top_timelines_filepath = os.path.join(
        os.path.dirname(__file__), "input", "itl", "TOP_timelines.itl"
    )

    edf_spc_link_kab_filepath = os.path.join(
        os.path.dirname(__file__), "input", "edf", "EDF_JUI_SPC_LINK_KAB.edf"
    )

    edf_spc_link_xb_filepath = os.path.join(
        os.path.dirname(__file__), "input", "edf", "EDF_JUI_SPC_LINK_XB.edf"
    )

    edf_spacecraft_filepath = os.path.join(
        os.path.dirname(__file__), "input", "edf", "juice__spacecraft.edf"
    )

    edf_spacecraft_platform_filepath = os.path.join(
        os.path.dirname(__file__), "input", "edf", "juice__spacecraft_platform.edf"
    )

    edf_spacecraft_ssmm_filepath = os.path.join(
        os.path.dirname(__file__), "input", "edf", "juice__spacecraft_ssmm.edf"
    )

    edf_tbd_filepath = os.path.join(
        os.path.dirname(__file__), "input", "edf", "TBD.edf"
    )

    edf_top_experiments_filepath = os.path.join(
        os.path.dirname(__file__), "input", "edf", "TOP_experiments.edf"
    )

    evf_top_events_filepath = os.path.join(
        os.path.dirname(__file__), "input", f"TOP_{crema_id}_events.evf"
    )

    evf_downlink_filepath = os.path.join(
        os.path.dirname(__file__), "input", "downlink.evf"
    )

    evf_crema_filepath = os.path.join(
        os.path.dirname(__file__), "input", "evf", f"EVT_{crema_id.upper()}_GEOPIPELINE.EVF"
    )

    with open(session_json_filepath, "r") as session_json_file:
        session_json = json.load(session_json_file)

    # Paths for the execution
    config_dir = "config"
    input_dir = "input"
    kernel_dir = "kernels"
    output_dir = "outputs"

    age_config_path = os.path.join(temp_parent_path.name, config_dir, "age")
    ise_config_path = os.path.join(temp_parent_path.name, config_dir, "ise")
    os.makedirs(age_config_path, exist_ok=True)
    os.makedirs(ise_config_path, exist_ok=True)

    # age
    copy_with_full_permissions(agm_config_filepath, age_config_path)
    copy_with_full_permissions(fixed_definitions_filepath, age_config_path)
    copy_with_full_permissions(predefined_blocks_filepath, age_config_path)
    copy_with_full_permissions(event_definitions_filepath, age_config_path)
    # ise
    copy_with_full_permissions(bit_rate_filepath, ise_config_path)
    copy_with_full_permissions(eps_config_filepath, ise_config_path)
    copy_with_full_permissions(eps_events_filepath, ise_config_path)
    copy_with_full_permissions(sa_cells_count_filepath, ise_config_path)
    copy_with_full_permissions(sa_cells_efficiency_filepath, ise_config_path)
    copy_with_full_permissions(eps_units_filepath, ise_config_path)

    file_list = session_json["sessionConfiguration"]["attitudeSimulationConfiguration"][
        "kernelsList"
    ]["fileList"]

    file_list.append(
        {
            "fileRelPath": os.path.basename(metakernel_path),
            "description": f"{os.path.basename(metakernel_path)}",
        }
    )

    if not quaternions:
        del session_json['sessionConfiguration']['outputFiles']['txtAttitudeFilePath']
    if not sa_ck:
        del session_json['sessionConfiguration']['outputFiles']['ckSaFilePath']
        del session_json['sessionConfiguration']['outputFiles']['saDataFilePath']
    if not mga_ck:
        del session_json['sessionConfiguration']['outputFiles']['ckMgaFilePath']
        del session_json['sessionConfiguration']['outputFiles']['mgaDataFilePath']
    if not power:
        del session_json['sessionConfiguration']['outputFiles']['powerFilePath']
        del session_json['sessionConfiguration']['outputFiles']['powerConfig']

    session_json['sessionConfiguration']['simulationConfiguration']['timeStep'] = step
    session_json['sessionConfiguration']['outputFiles']['ckConfig']['ckTimeStep'] = step
    session_json['sessionConfiguration']['inputFiles']['eventTimelineFilePath'] = f"TOP_{crema_id}_events.evf"

    kernel_path = os.path.join(temp_parent_path.name, kernel_dir)
    os.makedirs(kernel_path, exist_ok=True)
    try:
        copy_with_full_permissions(metakernel_path, kernel_path)
    except (OSError, shutil.Error) as e:
        print(f'[ERROR]    {"<PTWR>":<27} An error occurred while copying the file: {e}')

    # Dump the ptr content
    ptr_folder_path = os.path.join(temp_parent_path.name, input_dir)
    os.makedirs(ptr_folder_path, exist_ok=True)

    ptr_path = os.path.join(ptr_folder_path, "PTR_PT_V1.ptx")
    with open(ptr_path, encoding="utf-8", mode="w") as ptr_file:
        ptr_file.write(ptr_content)

    # Create the dummy ITL and EDF inputs
    itl_folder_path = os.path.join(temp_parent_path.name, input_dir, "itl")
    os.makedirs(itl_folder_path, exist_ok=True)

    copy_with_full_permissions(itl_downlink_filepath, itl_folder_path)
    copy_with_full_permissions(itl_platform_filepath, itl_folder_path)
    copy_with_full_permissions(itl_tbd_filepath, itl_folder_path)
    copy_with_full_permissions(itl_top_timelines_filepath, itl_folder_path)

    edf_folder_path = os.path.join(temp_parent_path.name, input_dir, "edf")
    os.makedirs(edf_folder_path, exist_ok=True)

    copy_with_full_permissions(edf_spc_link_kab_filepath, edf_folder_path)
    copy_with_full_permissions(edf_spc_link_xb_filepath, edf_folder_path)
    copy_with_full_permissions(edf_spacecraft_filepath, edf_folder_path)
    copy_with_full_permissions(edf_spacecraft_platform_filepath, edf_folder_path)
    copy_with_full_permissions(edf_spacecraft_ssmm_filepath, edf_folder_path)
    copy_with_full_permissions(edf_tbd_filepath, edf_folder_path)
    copy_with_full_permissions(edf_top_experiments_filepath, edf_folder_path)

    evf_folder_path = os.path.join(temp_parent_path.name, input_dir, "evf")
    os.makedirs(evf_folder_path, exist_ok=True)

    copy_with_full_permissions(evf_top_events_filepath, ptr_folder_path)
    copy_with_full_permissions(evf_downlink_filepath, ptr_folder_path)
    copy_with_full_permissions(evf_crema_filepath, evf_folder_path)

    # Prepare the output folder
    output_path = os.path.join(temp_parent_path.name, output_dir)
    os.makedirs(output_path, exist_ok=True)

    # Finally dump the session file
    session_file_path = os.path.abspath(os.path.join(temp_parent_path.name, "session_file.json"))
    with open(session_file_path, "w") as session_json_file:
        json.dump(session_json, session_json_file, indent=2)

    return temp_parent_path, session_file_path


def get_base_path(rel_path, root_path):
    """
    Generate the absolute path of a relative path based on the provided root directory.

    Parameters
    ----------
    rel_path : str
        The relative path that needs to be converted into an absolute path.

    root_path : str
        The root directory from which the relative path should be resolved. If it's already
        an absolute path, `rel_path` is returned unchanged.

    Returns
    -------
    str
        The absolute path computed based on the relative path and root directory.

    """
    return rel_path if os.path.isabs(root_path) \
        else os.path.abspath(os.path.join(root_path, rel_path))


def get_kernels_to_load(session_file_path, root_scenario_path):
    kernels_to_load = []
    with open(session_file_path) as f:
        config = json.load(f)

        if "sessionConfiguration" in config:
            sessionConfiguration = config["sessionConfiguration"]

            if "attitudeSimulationConfiguration" in sessionConfiguration:
                agm_config = sessionConfiguration["attitudeSimulationConfiguration"]

        if agm_config is not None:
            if "kernelsList" in agm_config:
                if "baselineRelPath" in agm_config["kernelsList"]:
                    kernels_base_path = agm_config["kernelsList"]["baselineRelPath"]
                else:
                    raise "No baselineRelPath found at kernelsList."

                if "fileList" in agm_config["kernelsList"]:
                    for kernel in agm_config["kernelsList"]["fileList"]:
                        if "fileRelPath" in kernel:
                            kernels_to_load.append(os.path.join(kernels_base_path, kernel["fileRelPath"]))
                        else:
                            raise "No Kernel file relative path (fileRelPath) found."
                else:
                    raise "No fileList found at kernelsList."
            else:
                raise "No kernelsList found at attitudeSimulationConfiguration."

        else:
            raise "No AGM configuration found."

    return kernels_to_load


def crema_identifier(metakernel_path):
    """
    Extract the JUICE Crema identifier from a metakernel file.

    This function scans the metakernel file for the pattern 'juice_events_*_vXX.tf' and
    extracts the portion between 'juice_events_' and '_v'. If multiple identifiers are
    found, a warning is printed, and the first one is used.

    Parameters
    ----------
    metakernel_path : str
        The path to the metakernel file from which the identifier will be extracted.

    Returns
    -------
    str
        The JUICE Crema identifier extracted from the file. If no identifier is found,
        an empty string is returned.
    """
    # Define the pattern with a capturing group around '.*'
    pattern = r'juice_events_(.*)_v\d{2}\.tf'  # The part between juice_events_ and _v is captured

    # Open the file and read its content
    with open(metakernel_path, 'r') as file:
        content = file.read()

    # Find all occurrences of the pattern and capture the part that matches '.*'
    matches = re.findall(pattern, content)

    if len(matches) > 1:
        print(f'[WARNING] {"<PTWR>":<27} More than one JUICE Crema reference found, {matches[0]} will be used')
    elif len(matches) == 0:
        print(f'[WARNING] {"<PTWR>":<27} No JUICE Crema reference found: eclipses not taken into account.')
        return ''
    return matches[0]


def dict_to_html_table(data_dict):
    """
    Generate an HTML table representation of a dictionary containing PTR debugging logs.

    This function takes a nested dictionary of PTR logs and transforms it into an HTML table format.
    The generated HTML includes error messages styled according to their severity (e.g., 'error',
    'warning', 'info') and is formatted for clarity using a clean and modern design.

    Parameters
    ----------
    data_dict : dict
        A dictionary structured with keys, each containing blocks
        of observations. Each block has the following fields: 'observation', 'start_time',
        'end_time', and a list of 'error_messages'. Each error message includes 'time', 'severity',
        and 'text' attributes.

    Returns
    -------
    str
        A string representing the HTML content with a structured table for PTR debugging logs.
    """

    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>PTR Debugging Log</title>
<style>
    body {
        font-family: 'Roboto', sans-serif; /* Change font to Roboto */
        background-color: #f0f0f5;
        color: #444;
        margin: 10;
        padding: 10;
    }
    h1 {
        text-align: left; /* Left alignment */
        color: #2c3e50;
        font-size: 24px;
        margin-top: 20px;
    }
    h2, h3, h4 {
        color: #34495e;
        font-size: 18px;
        margin-top: 20px;
    }
    table {
        width: 90%;
        margin: 20px 0 20px 20px; /* Left-aligned margin */
        border-collapse: collapse;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        background-color: white;
        border-radius: 5px;
        overflow: hidden;
    }
    th {
        background-color: #2980b9;
        color: #fff;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: left; /* Ensure header text is also left-aligned */
    }
    td {
        border-bottom: 1px solid #ddd;
        text-align: left; /* Ensure text is aligned to the left */
    }
    tr:last-child td {
        border-bottom: none;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .error {
        color: #e74c3c;
    }
    .warning {
        color: #f39c12;
    }
    .info {
        color: #3498db;
    }
    table th, table td {
        border: none;
    }
    .table-header {
        background-color: #2980b9;
        color: white;
    }

    /* Adjustments for column widths */
    td:first-child {
        width: 175px; /* First column width */
        text-align: left !important; /* Force left alignment with !important */
    }
    td:nth-child(2) {
        width: 35px; /* Second column width */
        text-align: left !important; /* Force left alignment with !important */
    }
    td:nth-child(3) {
        width: 100px; /* Second column width */
        text-align: left !important; /* Force left alignment with !important */
    }
    td:nth-child(4) {
        width: auto; /* Third column takes the remaining space */
        text-align: left !important; /* Force left alignment with !important */
    }
</style>



</head>
    <body>
        <h1>PTR Debugging Log</h1>
    '''

    # Loop through SOC, then blocks
    for designer_key, designer_value in data_dict.items():
        html_content += f'<h2>{designer_key}</h2>'

        # Loop through blocks within SOC
        for block_key, block_value in designer_value.items():

            html_line = f'<h3>{block_key} - {block_value["observation"]} [{block_value["start_time"]} - {block_value["end_time"]}] </h3>'
            if html_line != f'<h3> -  [ - ] </h3>':
                html_content += html_line


            # Add error messages
            # html_content += '<tr><td>Error Messages</td><td><table>'
            html_content += '<table>'
            for error in block_value["error_messages"]:
                severity_class = error['severity'].lower()  # Use the severity for styling
                html_content += f'''
                <tr class="{severity_class}">
                    <td>{error["time"]}</td>
                    <td>{error["percentage"]}</td>
                    <td>{error["severity"]}</td>
                    <td>{error["text"]}</td>
                </tr>
                '''
            html_content += '</table></td></tr>'
            html_content += '</table><br>'

    # Close the HTML document
    html_content += '''
    </body>
    </html>
    '''

    return html_content

def merge_logs(ptr_log, osve_log_file):
    # This function is to add the Timeline handler error messages at the beginning.
    # Opening JSON file
    with open(osve_log_file, 'r') as file:
        osve_log = json.load(file)

    capturing = False
    att_timeline = []

    # Capture the Attitude Timeline Initialization blocks
    for entry in osve_log:
        # Check if we're about to start capturing:
        if (entry.get("module") == "AGM" or entry.get("module") == "AGE") and "Initializing Attitude Timeline" in entry.get("text"):
            # We found the line indicating the start
            capturing = True
            att_timeline.append(entry)
            continue

        # If we're already capturing, keep going as long as we stay in module "AGM"
        if capturing:
            # If the module changed to something other than "AGM", we stop capturing
            if entry.get("module") != "AGM":
                capturing = False
            else:
                att_timeline.append(entry)

    record_slew_block = False
    slew_log = []
    slew = {}
    for entry in att_timeline:
        if "TimelineHandler: Invalid slew due to attitude constraint breaks found" in entry.get("text"):
            if slew:
                slew_log.append(slew)
            record_slew_block = True
            slew = {"error_messages":["Problems occur computing SLEW"],
                    "block_name":[],
                    "block_instrument":[]}
        if record_slew_block and "Problems occur computing slew" in entry.get("text"):
            slew["time"] =  entry.get("time")
        if record_slew_block and "During slew checking" in entry.get("text"):
            slew["time"] =  entry.get("time")
        if record_slew_block and "would solve breaks" in entry.get("text"):
            slew["error_messages"].append(entry.get("text").split("TimelineHandler: ")[-1])
    # Append the last one.
    if slew:
        slew_log.append(slew)

    # Now we need to loop over all the blocks in the PTR LOG to find where the affected slew is and extract the
    # Observation name and the instrument.
    if slew_log:
        for slew in slew_log:
            for instrument, blocks in ptr_log.items():
                for block_name, block_log in blocks.items():
                    if (slew["time"] == block_log["start_time"]) and " SLEW " in block_name:
                        slew["block_name"].append(block_name)
                        slew["block_instrument"].append(instrument)

        # Now we insert the slew_log into the ptr_log
        ptr_log["SLEW ESTIMATOR"] = {}
        for slew in slew_log:
            error_messages = []
            for error_message in slew['error_messages']:
                if "would solve breaks" in error_message:
                    severity = "INFO"
                else:
                    severity = "ERROR"
                error_messages.append(
                      {'percentage':'-',
                       'severity':severity,
                       'time':slew['time'],
                       'text':error_message})

            slew_block = {'observation':"",
                          'start_time':slew['time'],
                          'end_time':slew['time'],
                          'error_messages':error_messages
                          }

            # Build up the block name
            try:
                blck_idx = 0
                block_name = ''
                for block in slew['block_name']:
                    block_name += f'{block} ({slew["block_instrument"][blck_idx]}) '
                    blck_idx += 1
            except:
                block_name = f"{' '.join(slew['block_name'])}"

            ptr_log["SLEW ESTIMATOR"][block_name] = slew_block

    return ptr_log


def extract_agm_entries(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    capturing = False
    extracted = []

    for entry in data:
        # Check if we're about to start capturing:
        if entry.get("module") == "AGM" and "Initializing Attitude Timeline" in entry.get("text", ""):
            # We found the line indicating the start
            capturing = True
            extracted.append(entry)
            continue

        # If we're already capturing, keep going as long as we stay in module "AGM"
        if capturing:
            # If the module changed to something other than "AGM", we stop capturing
            if entry.get("module") != "AGM":
                capturing = False
            else:
                extracted.append(entry)

    return extracted


def reorder_dict(d, first_key):
    """
    Returns a new dictionary that puts `first_key` first (if present),
    followed by the other keys in alphabetical order.
    """
    new_dict = {}

    # 1. If the special key is in `d`, add it first
    if first_key in d:
        new_dict[first_key] = d[first_key]

    # 2. Add the remaining keys in alphabetical order
    for key in sorted(d.keys()):
        if key != first_key:
            new_dict[key] = d[key]

    return new_dict