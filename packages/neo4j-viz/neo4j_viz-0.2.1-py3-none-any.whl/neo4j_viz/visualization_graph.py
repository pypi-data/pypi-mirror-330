from __future__ import annotations

import warnings
from collections.abc import Iterable
from typing import Optional

from IPython.display import HTML
from pydantic_extra_types.color import Color, ColorType

from .colors import ColorsType, neo4j_colors
from .node import Node, NodeIdType
from .node_size import RealNumber, verify_radii
from .nvl import NVL
from .options import Layout, Renderer, RenderOptions
from .relationship import Relationship


class VisualizationGraph:
    """
    A graph to visualize.
    """

    #: "The nodes in the graph"
    nodes: list[Node]
    #: "The relationships in the graph"
    relationships: list[Relationship]

    def __init__(self, nodes: list[Node], relationships: list[Relationship]) -> None:
        """ "
        Create a new `VisualizationGraph`.

        Parameters
        ----------
        nodes:
            The nodes in the graph.
        relationships:
            The relationships in the graph.
        """
        self.nodes = nodes
        self.relationships = relationships

    def render(
        self,
        layout: Optional[Layout] = None,
        renderer: Renderer = Renderer.CANVAS,
        width: str = "100%",
        height: str = "600px",
        pan_position: Optional[tuple[float, float]] = None,
        initial_zoom: Optional[float] = None,
        min_zoom: float = 0.075,
        max_zoom: float = 10,
        allow_dynamic_min_zoom: bool = True,
        max_allowed_nodes: int = 10_000,
    ) -> HTML:
        """
        Render the graph.

        Parameters
        ----------
        layout:
            The `Layout` to use.
        renderer:
            The `Renderer` to use.
        width:
            The width of the rendered graph.
        height:
            The height of the rendered graph.
        pan_position:
            The initial pan position.
        initial_zoom:
            The initial zoom level.
        min_zoom:
            The minimum zoom level.
        max_zoom:
            The maximum zoom level.
        allow_dynamic_min_zoom:
            Whether to allow dynamic minimum zoom level.
        max_allowed_nodes:
            The maximum allowed number of nodes to render.
        """

        num_nodes = len(self.nodes)
        if num_nodes > max_allowed_nodes:
            raise ValueError(
                f"Too many nodes ({num_nodes}) to render. Maximum allowed nodes is set "
                f"to {max_allowed_nodes} for performance reasons. It can be increased by "
                "overriding `max_allowed_nodes`, but rendering could then take a long time"
            )

        Renderer.check(renderer, num_nodes)

        render_options = RenderOptions(
            layout=layout,
            renderer=renderer,
            pan_X=pan_position[0] if pan_position is not None else None,
            pan_Y=pan_position[1] if pan_position is not None else None,
            initial_zoom=initial_zoom,
            min_zoom=min_zoom,
            max_zoom=max_zoom,
            allow_dynamic_min_zoom=allow_dynamic_min_zoom,
        )

        return NVL().render(
            self.nodes,
            self.relationships,
            render_options,
            width,
            height,
        )

    def toggle_nodes_pinned(self, pinned: dict[NodeIdType, bool]) -> None:
        """
        Toggle whether nodes should be pinned or not.

        Parameters
        ----------
        pinned:
            A dictionary mapping from node ID to whether the node should be pinned or not.
        """
        for node in self.nodes:
            node_pinned = pinned.get(node.id)

            if node_pinned is None:
                continue

            node.pinned = node_pinned

    def resize_nodes(
        self,
        sizes: Optional[dict[NodeIdType, RealNumber]] = None,
        node_radius_min_max: Optional[tuple[RealNumber, RealNumber]] = (3, 60),
    ) -> None:
        """
        Resize the nodes in the graph.

        Parameters
        ----------
        sizes:
            A dictionary mapping from node ID to the new size of the node.
            If a node ID is not in the dictionary, the size of the node is not changed.
        node_radius_min_max:
            Minimum and maximum node size radius as a tuple. To avoid tiny or huge nodes in the visualization, the
            node sizes are scaled to fit in the given range. If None, the sizes are used as is.
        """
        if sizes is None and node_radius_min_max is None:
            raise ValueError("At least one of `sizes` and `node_radius_min_max` must be given")

        # Gather and verify all node size values we have to work with
        all_sizes = {}
        for node in self.nodes:
            size = None
            if sizes is not None:
                size = sizes.get(node.id)

                if size is not None:
                    if not isinstance(size, (int, float)):
                        raise ValueError(f"Size for node '{node.id}' must be a real number, but was {size}")

                    if size < 0:
                        raise ValueError(f"Size for node '{node.id}' must be non-negative, but was {size}")

                    all_sizes[node.id] = size

            if size is None:
                if node.size is not None:
                    all_sizes[node.id] = node.size

        if node_radius_min_max is not None:
            verify_radii(node_radius_min_max)

            unscaled_min_size = min(all_sizes.values())
            unscaled_max_size = max(all_sizes.values())
            unscaled_size_range = float(unscaled_max_size - unscaled_min_size)

            new_min_size, new_max_size = node_radius_min_max
            new_size_range = new_max_size - new_min_size

            if abs(unscaled_size_range) < 1e-6:
                default_node_size = new_min_size + new_size_range / 2.0
                final_sizes = {id: default_node_size for id in all_sizes}
            else:
                final_sizes = {
                    id: new_min_size + new_size_range * ((nz - unscaled_min_size) / unscaled_size_range)
                    for id, nz in all_sizes.items()
                }
        else:
            final_sizes = all_sizes

        for node in self.nodes:
            size = final_sizes.get(node.id)

            if size is None:
                continue

            node.size = size

    def color_nodes(self, property: str, colors: Optional[ColorsType] = None, override: bool = False) -> None:
        """
        Color the nodes in the graph based on a property.

        Parameters
        ----------
        property:
            The property of the nodes to use for coloring.
        colors:
            The colors to use for the nodes. If a dictionary is given, it should map from property to color.
            If an iterable is given, the colors are used in order.
            The default colors are the Neo4j graph colors.
        override:
            Whether to override existing colors of the nodes, if they have any.
        """
        if colors is None:
            colors = neo4j_colors

        if isinstance(colors, dict):
            self._color_nodes_dict(property, colors, override)
        else:
            self._color_nodes_iter(property, colors, override)

    def _color_nodes_dict(self, property: str, colors: dict[str, ColorType], override: bool) -> None:
        for node in self.nodes:
            color = colors.get(getattr(node, property))

            if color is None:
                continue

            if node.color is not None and not override:
                continue

            if not isinstance(color, Color):
                node.color = Color(color)
            else:
                node.color = color

    def _color_nodes_iter(self, property: str, colors: Iterable[ColorType], override: bool) -> None:
        exhausted_colors = False
        prop_to_color = {}
        colors_iter = iter(colors)
        for node in self.nodes:
            prop = getattr(node, property)

            if prop not in prop_to_color:
                next_color = next(colors_iter, None)
                if next_color is None:
                    exhausted_colors = True
                    colors_iter = iter(colors)
                    next_color = next(colors_iter)
                prop_to_color[prop] = next_color

            color = prop_to_color[prop]

            if node.color is not None and not override:
                continue

            if not isinstance(color, Color):
                node.color = Color(color)
            else:
                node.color = color

        if exhausted_colors:
            warnings.warn(
                f"Ran out of colors for property '{property}'. {len(prop_to_color)} colors were needed, but only "
                f"{len(set(prop_to_color.values()))} were given, so reused colors"
            )
