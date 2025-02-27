import os
import time
import ipywidgets as widgets
from ipywidgets import Layout
from jupyter_ui_poll import ui_events
from IPython.display import display
from importlib.resources import files
from common.logging_config import logger
from common.console import console
from common.api.funding_envs_images import *
from common.config import PositronJob
from common.cli_args import args

RUN_NAME_HELPER_TEXT = '(Optional customized run name)'
COMING_SOON_MENU_ITEM = 'Customize...(coming soon)'
clicked = False

def notebook_cell_ui() -> PositronJob:
    """ 
    When the user runs this function, it will display a UI that allows the user to select the hardware to run the notebook on.
    
    This function will display a UI that allows the user to select the hardware to run the notebook on.
    
    """
    #
    # Left Column
    #
    left_column_title = widgets.HTML(
        value="<b>Run your remote function on Robbie!</b>",
    )

    # logo
    dog_img_resource = files('robbie').joinpath('img/dog.png')
    image = dog_img_resource.read_bytes()

    logo = widgets.Image(
        value=image,
        format='png',
        width=100,
        height=100,
    )

    style = {'description_width': 'initial'}

    #
    # Middle Column
    #
    middle_column_title = widgets.HTML(
        value="<b>Just choose your hardware!</b>",
    )
     # Environment Drop down
    _drop_dict = _load_envs_for_dropdown()
    if _drop_dict is None:
        console.print("[red] Error loading environments")
        return None
    _drop_dict.update({COMING_SOON_MENU_ITEM: None})
    
    hardware_dropdown = widgets.Dropdown(
        options = _drop_dict.items(),
        # value=_drop_dict[1],
        description='Hardware Options:',
        style=style,
        layout={'width': 'max-content'}
    )

    _or_ = widgets.HTML(
        value="           - or - ",
    )

    """ robbie does it for you
    auto_checkbox = widgets.Checkbox(
        value=False,
        description='Let Robbie choose the best resources for you',
        disabled=False,
        indent=False
    )
    """

    # goes back to simple mode
    take_me_back_button = widgets.Button(
        description='Take me back',
        disabled=False,
        # button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Go back to simple options',
        style = style
    )

    #
    # Right Column
    #
    right_column_title = widgets.HTML(
        value="<b>And get the ball rolling!</b>",
    )

    # optional name
    optional_name = widgets.Text(
        value=RUN_NAME_HELPER_TEXT,
        # description='Enter a name:',
        disabled=False,
        style=style
    )
    
    # "Run" button
    run_button = widgets.Button(
        description='Run',
        disabled=False,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Your notebook cell will run on Robbie',
        icon='play',
        style = style
    )

    coming_soon_text = widgets.HTML(
        value="Coming soon!",
    )

    # robbie does it for you
    tail_checkbox = widgets.Checkbox(
        value=False,
        description='Tail the remote machine stdout.',
        disabled=False,
        indent=False,
        style=style
    )

    # layout
    left_column = widgets.VBox([left_column_title, logo])
    middle_column = widgets.VBox([middle_column_title, hardware_dropdown, tail_checkbox],layout=Layout(margin = '0 20px 0 20px'))
    right_column = widgets.VBox([right_column_title, optional_name, run_button, ], layout=Layout(margin = '0 20px 0 20px'))
    ui = widgets.HBox([left_column, middle_column, right_column])

    out = widgets.Output()
    # display everything
    display(ui, out)

 
    def on_take_me_back_button_clicked(change):
        """ When we display the full list of option (all disabled) this button gets gets us back to the simple mode"""
        with out:
            # print("on_take_me_back_clicked() - change:", change)
            middle_column.children = [middle_column_title, hardware_dropdown, tail_checkbox]
    
    take_me_back_button.on_click(on_take_me_back_button_clicked)
    

    # this is the hardware dropdown to change to customization mode
    def on_hw_dropdown_changed(change):
        """ This is experimental now to show users what is coming"""
        with out:
            logger.debug(f"on_checkbox_clicked() - change:{change}")
            if change.get('type') == 'change' and change.get('name') == 'label' and change.get('new') == COMING_SOON_MENU_ITEM:
                logger.debug("detetected change")
                gpu_dropdown = widgets.Dropdown(
                    options=['Nvidia A10 (24GB)', 'Nvidia A100 (40GB)', 'Nvidia H100 (40GB)', 'CPU only'],
                    value='Nvidia A100 (40GB)',
                    description='GPU model:',
                    style=style,
                    layout={'width': 'max-content'},
                    disabled=True
                )
                cpu_slider=widgets.IntSlider(description='vCPU cores', min=1, max=64, step=1, value=4, style=style, disabled=True);
                memory_slider=widgets.IntSlider(description='System Memory (GB)', min=16, max=128, step=16, value=32, style=style, disabled=True);
                disksize_slider=widgets.IntSlider(description='Disk Size (GB)', min=16, max=128, step=16, value=32, style=style, disabled=True);
                middle_column.children = [middle_column_title, coming_soon_text, gpu_dropdown, cpu_slider, memory_slider, disksize_slider, take_me_back_button]
            else:
                logger.debug("did not detect change")

    hardware_dropdown.observe(on_hw_dropdown_changed)

    # this is the robbie does it for you checkbox
    """
    def on_checkbox_clicked(change):
        with out:
            # print("on_checkbox_clicked() - change:", change)
            if change.get('type') == 'change' and change.get('name') == 'value' and change.get('new') == True:
                hardware_dropdown.disabled = True
            elif change.get('type') == 'change' and change.get('name') == 'value' and change.get('new') == False:
                hardware_dropdown.disabled = False

    # register the event handler
    auto_checkbox.observe(on_checkbox_clicked)

    """
    
    def on_button_clicked(b):
        global clicked
        """ The user clicked the run button """
        print(f"on_button_clicked() - {clicked}")
        with out:
            logger.debug(f"Hardware dropdown value: {hardware_dropdown.value}")  
            if hardware_dropdown.value == None:
                console.print("[red] Please choose a hardware option, before running.")
                return None
            else:
                # print(f"Running on {hardware_dropdown.value}")
                clicked = True
            

    # register the event handler
    run_button.on_click(on_button_clicked)

    # wait for the user to click the run button
    try:
        with ui_events() as poll:
            while not clicked:
                poll(10) # poll queued UI events including button
                time.sleep(1) # wait for 1 second before checking again
    except KeyboardInterrupt:
        console.print("[red] User interrupted.")
        return None

    # do we want to stream?
    if tail_checkbox.value:
        args.stream_stdout = True

    # return a job config object
    job_config = PositronJob()
    if optional_name.value != RUN_NAME_HELPER_TEXT:
        job_config.name=optional_name.value
    job_config.funding_group_id = None
    job_config.environment_id = hardware_dropdown.value
    job_config.environment_selection = "user selected from dropdown"
    job_config.image = "auto-select" 

    return job_config

#
# Reads the environments from the PERSONAL funding group
#

def _load_envs_for_dropdown():
    """
    Load the environments for the dropdown list in the cell output
    """
    fs = list_funding_sources()
    if len(fs) == 0:
        return None
    
    personal_fs_id = None
    for key, val in fs.items():
        if (val[FS_TYPE] == FS_PERSONAL_TYPE):
            personal_fs_id = val.get(FS_ID)
    
    if personal_fs_id is None:
        return None
    envs = list_environments(personal_fs_id)
    if len(envs) == 0:
        return None
    
    dropdown_list = {}
    for _, val in envs.items():
        if not val.get(ENV_DELETED):
            dropdown_list.update({val.get(ENV_NAME) + " - " + val.get(ENV_DESCRIPTION) + f' ({val.get(ENV_TPH)} tokens/hr)' : val.get(ENV_ID)})
    return dropdown_list





    

