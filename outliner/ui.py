# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Compact native Qt tree, keyboard navigation and model-backed drops."""
from .i18n import tr
import json
from functools import lru_cache
from pathlib import Path
from uuid import uuid4

from PySide6.QtCore import QMimeData, QSettings, QSize, Qt, Signal
from PySide6.QtGui import QActionGroup, QIcon, QPixmap
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QHBoxLayout,
                               QHeaderView, QLabel, QLineEdit, QMenu,
                               QToolButton, QTreeWidget, QVBoxLayout, QWidget)

ROLE = Qt.ItemDataRole.UserRole
ROOT_KEY = "@model"
SECTIONS_KEY = "@sections"
MIME = "application/x-ingetrazo-outliner"


@lru_cache(maxsize=32)
def icon(name):
    path = Path(__file__).parent / "icons" / f"{name}.svg"
    result = QIcon(str(path))
    raw = path.read_text(encoding="utf-8")
    import re
    selected = QPixmap()
    selected.loadFromData(re.sub(r'stroke="#[a-fA-F0-9]+"', 'stroke="#ffffff"', raw).encode(), "SVG")
    result.addPixmap(selected, QIcon.Mode.Selected)
    return result


class Tree(QTreeWidget):
    renameRequested = Signal()
    editRequested = Signal()
    leaveRequested = Signal()
    zoomRequested = Signal()
    moveRequested = Signal(object, object, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = uuid4().hex
        self.setColumnCount(3)
        self.setHeaderLabels([tr("Objeto"), tr("Etiqueta"), tr("Ver")])
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDropIndicatorShown(True)
        self.setUniformRowHeights(True)
        self.setIndentation(16)
        self.setIconSize(QSize(17, 17))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header = self.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(1, 82)
        header.resizeSection(2, 34)
        self.setMinimumWidth(230)
        self.setToolTip(tr("Clic: seleccionar · Doble clic: editar · F2: renombrar\n"
                        "Arrastre sobre un grupo para anidar; sobre Modelo para sacarlo."))

    def selected_keys(self):
        return [item.data(0, ROLE) for item in self.selectedItems()
                if not str(item.data(0, ROLE)).startswith("@")]

    def mimeTypes(self):
        return [MIME]

    def mimeData(self, items):
        mime = QMimeData()
        keys = [i.data(0, ROLE) for i in items
                if str(i.data(0, ROLE)).startswith("group:")]
        mime.setData(MIME, json.dumps({"token": self.token, "keys": keys}).encode())
        return mime

    def supportedDropActions(self):
        return Qt.DropAction.MoveAction

    def dropEvent(self, event):
        if event.source() is not self or not event.mimeData().hasFormat(MIME):
            event.ignore()
            return
        try:
            payload = json.loads(bytes(event.mimeData().data(MIME)))
        except (ValueError, TypeError):
            event.ignore()
            return
        if payload.get("token") != self.token or not payload.get("keys"):
            event.ignore()
            return
        item = self.itemAt(event.position().toPoint())
        where = self.dropIndicatorPosition()
        destination, before = None, None
        if item is not None:
            key = item.data(0, ROLE)
            if key == SECTIONS_KEY or str(key).startswith("section:"):
                event.ignore()
                return
            if key != ROOT_KEY:
                if where == QAbstractItemView.DropIndicatorPosition.OnItem:
                    destination = key
                else:
                    parent = item.parent()
                    destination = parent.data(0, ROLE) if parent else None
                    if destination == ROOT_KEY:
                        destination = None
                    before = (key, where == QAbstractItemView.DropIndicatorPosition.BelowItem)
        # Qt must never move only a visual row. The controller validates and
        # executes a native-history command, then refreshes the real tree.
        self.moveRequested.emit(payload["keys"], destination, before)
        event.setDropAction(Qt.DropAction.MoveAction)
        event.accept()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_F2:
            self.renameRequested.emit()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.editRequested.emit()
        elif key == Qt.Key.Key_Escape:
            self.leaveRequested.emit()
        elif key == Qt.Key.Key_F:
            self.zoomRequested.emit()
        else:
            super().keyPressEvent(event)
            return
        event.accept()


class Panel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("outliner_panel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        heading = QHBoxLayout()
        title = QLabel("JA Tree")
        font = title.font()
        font.setBold(True)
        title.setFont(font)
        heading.addWidget(title)
        heading.addStretch()
        self.locate = QToolButton()
        self.locate.setIcon(icon("locate"))
        self.locate.setToolTip(tr("Localizar la selección de la vista 3D en el árbol"))
        heading.addWidget(self.locate)
        self.options = QToolButton()
        self.options.setIcon(icon("options"))
        self.options.setToolTip(tr("Opciones del árbol"))
        self.options.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        menu = QMenu(self.options)
        self.expand = menu.addAction(tr("Expandir todo"))
        self.collapse = menu.addAction(tr("Contraer todo"))
        menu.addSeparator()
        self.sort = menu.addAction(tr("Ordenar por nombre (A–Z)"))
        self.sort.setCheckable(True)
        self.tags = menu.addAction(tr("Mostrar etiquetas"))
        self.tags.setCheckable(True)
        self.tags.setChecked(True)
        menu.addSeparator()
        self.reload = menu.addAction(tr("Actualizar"))
        menu.addSeparator()
        self.language_menu = menu.addMenu(tr("Idioma"))
        self.language_group = QActionGroup(self)
        self.language_group.setExclusive(True)
        self.language_actions = {}
        choice = QSettings().value("outliner/language", "auto", type=str)
        for code, label in (("auto", tr("Automático (IngeTrazo)")),
                            ("es", "Español"), ("en", "English"), ("fr", "Français")):
            action = self.language_menu.addAction(label)
            action.setCheckable(True)
            action.setChecked(code == choice)
            self.language_group.addAction(action)
            self.language_actions[code] = action
        self.options.setMenu(menu)
        heading.addWidget(self.options)
        layout.addLayout(heading)
        self.search = QLineEdit()
        self.search.setPlaceholderText(tr("Buscar nombre o etiqueta…"))
        self.search.setClearButtonEnabled(True)
        self.search.setAccessibleName(tr("Buscar objetos del modelo"))
        layout.addWidget(self.search)
        filters = QHBoxLayout()
        self.kind = QComboBox()
        for label, kind in ((tr("Todos los objetos"), "all"), (tr("Grupos"), "group"),
                            (tr("Componentes"), "component"), (tr("Planos de sección"), "section")):
            self.kind.addItem(label, kind)
        filters.addWidget(self.kind, 1)
        self.zoom = QToolButton()
        self.zoom.setIcon(icon("zoom"))
        self.zoom.setToolTip(tr("Encuadrar selección · F"))
        filters.addWidget(self.zoom)
        self.leave = QToolButton()
        self.leave.setIcon(icon("leave"))
        self.leave.setToolTip(tr("Salir de la edición del grupo · Esc"))
        filters.addWidget(self.leave)
        layout.addLayout(filters)
        self.context = QLabel(tr("Modelo"))
        self.context.setWordWrap(True)
        self.context.setTextFormat(Qt.TextFormat.PlainText)
        layout.addWidget(self.context)
        self.tree = Tree(self)
        layout.addWidget(self.tree, 1)
        self.empty = QLabel(tr("Cree grupos o componentes para organizar el modelo."))
        self.empty.setWordWrap(True)
        self.empty.setTextFormat(Qt.TextFormat.PlainText)
        layout.addWidget(self.empty)
        self.count = QLabel()
        self.count.setWordWrap(True)
        layout.addWidget(self.count)
        self.status = QLabel(tr("F2: nombre · Doble clic: editar · Arrastre: organizar"))
        self.status.setWordWrap(True)
        self.status.setTextFormat(Qt.TextFormat.PlainText)
        layout.addWidget(self.status)

    def retranslate(self):
        self.tree.setHeaderLabels([tr("Objeto"), tr("Etiqueta"), tr("Ver")])
        self.tree.setToolTip(tr("Clic: seleccionar · Doble clic: editar · F2: renombrar\n"
                                "Arrastre sobre un grupo para anidar; sobre Modelo para sacarlo."))
        self.search.setPlaceholderText(tr("Buscar nombre o etiqueta…"))
        self.search.setAccessibleName(tr("Buscar objetos del modelo"))
        for widget, source in ((self.locate, "Localizar la selección de la vista 3D en el árbol"),
                               (self.options, "Opciones del árbol"),
                               (self.zoom, "Encuadrar selección · F"),
                               (self.leave, "Salir de la edición del grupo · Esc")):
            widget.setToolTip(tr(source))
        for action, source in ((self.expand, "Expandir todo"), (self.collapse, "Contraer todo"),
                               (self.sort, "Ordenar por nombre (A–Z)"), (self.tags, "Mostrar etiquetas"),
                               (self.reload, "Actualizar")):
            action.setText(tr(source))
        for i, source in enumerate(("Todos los objetos", "Grupos", "Componentes", "Planos de sección")):
            self.kind.setItemText(i, tr(source))
        self.language_menu.setTitle(tr("Idioma"))
        self.language_actions["auto"].setText(tr("Automático (IngeTrazo)"))
        self.status.setText(tr("F2: nombre · Doble clic: editar · Arrastre: organizar"))
