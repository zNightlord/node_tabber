import bpy
import json
import os
import time
import nodeitems_utils
import pprint
from .gn_items import geonodes_node_items
from . import nt_extras

from bpy.types import (
    Operator,
    PropertyGroup,
)
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    IntProperty,
    StringProperty,
)


def nt_debug(msg):
    addon = bpy.context.preferences.addons["node_tabber"]
    prefs = addon.preferences

    if prefs.nt_debug:
        print(str(msg))

    return


def take_fifth(elem):
    return int(elem[2])


def write_score(category, enum_items):
    addon = bpy.context.preferences.addons["node_tabber"]
    prefs = addon.preferences

    if category == "S":
        category = "shader.json"
    if category == "C":
        category = "compositor.json"
    if category == "T":
        category = "texture.json"
    if category == "G":
        category = "geometry.json"

    path = os.path.dirname(__file__) + "/" + category
    if not os.path.exists(path):
        content = {}
        content[enum_items] = {"tally": 1}

        with open(path, "w") as f:
            json.dump(content, f)

        print("Nodetabber created :" + path)
    else:
        with open(path, "r") as f:
            content = json.load(f)

        if enum_items in content:
            if content[enum_items]["tally"] < prefs.tally_weight:
                content[enum_items]["tally"] += 1
        else:
            content[enum_items] = {"tally": 1}

        with open(path, "w") as f:
            json.dump(content, f)

    return


def sub_search(
    enum_items, node_type_index, node_type, extras_ops, index_offset, content
):
    if node_type_index > -1:
        nt_debug(f"Adding ${node_type} nodes")
        for index2, subname in enumerate(extras_ops):
            tally = 0
            if subname[1] in content:
                tally = content[subname[1]]["tally"]
            enum_items.append(
                (
                    str(node_type_index) + subname[0] + " " + subname[1],
                    subname[1],
                    str(tally),
                    index_offset + 1 + index2,
                )
            )
        index_offset += index2 + 1
    return enum_items, index_offset


class NodeTabSetting(PropertyGroup):
    value: StringProperty(
        name="Value",
        description="Python expression to be evaluated " "as the initial node setting",
        default="",
    )


class NODE_OT_add_tabber_search(bpy.types.Operator):
    """Add a node to the active tree using node tabber"""

    bl_idname = "node.add_tabber_search"
    bl_label = "Search and Add Node"
    bl_options = {"REGISTER", "UNDO"}
    bl_property = "node_item"

    _enum_item_hack = []

    # Create an enum list from node items
    def node_enum_items(self, context):
        nt_debug("DEF: node_enum_items")
        enum_items = NODE_OT_add_tabber_search._enum_item_hack

        addon = bpy.context.preferences.addons["node_tabber"]
        prefs = addon.preferences

        enum_items.clear()
        category = context.space_data.tree_type[0]

        node_items = nodeitems_utils.node_items_iter(context)

        if category == "S":
            category = "shader.json"
        if category == "C":
            category = "compositor.json"
        if category == "T":
            category = "texture.json"
        if category == "G":
            node_items = geonodes_node_items(context)
            category = "geometry.json"

        path = os.path.dirname(__file__) + "/" + category
        if not os.path.exists(path):
            content = {}
        else:
            with open(path, "r") as f:
                content = json.load(f)

        index_offset = 0

        math_index = -1
        vector_math_index = -1
        mix_rgb_index = -1
        boolean_math_index = -1
        random_value_index = -1
        switch_index = -1
        capture_attr_index = -1
        sep_col_index = -1
        com_col_index = -1

        for index, item in enumerate(node_items):
            if isinstance(item, nodeitems_utils.NodeItem):
                short = ""
                tally = 0
                words = item.label.split()
                for word in words:
                    short += word[0]
                match = item.label + " (" + short + ")"
                if match in content:
                    tally = content[match]["tally"]

                enum_items.append(
                    (
                        str(index) + " 0 0",
                        item.label + " (" + short + ")",
                        str(tally),
                        index,
                    )
                )
                index_offset = index

                if item.label == "Math":
                    math_index = index
                if item.label == "Vector Math":
                    vector_math_index = index
                if item.label == "Mix":
                    mix_rgb_index = index
                if item.label == "Boolean Math":
                    boolean_math_index = index
                if item.label == "Random Value":
                    random_value_index = index
                if item.label == "Switch":
                    switch_index = index
                if item.label == "Capture Attribute":
                    capture_attr_index = index
                if item.label == "Separate Color":
                    sep_col_index = index
                if item.label == "Combine Color":
                    com_col_index = index

        # Add sub node searching if enabled
        if prefs.sub_search:
            for s in [
                (math_index, "math", nt_extras.math),
                (vector_math_index, "vector math", nt_extras.vector_math),
                (mix_rgb_index, "mix", nt_extras.color),
                (boolean_math_index, "boolean math", nt_extras.boolean_math),
                (random_value_index, "random value", nt_extras.random_value),
                (switch_index, "switch", nt_extras.switch),
                (capture_attr_index, "capture attribute",
                 nt_extras.capture_attr),
                (sep_col_index, "separate color", nt_extras.sep_col),
                (com_col_index, "combine color", nt_extras.com_col)
            ]:
                enum_items, index_offset = sub_search(
                    enum_items, s[0], s[1], s[2], index_offset, content
                )

        if prefs.tally:
            tmp = enum_items
            tmp = sorted(enum_items, key=take_fifth, reverse=True)
        else:
            tmp = enum_items
        return tmp
        # return enum_items

    # Look up the item based on index
    def find_node_item(self, context):
        nt_debug("DEF: find_node_item")
        tmp = int(self.node_item.split()[0])
        nt_debug("FIND_NODE_ITEM: Tmp : " + str(self.node_item.split()))

        node_item = tmp
        extra = self.node_item.split()[1:]
        nice_name = " ".join(self.node_item.split()[3:])
        node_items = nodeitems_utils.node_items_iter(context)

        if context.space_data.tree_type == "GeometryNodeTree":
            node_items = geonodes_node_items(context)

        for index, item in enumerate(node_items):
            if index == node_item:
                return [item, extra, nice_name]
        return None

    def execute(self, context):
        print("started")
        nt_debug("DEF: execute")
        startTime = time.perf_counter()
        addon = bpy.context.preferences.addons["node_tabber"]
        prefs = addon.preferences

        _find_node_item = self.find_node_item(context)
        item = _find_node_item[0]
        extra = _find_node_item[1]
        nice_name = _find_node_item[2]

        # Add to tally
        short = ""
        words = item.label.split()
        nt_debug("EXECUTE: Item label : " + str(item.label))
        for word in words:
            short += word[0]
        match = item.label + " (" + short + ")"

        type = self.node_item.split()[1]
        nt_debug("Checking type : " + str(type))

        if type == "0":
            nt_debug("Writing normal node tally")
            write_score(item.nodetype[0], match)
        else:
            nt_debug("Writing sub node tally")
            write_score(item.nodetype[0], nice_name)

        nt_debug("Hack")

        # no need to keep
        self._enum_item_hack.clear()

        if item:
            node_tree_type = None
            if "node_tree" in item.settings:
                node_tree_type = eval(item.settings["node_tree"])
            try:
                for setting in item.settings.items():
                    if setting[0] != "node_tree":
                        ops = self.settings.add()
                        ops.name = setting[0]
                        ops.value = setting[1]
            except AttributeError:
                print("An exception occurred")

            self.create_node(context, item.nodetype, node_tree_type)

            nt_debug(str(item.nodetype))
            nt_debug("extra 0: " + str(extra[0]))
            nt_debug("extra 1: " + str(extra[1]))

            space = context.space_data
            node_tree = space.node_tree
            node_active = context.active_node
            node_selected = context.selected_nodes

            if extra[0] in ["M", "VM", "BM"]:
                node_active.operation = extra[1]

            if extra[0] == "C":
                node_active.data_type = 'RGBA'
                node_active.blend_type = extra[1]

            if extra[0] == "RV":
                node_active.data_type = extra[1]

            if extra[0] == "SW":
                node_active.input_type = extra[1]

            if extra[0] == "CAP":
                node_active.data_type = extra[1]
                node_active.domain = extra[2].replace("SPLINE", "CURVE")

            if extra[0] == "SEP":
                node_active.mode = extra[1]

            if extra[0] == "COM":
                node_active.mode = extra[1]

            if not prefs.quick_place:
                bpy.ops.node.translate_attach_remove_on_cancel(
                    "INVOKE_DEFAULT")

            nt_debug("Time taken: " + str(time.perf_counter() - startTime))
            return {"FINISHED"}
        else:
            return {"CANCELLED"}

    def create_node(self, context, node_type=None, node_tree_type=None):
        nt_debug("DEF: create_node")
        space = context.space_data
        tree = space.edit_tree

        if node_type is None:
            node_type = self.type

        # select only the new node
        for n in tree.nodes:
            n.select = False

        node = tree.nodes.new(type=node_type)

        if node_tree_type != None:
            node.node_tree = node_tree_type

        node.select = True
        tree.nodes.active = node
        node.location = space.cursor_location
        return node

    def invoke(self, context, event):
        # self.store_mouse_cursor(context, event)
        # Delayed execution in the search popup
        context.window_manager.invoke_search_popup(self)
        return {"CANCELLED"}

    populate = node_enum_items

    node_item: EnumProperty(
        name="Node Type",
        description="Node type",
        items=populate,
    )


class NODE_OT_reset_tally(bpy.types.Operator):
    """Reset the tally count"""

    bl_idname = "node.reset_tally"
    bl_label = "Reset node tally count"

    def execute(self, context):
        categories = ["shader.json", "compositor.json",
                      "texture.json", "geometry.json"]
        reset = False
        for cat in categories:
            path = os.path.dirname(__file__) + "/" + cat
            if os.path.exists(path):
                reset = True
                # delete file
                os.remove(path)

            if reset:
                info = "Reset Tallies"
                self.report({"INFO"}, info)
            else:
                info = "No tallies to reset."
                self.report({"INFO"}, info)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(NodeTabSetting)
    bpy.utils.register_class(NODE_OT_add_tabber_search)
    bpy.utils.register_class(NODE_OT_reset_tally)


def unregister():
    bpy.utils.unregister_class(NodeTabSetting)
    bpy.utils.unregister_class(NODE_OT_add_tabber_search)
    bpy.utils.unregister_class(NODE_OT_reset_tally)
