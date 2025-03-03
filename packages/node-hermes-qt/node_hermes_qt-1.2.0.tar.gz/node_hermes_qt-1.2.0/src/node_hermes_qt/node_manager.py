import logging
from typing import List

from node_hermes_core.nodes.generic_node import GenericNode
from qt_custom_treewidget import ColumnNames, TreeItem, TreeviewViewer
from qtpy import QtCore, QtGui, QtWidgets

from .ui.toolbar import Ui_Form


class ToolbarWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class NodeInfoFields(ColumnNames):
    NAME = "Name"
    TYPE = "Type"
    STATUS = "Status"
    INFO = "Info"
    QUEUE = "Queue"


class NodeTreeItem(TreeItem):
    def __init__(self, node: GenericNode, root_item: QtWidgets.QTreeWidgetItem | None = None):
        super().__init__()
        self.treeitem = root_item if root_item else self
        self.set_node(node)

    def set_node(self, node: GenericNode):
        self.node = node
        self.treeitem.setExpanded(True)
        for name, node in self.node.managed_child_nodes.items():
            self.treeitem.addChild(NodeTreeItem(node))

    def get_text(self, column_type: ColumnNames):
        if column_type == NodeInfoFields.NAME:
            return self.node.name
        elif column_type == NodeInfoFields.STATUS:
            return self.node.state.name
        elif column_type == NodeInfoFields.TYPE:
            return self.node.__class__.__name__
        elif column_type == NodeInfoFields.INFO:
            return self.node.info_string
        elif column_type == NodeInfoFields.QUEUE:
            return self.node.queue_string
        return "Unknown"

    def get_color(self):
        if self.node.state == GenericNode.State.ACTIVE:
            return QtGui.QColor("lightgreen")
        elif self.node.state == GenericNode.State.INITIALIZING:
            return QtGui.QColor("yellow")
        elif self.node.state == GenericNode.State.ERROR:
            return QtGui.QColor("lightcoral")
        elif self.node.state == GenericNode.State.STOPPED:
            return QtGui.QColor("lightyellow")

        return None

    def expand_recursive(self):
        self.treeitem.setExpanded(True)
        for i in range(self.treeitem.childCount()):
            child = self.treeitem.child(i)
            if isinstance(child, NodeTreeItem):
                child.expand_recursive()


class NodeViewerWidget(QtWidgets.QWidget):
    root_item: NodeTreeItem | None = None

    def __init__(self):
        super().__init__()

        self.devices = {}
        self.treeitems = {}

        self.toolbar = ToolbarWidget()
        self.toolbar.start_btn.clicked.connect(self.start_selected_device)
        self.toolbar.stop_btn.clicked.connect(self.stop_selected_device)

        self.viewer_widget = TreeviewViewer()
        # self.viewer_widget.itemSelectionChanged.connect(self.on_selection_change)
        self.log = logging.getLogger(__name__)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.viewer_widget)

        self.setLayout(layout)
        self.viewer_widget.set_columns([t for t in NodeInfoFields])

        # Allow multiple selection
        self.viewer_widget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)

        # Use a qt timer to update the ui
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.viewer_widget.refresh_ui)
        self.timer.start(500)

    def set_root_node(self, root_node: GenericNode | None):
        # Get root tree item
        self.clear()

        if root_node is None:
            self.root_item = None
            return

        root_tree_item = self.viewer_widget.invisibleRootItem()  # type: ignore

        self.root_item = NodeTreeItem(root_node, root_tree_item)
        
        # Expand all clildren
        self.root_item.expand_recursive()   
        
    @property
    def selected_nodes(self) -> List[GenericNode]:
        selected_items = self.viewer_widget.get_selected_items()
        return [item.node for item in selected_items if isinstance(item, NodeTreeItem)]

    def start_selected_device(self):
        for node in self.selected_nodes:
            node.attempt_init()

    def stop_selected_device(self):
        for node in self.selected_nodes:
            node.attempt_deinit()

    def clear(self):
        self.viewer_widget.clear()

    def set_columns(self, collumns: List[ColumnNames]):
        self.viewer_widget.set_columns(collumns)
