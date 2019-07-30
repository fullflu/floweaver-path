import numpy as np
from floweaver import SankeyDefinition, weave
from IPython.display import clear_output
from IPython.display import display

from .utils import get_node_order_bundle, get_palette, load_file


class TsSankey(object):
    def __init__(self, multiple_display_widget, path_widget, index_widget, column_widget, value_widget, column_level_widget, value_level_widget,
                 width, height, target_color, base_color):
        self.df = None
        self.flows = None
        self.column_values = None
        self.multiple_display_widget = multiple_display_widget
        self.path_widget = path_widget
        self.index_widget = index_widget
        self.column_widget = column_widget
        self.value_widget = value_widget
        self.column_level_widget = column_level_widget
        self.value_level_widget = value_level_widget
        self.sdd = None
        # display flag
        self.display_flag = False
        self.width = width
        self.height = height
        self.target_color = target_color
        self.base_color = base_color

    def on_path_update(self, change):
        # extract changed value
        file_path = change["new"]
        self.file_path = file_path

        # load dataframe
        self.df = load_file(file_path)
        self.index_widget.options = self.df.columns.tolist()
        self.index_widget.value = None
        # reset column level observation
        self.column_widget.unobserve(self.on_column_update, names="value")
        self.column_level_widget.unobserve(self.on_column_to_value_update, names="value")
        # set column list
        self.column_widget.options = self.df.columns.tolist()
        # reset default values
        self.column_widget.value = None
        self.column_level_widget.options = []
        self.column_level_widget.value = None

        # reset value level observation
        self.value_widget.unobserve(self.on_value_update, names="value")
        self.value_level_widget.unobserve(self.on_value_level_update, names="value")
        # set column list
        self.value_widget.options = self.df.columns.tolist()
        # reset default values
        self.value_widget.value = None
        self.value_level_widget.options = []
        self.value_level_widget.value = None

        # observe level observations
        self.column_widget.observe(self.on_column_update, names="value")
        self.value_widget.observe(self.on_value_update, names="value")
        self.column_level_widget.observe(self.on_column_to_value_update, names="value")
        self.value_level_widget.observe(self.on_value_level_update, names="value")

        # reset floweaver resources
        self.sdd = None
        self.flows = None
        self.palette = None

    def on_column_update(self, change):
        # extract changed value
        column_name = change["new"]
        # reset column level observation
        self.column_level_widget.unobserve(self.on_column_to_value_update, names="value")
        # reset value level observation
        self.value_level_widget.unobserve(self.on_value_level_update, names="value")
        # set column level options
        self.column_level_widget.options = np.sort(self.df[column_name].unique()).tolist()
        # reset column level value and value level variables
        self.column_level_widget.value = None
        self.value_level_widget.options = []
        self.value_level_widget.value = None
        # reset floweaver resources
        self.sdd = None
        # observe level observations
        self.column_level_widget.observe(self.on_column_to_value_update, names="value")
        self.value_level_widget.observe(self.on_value_level_update, names="value")

    def on_value_update(self, change):
        value_name = change["new"]
        if self.column_widget.value is not None and self.column_level_widget.value is not None:
            # reset value level observation
            self.value_level_widget.unobserve(self.on_value_level_update, names="value")
            # update　options
            options = np.sort(
                self.df[self.df[self.column_widget.value] == self.column_level_widget.value][value_name].unique()).tolist()
            if self.value_level_widget.value in options:
                self.sdd = self.get_sdd()
            else:
                self.value_level_widget.value = None
                self.sdd = None
            self.value_level_widget.options = options
            self.value_level_widget.observe(self.on_value_level_update, names="value")

    def on_column_to_value_update(self, change):
        column_level = change["new"]
        if self.column_widget.value is not None and self.value_widget.value is not None:
            # reset value level observation
            self.value_level_widget.unobserve(self.on_value_level_update, names="value")
            # update　options
            options = np.sort(
                self.df[self.df[self.column_widget.value] == column_level][self.value_widget.value].unique()).tolist()
            if self.value_level_widget.value in self.value_level_widget.options:
                self.sdd = self.get_sdd()
            else:
                self.sdd = None
            self.value_level_widget.options = options
            self.value_level_widget.value = None
            self.value_level_widget.observe(self.on_value_level_update, names="value")

    def on_value_level_update(self, change):
        value = change["new"]
        if self.df is not None:
            self.sdd = self.get_sdd()

    def on_clear_output(self, change):
        flag = change["new"]
        if self.sdd is not None:
            if flag == "Yes":
                display(self.multiple_display_widget)
                display(self.path_widget)
                display(self.index_widget)
                display(self.column_widget)
                display(self.value_widget)
                display(self.column_level_widget)
                display(self.value_level_widget)
                print("file: {}, index: {}, date: {} is {}, target: {} is {}".format(
                    self.path_widget.value,
                    self.index_widget.value,
                    self.column_widget.value,
                    self.column_level_widget.value,
                    self.value_widget.value,
                    self.value_level_widget.value
                ))
                display(weave(self.sdd, self.flows, palette=self.palette).to_widget(**self.size))
            else:
                clear_output(wait=False)
                display(self.multiple_display_widget)
                display(self.path_widget)
                display(self.index_widget)
                display(self.column_widget)
                display(self.value_widget)
                display(self.column_level_widget)
                display(self.value_level_widget)
                print("file: {}, index: {}, date: {} is {}, target: {} is {}".format(
                    self.path_widget.value,
                    self.index_widget.value,
                    self.column_widget.value,
                    self.column_level_widget.value,
                    self.value_widget.value,
                    self.value_level_widget.value
                ))
                display(weave(self.sdd, self.flows, palette=self.palette).to_widget(**self.size))
                clear_output(wait=True)

    def get_sdd(self):
        tmp_flows, nodes, bundles, orderings, df_piv = get_node_order_bundle(
            self.df,
            self.index_widget.value,
            self.column_widget.value,
            self.value_widget.value
        )
        flow_partition = nodes[self.column_level_widget.value].partition
        y_list = np.sort(df_piv[self.column_level_widget.value].unique()).tolist()
        palette = get_palette(y_list, self.value_level_widget.value, self.target_color, self.base_color)
        sdd = SankeyDefinition(nodes, bundles, orderings,
                               flow_partition=flow_partition)
        self.flows = tmp_flows
        self.palette = palette
        self.size = dict(width=self.width, height=self.height)
        if self.multiple_display_widget.value == "No" and self.display_flag is True:
            display(self.multiple_display_widget)
            display(self.path_widget)
            display(self.index_widget)
            display(self.column_widget)
            display(self.value_widget)
            display(self.column_level_widget)
            display(self.value_level_widget)
        print("file: {}, index: {}, date: {} is {}, target: {} is {}".format(
            self.path_widget.value,
            self.index_widget.value,
            self.column_widget.value,
            self.column_level_widget.value,
            self.value_widget.value,
            self.value_level_widget.value
        ))
        display(weave(sdd, self.flows, palette=self.palette).to_widget(**self.size))
        if self.multiple_display_widget.value == "No":
            clear_output(wait=True)
        self.display_flag = True
        return sdd
