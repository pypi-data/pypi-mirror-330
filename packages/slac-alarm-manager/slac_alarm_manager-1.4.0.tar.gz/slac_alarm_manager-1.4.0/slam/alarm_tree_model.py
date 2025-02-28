from qtpy.QtCore import QAbstractItemModel, QModelIndex, QObject, Qt
from typing import List, Optional
from .alarm_item import AlarmItem, AlarmSeverity, get_item_name
import logging

logger = logging.getLogger(__name__)


class AlarmItemsTreeModel(QAbstractItemModel):
    """
    The AlarmItemsTreeModel is a tree-based model for organizing alarm data based on the QAbstractItemModel

    Parameters
    ----------
    parent : QObject, optional
        The parent of this model.
    """

    def __init__(self, annunciate: bool = False, enable_all_topic: bool = False, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.root_item = AlarmItem("")
        self.nodes = []
        self.path_to_index = {}  # Map from the alarm path to the index into the tree
        self.enable_all_topic = enable_all_topic
        # when we have multiple topics to display, make each topic-tree's root a child of a dummy root
        if self.enable_all_topic:
            self.nodes.insert(0, self.root_item)
        self.added_paths = dict()  # Mapping from PV name to all associated paths in the tree (will be just 1 for most)
        self.annunciate = annunciate

    def clear(self) -> None:
        """Clear out all the nodes in this tree and set the root to an empty item"""
        self.nodes.clear()
        self.added_paths.clear()
        self.path_to_index.clear()
        self.root_item = AlarmItem("")

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the column count"""
        return self.root_item.column_count()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the row count"""
        return self.getItem(parent).child_count()

    def data(self, index: QModelIndex, role=None):
        """Return the data for the associated role. Currently only supporting DisplayRole and TextColorRole."""
        if not index.isValid():
            return None

        alarm_item = self.getItem(index)
        if role == Qt.DisplayRole:
            if not alarm_item.is_enabled():
                return alarm_item.name + " * (disabled)"
            bypass_indicator = ""
            if not alarm_item.is_leaf() and alarm_item.bypass_count > 0:
                bypass_indicator = " *"
            elif alarm_item.alarm_severity != AlarmSeverity.OK:
                if alarm_item.is_leaf():
                    return (
                        alarm_item.name
                        + f"{bypass_indicator} - {alarm_item.alarm_severity.value}/{alarm_item.alarm_status}"
                    )
                else:
                    return f"{alarm_item.name}{bypass_indicator}"
            return alarm_item.name + bypass_indicator
        elif role == Qt.TextColorRole:
            return alarm_item.display_color(alarm_item.alarm_severity)

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        """Create an index for the input row and column based on the parent item."""
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = self.getItem(parent)

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)

        return QModelIndex()

    @staticmethod
    def get_all_leaf_nodes(alarm_item) -> List[AlarmItem]:
        """Returns all leaf nodes for the input item."""
        leaves = []
        items_to_add = []

        for i in alarm_item.child_items:
            items_to_add.append(i)
        while len(items_to_add) != 0:
            i = items_to_add.pop()
            if i.is_leaf():
                leaves.append(i)
            else:
                for j in i.child_items:
                    items_to_add.append(j)
        return leaves

    def parent(self, index) -> QModelIndex:
        """Create and return an index for the parent node given the index of the child."""
        if not index.isValid():
            return QModelIndex()

        child_item = self.getItem(index)
        parent_item = child_item.parent_item

        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def getItem(self, index: QModelIndex) -> AlarmItem:
        """Returns an AlarmItem given its index in the tree"""
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        else:
            return self.root_item

    def getItemIndex(self, path: str) -> int:
        """Returns the list index of the item based on its path, or -1 if no item exists at that path"""
        return self.path_to_index.get(path, -1)

    def update_item(
        self,
        name: str,
        path: str,
        severity: AlarmSeverity,
        status: str,
        time,
        value: str,
        pv_severity: AlarmSeverity,
        pv_status: str,
    ) -> None:
        """Updates the alarm item with the input name and path in this tree."""
        if name not in self.added_paths:
            logger.debug(f"Attempting update on a node that has not been added by config: {path}")
            return

        for alarm_path in self.added_paths[name]:
            item_to_update = self.nodes[self.getItemIndex(alarm_path)]
            item_to_update.alarm_severity = severity
            item_to_update.alarm_status = status
            item_to_update.alarm_time = time
            item_to_update.alarm_value = value
            item_to_update.pv_severity = pv_severity
            item_to_update.pv_status = pv_status
            if status == "Disabled":
                item_to_update.filtered = True
                parent_item = item_to_update.parent_item
                while parent_item is not None:
                    parent_item.bypass_count += 1
                    parent_item = parent_item.parent_item
            elif item_to_update.filtered:
                parent_item = item_to_update.parent_item
                while parent_item is not None:
                    parent_item.bypass_count -= 1
                    parent_item = parent_item.parent_item
                item_to_update.filtered = False

            # also ensure annunciate is enabled on application level (self.annunciate) and also for the current item.
            if self.annunciate and item_to_update.annunciating and item_to_update.is_in_active_alarm_state():
                # prints bell character, cross platform way to generate "beep" noise
                # (assuming the user has the bell-sound option enabled for their terminal),
                # could be replaced with call to audio library for more sound options
                print("\a")

        self.layoutChanged.emit()

    def update_model(self, item_path: str, values: dict) -> None:
        """
        Adds an alarm item to the tree if the given path does not yet exist, or updates the item at that path if it does

        Parameters
        ----------
        item_path : str
            The path of the alarm item to add or update
        values : dict
            All of the values associated with the alarm to add or update
        """
        item_name = get_item_name(item_path)
        alarm_item = AlarmItem(
            name=item_name,
            path=item_path,
            alarm_severity=AlarmSeverity.OK,
            description=values.get("description"),
            guidance=values.get("guidance"),
            displays=values.get("displays"),
            commands=values.get("commands"),
            enabled=values.get("enabled"),
            latching=values.get("latching"),
            annunciating=values.get("annunciating"),
            delay=values.get("delay"),
            alarm_filter=values.get("filter"),
        )

        if (
            item_name not in self.added_paths or item_path not in self.added_paths[item_name]
        ):  # This means this is a brand new item we are adding
            self.beginInsertRows(QModelIndex(), len(self.nodes), len(self.nodes))

            if ":\\/\\/" in item_path:
                path_as_list = item_path.split(":\\/\\/", 1)[0]
            else:
                path_as_list = item_path.split("=", 1)[0]
            path_as_list = path_as_list.split("/")
            self.nodes.append(alarm_item)
            self.path_to_index[item_path] = len(self.nodes) - 1

            if item_name not in self.added_paths:
                self.added_paths[item_name] = []
            self.added_paths[item_name].append(item_path)

            parent_path = "/".join(path_as_list[0:-1])

            # If the node has no parent, it must be the root-node of a topic's tree,
            # if we have multiple topic root-nodes then make them children of a dummy root-node
            if parent_path == "":
                logger.debug(f"Setting root of alarm tree to: {item_path}")
                if self.enable_all_topic:
                    alarm_item.assign_parent(self.root_item)
                    self.nodes[0].append_child(alarm_item)  # when 'All' topic enabled, nodes[0] is root of topic trees
                else:
                    self.root_item = alarm_item
                return

            parent_item_index = self.getItemIndex(parent_path)
            if parent_item_index == -1:
                self.update_model(parent_path, {})
                parent_item_index = self.getItemIndex(parent_path)
            alarm_item.assign_parent(self.nodes[parent_item_index])
            self.nodes[parent_item_index].append_child(alarm_item)
            # Sort nodes in alphabetical order
            self.nodes[parent_item_index].child_items.sort(key=lambda x: x.name)
            self.endInsertRows()

        else:  # Otherwise it is an update to an existing item
            for alarm_path in self.added_paths[item_name]:
                item_index = self.getItemIndex(alarm_path)
                self.nodes[item_index].description = values.get("description")
                self.nodes[item_index].guidance = values.get("guidance")
                self.nodes[item_index].displays = values.get("displays")
                self.nodes[item_index].commands = values.get("commands")
                self.nodes[item_index].delay = values.get("delay")
                self.nodes[item_index].alarm_filter = values.get("filter")
                if "enabled" in values:
                    self.nodes[item_index].enabled = values["enabled"]
                if "latching" in values:
                    self.nodes[item_index].latching = values["latching"]
                if "annunciating" in values:
                    self.nodes[item_index].annunciating = values["annunciating"]

    def remove_item(self, item_path: str) -> None:
        """Removes the alarm item at the input path from this tree"""
        item_index = self.getItemIndex(item_path)
        if item_index == -1:
            logger.debug(f"Attempting to remove item not in the tree: {item_path}")
            return

        item_name = get_item_name(item_path)
        self.beginRemoveRows(QModelIndex(), item_index, item_index)
        self.added_paths[item_name].remove(item_path)
        del self.path_to_index[item_path]
        del self.nodes[item_index]
        self.endRemoveRows()

        self.path_to_index = {node.path: idx for idx, node in enumerate(self.nodes)}

        if len(self.nodes) == 1:
            # All nodes should be removed at this point, as it is a complete replacement
            self.beginRemoveRows(QModelIndex(), 0, 0)
            self.clear()
            self.endRemoveRows()
