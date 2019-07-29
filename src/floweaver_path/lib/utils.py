import os
import pickle

import pandas as pd
import numpy as np
from floweaver import ProcessGroup, Waypoint, Partition, Bundle


base_extensions = ["csv", "xlsx", "pickle"]


def extract_files(data_dir, extensions=base_extensions):
    file_candidate = os.listdir(data_dir)
    file_list = [os.path.join(data_dir, file_path) for file_path in file_candidate
                 if sum([extension == file_path.split(".")[-1] for extension in extensions])]
    return file_list


def load_file(file_path, extensions=base_extensions):
    assert sum([extension == file_path.split(".")[-1] for extension in extensions]), "the extension of your file ({}) is not supported".format(file_path)
    extension = file_path.split(".")[-1]
    if "csv" == extension:
        data = pd.read_csv(file_path)
    elif "xlsx" == extension:
        data = pd.read_excel(file_path)
    elif "pickle" == extension:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
    return data


def get_palette(y_values, yl, target_color, base_color):
    palette = {value: base_color for value in y_values}
    palette[yl] = target_color
    return palette


def concat_in_out_df(df, i, col, val):
    n = df[i].unique().shape[0]
    df = df[[i, col, val]].copy()
    id = df[i].unique()
    add_df = pd.DataFrame()
    add_df[i] = id
    add_df[col] = "Start"
    add_df[val] = 'in'
    df = pd.concat([df, add_df])
    add_df = pd.DataFrame()
    add_df[i] = id
    add_df[col] = "End"
    add_df[val] = 'out'
    df = pd.concat([df, add_df]).reset_index(drop=True)
    return df


def get_node_order_bundle(df, i, x, y):
    df = df.copy()
    df = concat_in_out_df(df, i, x, y)
    df_piv = df.pivot_table(values=y, index=i, columns=x, aggfunc='sum').reset_index()
    x_values = ["Start"] + df_piv.columns.drop([i, "Start", "End"]).sort_values().tolist() + ["End"]
    assert len(x_values) > 3, "the cardinality of x need to be larger than 1"
    df_piv_count = df_piv.groupby(x_values)[i].count().reset_index().rename(columns={i: "value"})
    nodes = {}
    nodes[x_values[0]] = ProcessGroup(np.sort(df_piv_count[x_values[0]].unique()).tolist(), title=x_values[0])
    nodes[x_values[0]].partition = Partition.Simple("process", np.sort(df_piv_count[x_values[0]].unique()).tolist())
    nodes[x_values[-1]] = ProcessGroup(np.sort(df_piv_count[x_values[-1]].unique()).tolist(), title=x_values[-1])
    nodes[x_values[-1]].partition = Partition.Simple("process", np.sort(df_piv_count[x_values[-1]].unique()).tolist())
    for x_value in x_values[1:-1]:
        part = Partition.Simple(x_value, np.sort(df_piv_count[x_value].unique()).tolist())
        nodes[x_value] = Waypoint(part, title=x_value)

    ordering = [[x_value] for x_value in x_values]

    bundles = [Bundle(x_values[0], x_values[-1], waypoints=x_values[1:-1])]
    tmp_flows = df_piv_count.copy().rename(columns={x_values[0]: "source", x_values[-1]: "target"})
    return tmp_flows, nodes, bundles, ordering, df_piv
