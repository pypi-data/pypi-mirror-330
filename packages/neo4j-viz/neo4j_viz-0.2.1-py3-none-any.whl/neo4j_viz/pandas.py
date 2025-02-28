from __future__ import annotations

from collections.abc import Iterable
from typing import Optional, Union

from pandas import DataFrame

from .node import Node
from .relationship import Relationship
from .visualization_graph import VisualizationGraph

DFS_TYPE = Union[DataFrame, Iterable[DataFrame]]


def from_dfs(
    node_dfs: DFS_TYPE, rel_dfs: DFS_TYPE, node_radius_min_max: Optional[tuple[float, float]] = (3, 60)
) -> VisualizationGraph:
    """
    Create a VisualizationGraph from two pandas DataFrames.

    Parameters
    ----------
    node_dfs: Union[DataFrame, Iterable[DataFrame]]
        DataFrame or iterable of DataFrames containing node data.
    rel_dfs: Union[DataFrame, Iterable[DataFrame]]
        DataFrame or iterable of DataFrames containing relationship data.
    node_radius_min_max : tuple[float, float], optional
        Minimum and maximum node radius.
        To avoid tiny or huge nodes in the visualization, the node sizes are scaled to fit in the given range.
    """
    if isinstance(node_dfs, DataFrame):
        node_dfs_iter: Iterable[DataFrame] = [node_dfs]
    else:
        node_dfs_iter = node_dfs

    has_size = True
    nodes = []
    for node_df in node_dfs_iter:
        has_size &= "size" in node_df.columns
        for _, row in node_df.iterrows():
            node = Node(**row.to_dict())
            nodes.append(node)

    if isinstance(rel_dfs, DataFrame):
        rel_dfs_iter: Iterable[DataFrame] = [rel_dfs]
    else:
        rel_dfs_iter = rel_dfs

    relationships = []
    for rel_df in rel_dfs_iter:
        for _, row in rel_df.iterrows():
            rel = Relationship(**row.to_dict())
            relationships.append(rel)

    VG = VisualizationGraph(nodes=nodes, relationships=relationships)

    if node_radius_min_max is not None and has_size:
        VG.resize_nodes(node_radius_min_max=node_radius_min_max)

    return VG
