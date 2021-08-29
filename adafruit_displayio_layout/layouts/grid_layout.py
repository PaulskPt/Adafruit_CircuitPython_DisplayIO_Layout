# SPDX-FileCopyrightText: 2020 Kevin Matocha, Tim Cocks
#
# SPDX-License-Identifier: MIT

"""
`grid_layout`
================================================================================

A layout that organizes cells into a grid table structure.


* Author(s): Kevin Matocha, Tim Cocks

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_Layout.git"


class GridLayout(displayio.Group):
    """
    A layout that organizes children into a grid table structure.

    :param int x: x location the layout should be placed. Pixel coordinates.
    :param int y: y location the layout should be placed. Pixel coordinates.
    :param int width: Width of the layout in pixels.
    :param int height: Height of the layout in pixels.
    :param tuple grid_size: Size in cells as two ints in a tuple e.g. (2, 2)
    :param int cell_padding: Extra padding space inside each cell. In pixels.
    :param bool divider_lines: Whether or not to draw lines between the cells. Defaults to False.
    :param tuple h_divider_line_rows: Row indexes to draw divider lines above.
        Row indexes are 0 based.
    :param tuple v_divider_line_cols: Column indexes to draw divider lines before.
        Column indexes are 0 based.

    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        x,
        y,
        width,
        height,
        grid_size,
        cell_padding,
        divider_lines=False,
        h_divider_line_rows=None,
        v_divider_line_cols=None,
    ):
        super().__init__(x=x, y=y)
        self.x = x
        self.y = y
        self._width = width
        self._height = height
        self.grid_size = grid_size
        self.cell_padding = cell_padding
        self._cell_content_list = []
        self._divider_lines_enabled = divider_lines
        self._divider_lines = []
        self.h_divider_line_rows = h_divider_line_rows
        self.v_divider_line_cols = v_divider_line_cols

    def _layout_cells(self):
        # pylint: disable=too-many-locals, too-many-branches, too-many-statements
        for cell in self._cell_content_list:
            if cell["content"] not in self:
                grid_size_x = self.grid_size[0]
                grid_size_y = self.grid_size[1]

                grid_position_x = cell["grid_position"][0]
                grid_position_y = cell["grid_position"][1]

                button_size_x = cell["cell_size"][0]
                button_size_y = cell["cell_size"][1]

                _measured_width = (
                    int(button_size_x * self._width / grid_size_x)
                    - 2 * self.cell_padding
                )

                _measured_height = (
                    int(button_size_y * self._height / grid_size_y)
                    - 2 * self.cell_padding
                )
                if hasattr(cell["content"], "resize"):
                    # if it has resize function
                    cell["content"].resize(
                        _measured_width,
                        _measured_height,
                    )
                else:
                    try:
                        # try width and height properties.
                        cell["content"].width = _measured_width
                        cell["content"].height = _measured_height
                    except AttributeError:
                        # This element does not allow setting width and height.
                        # No problem, we'll use whatever size it already is.
                        # _measured_width = cell["content"].width
                        # _measured_height = cell["content"].height

                        pass

                if not hasattr(cell["content"], "anchor_point"):

                    cell["content"].x = (
                        int(grid_position_x * self._width / grid_size_x)
                        + self.cell_padding
                    )
                    cell["content"].y = (
                        int(grid_position_y * self._height / grid_size_y)
                        + self.cell_padding
                    )
                else:
                    print(
                        "int({} * {} / {}) + {}".format(
                            grid_position_x, self._width, grid_size_x, self.cell_padding
                        )
                    )
                    print(
                        "int({} * {} / {}) + {}".format(
                            grid_position_y,
                            self._height,
                            grid_size_y,
                            self.cell_padding,
                        )
                    )

                    cell["content"].anchor_point = (0, 0)
                    cell["content"].anchored_position = (
                        int(grid_position_x * self._width / grid_size_x)
                        + self.cell_padding,
                        int(grid_position_y * self._height / grid_size_y)
                        + self.cell_padding,
                    )
                    print(cell["content"].anchored_position)
                    print("---")

                self.append(cell["content"])

                if self._divider_lines_enabled:
                    palette = displayio.Palette(2)
                    palette[0] = 0xFFFFFF
                    palette[1] = 0xFFFFFF

                    if not hasattr(cell["content"], "anchor_point"):
                        _bottom_line_loc_y = (
                            cell["content"].y + _measured_height + self.cell_padding
                        )
                        _bottom_line_loc_x = cell["content"].x - self.cell_padding

                        _top_line_loc_y = cell["content"].y - self.cell_padding
                        _top_line_loc_x = cell["content"].x - self.cell_padding

                        _right_line_loc_y = cell["content"].y - self.cell_padding
                        _right_line_loc_x = (
                            cell["content"].x + _measured_width + self.cell_padding
                        )
                    else:
                        _bottom_line_loc_y = (
                            cell["content"].anchored_position[1]
                            + _measured_height
                            + self.cell_padding
                        )
                        _bottom_line_loc_x = (
                            cell["content"].anchored_position[0] - self.cell_padding
                        )

                        _top_line_loc_y = (
                            cell["content"].anchored_position[1] - self.cell_padding
                        )
                        _top_line_loc_x = (
                            cell["content"].anchored_position[0] - self.cell_padding
                        )

                        _right_line_loc_y = (
                            cell["content"].anchored_position[1] - self.cell_padding
                        )
                        _right_line_loc_x = (
                            cell["content"].anchored_position[0]
                            + _measured_width
                            + self.cell_padding
                        )

                    _horizontal_divider_line = displayio.Shape(
                        _measured_width + (2 * self.cell_padding),
                        1,
                        mirror_x=False,
                        mirror_y=False,
                    )

                    _bottom_divider_tilegrid = displayio.TileGrid(
                        _horizontal_divider_line,
                        pixel_shader=palette,
                        y=_bottom_line_loc_y,
                        x=_bottom_line_loc_x,
                    )

                    _top_divider_tilegrid = displayio.TileGrid(
                        _horizontal_divider_line,
                        pixel_shader=palette,
                        y=_top_line_loc_y,
                        x=_top_line_loc_x,
                    )

                    _vertical_divider_line = displayio.Shape(
                        1,
                        _measured_height + (2 * self.cell_padding),
                        mirror_x=False,
                        mirror_y=False,
                    )

                    _left_divider_tilegrid = displayio.TileGrid(
                        _vertical_divider_line,
                        pixel_shader=palette,
                        y=_top_line_loc_y,
                        x=_top_line_loc_x,
                    )

                    _right_divider_tilegrid = displayio.TileGrid(
                        _vertical_divider_line,
                        pixel_shader=palette,
                        y=_right_line_loc_y,
                        x=_right_line_loc_x,
                    )

                    for line_obj in self._divider_lines:
                        self.remove(line_obj["tilegrid"])

                    print("pos_y: {} - size_y: {}".format(grid_position_y, grid_size_y))
                    print(grid_position_y == grid_size_y)
                    if grid_position_y == grid_size_y - 1 and (
                        self.h_divider_line_rows is None
                        or grid_position_y + 1 in self.h_divider_line_rows
                    ):
                        self._divider_lines.append(
                            {
                                "shape": _horizontal_divider_line,
                                "tilegrid": _bottom_divider_tilegrid,
                            }
                        )
                    if (
                        self.h_divider_line_rows is None
                        or grid_position_y in self.h_divider_line_rows
                    ):
                        self._divider_lines.append(
                            {
                                "shape": _horizontal_divider_line,
                                "tilegrid": _top_divider_tilegrid,
                            }
                        )
                    if (
                        self.v_divider_line_cols is None
                        or grid_position_x in self.v_divider_line_cols
                    ):
                        self._divider_lines.append(
                            {
                                "shape": _horizontal_divider_line,
                                "tilegrid": _left_divider_tilegrid,
                            }
                        )
                    if grid_position_x == grid_size_x - 1 and (
                        self.v_divider_line_cols is None
                        or grid_position_x + 1 in self.v_divider_line_cols
                    ):
                        self._divider_lines.append(
                            {
                                "shape": _vertical_divider_line,
                                "tilegrid": _right_divider_tilegrid,
                            }
                        )

                    for line_obj in self._divider_lines:
                        self.append(line_obj["tilegrid"])

    def add_content(self, cell_content, grid_position, cell_size):
        """Add a child to the grid.

        :param cell_content: the content to add to this cell e.g. label, button, etc...
         Group subclass that have width and height properties can be used.
        :param tuple grid_position: where in the grid it should go. Tuple with
         x,y coordinates in grid cells. e.g. (1,0)
        :param tuple cell_size: the size and shape that the new cell should
         occupy. Width and height in cells inside a tuple e.g. (1, 1)
        :return: None"""
        sub_view_obj = {
            "content": cell_content,
            "grid_position": grid_position,
            "cell_size": cell_size,
        }
        self._cell_content_list.append(sub_view_obj)
        self._layout_cells()
