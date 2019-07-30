from ipywidgets import interact, Dropdown

from .lib.ts_sankey import TsSankey
from .lib.utils import extract_files


def visualizer(data_dir='./data', width=1070, height=500, target_color='yellowgreen', base_color='gray'):
    # define widgets
    style = {'description_width': 'initial'}
    multiple_display_widget = Dropdown(options=["Yes", "No"], value=None, description="multiple display?", style=style)
    path_widget = Dropdown(options=extract_files(data_dir), value=None, description="file path", style=style)
    i_widget = Dropdown(options=[], value=None, description="index column", style=style)
    x_widget = Dropdown(options=[], value=None, description="date column", style=style)
    y_widget = Dropdown(options=[], value=None, description="target variable", style=style)
    x_level_widget = Dropdown(options=[], value=None, description="target date", style=style)
    y_level_widget = Dropdown(options=[], value=None, description="target value", style=style)

    # define an instance
    ts = TsSankey(multiple_display_widget, path_widget, i_widget, x_widget, y_widget, x_level_widget, y_level_widget,
                  width, height, target_color, base_color)

    # update widgets
    multiple_display_widget.observe(ts.on_clear_output, names='value')
    path_widget.observe(ts.on_path_update, names='value')
    x_widget.observe(ts.on_column_update, names='value')
    y_widget.observe(ts.on_value_update, names='value')
    x_level_widget.observe(ts.on_column_to_value_update, names='value')
    y_level_widget.observe(ts.on_value_level_update, names='value')

    # temp function to for interaction
    def f(multiple_display_widget, data_path, i_widget, x_widget, y_widget, x_level_widget, y_level_widget):
        pass

    interact(f,
             multiple_display_widget=multiple_display_widget,
             data_path=path_widget,
             i_widget=i_widget,
             x_widget=x_widget,
             y_widget=y_widget,
             x_level_widget=x_level_widget,
             y_level_widget=y_level_widget)
