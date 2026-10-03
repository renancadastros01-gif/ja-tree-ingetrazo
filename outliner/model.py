# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Read the native hierarchy and move placements without copying geometry."""
from .i18n import tr
from dataclasses import dataclass
import re
import unicodedata

from PySide6.QtGui import QMatrix4x4
from core.group import Group, iter_placements
from core.history import Command
from core.layers import layer_of


def folded(text):
    return "".join(c for c in unicodedata.normalize("NFD", str(text).casefold())
                   if not unicodedata.combining(c))


def natural_key(text):
    return tuple((1, int(part)) if part.isdigit() else (0, part)
                 for part in re.split(r"(\d+)", folded(text)))


def entity_key(entity):
    return ("group:" if isinstance(entity, Group) else "section:") + str(entity.uid)


@dataclass
class Node:
    entity: object
    parent: object
    ancestors: tuple
    world: QMatrix4x4
    kind: str
    visible: bool
    locked: bool

    @property
    def key(self):
        return entity_key(self.entity)

    @property
    def name(self):
        return self.entity.name or (tr("Plano de sección ") + str(self.entity.symbol)
                                    if self.kind == "section" else tr("Sin nombre"))

    @property
    def tag(self):
        return layer_of(self.entity) if self.kind != "section" else ""

    @property
    def parent_key(self):
        return entity_key(self.parent) if self.parent is not None else None


def index_scene(scene):
    """Preorder, including hidden objects; do not flatten component meshes."""
    result = {}
    editing_components = {level["group"] for level in scene._edit_stack
                          if level.get("share") is not None
                          and level["group"].component}
    stack = [(g, None, (), QMatrix4x4(), True, False)
             for g in reversed(scene.groups)]
    while stack:
        group, parent, ancestors, base, visible, locked = stack.pop()
        if group in ancestors:
            raise ValueError(tr("El modelo contiene un ciclo en su jerarquía."))
        world = base * group.xform if group.xform is not None else base
        layer = scene.layer(layer_of(group))
        visible = visible and not group.hidden and (layer is None or layer.visible)
        locked = locked or (layer is not None and layer.locked)
        kind = "component" if (group.is_component() or group in editing_components) else "group"
        node = Node(group, parent, ancestors, world, kind, bool(visible), bool(locked))
        if node.key in result:
            raise ValueError(tr("El modelo contiene identidades de objetos repetidas."))
        result[node.key] = node
        stack.extend((child, group, ancestors + (group,), world, visible, locked)
                     for child in reversed(group.children))
    for plane in scene.section_planes:
        node = Node(plane, None, (), QMatrix4x4(), "section",
                    scene.show_section_planes, False)
        result[node.key] = node
    return result


def matching_keys(nodes, query="", kind="all"):
    """Keep ancestors of matches so filtered rows retain their real context."""
    terms = folded(query).split()
    direct = set()
    for key, node in nodes.items():
        haystack = folded(f"{node.name} {node.tag} {getattr(node.entity, 'symbol', '')}")
        if (kind == "all" or kind == node.kind) and all(t in haystack for t in terms):
            direct.add(key)
    included = set(direct)
    for key in direct:
        included.update(entity_key(g) for g in nodes[key].ancestors)
    return included, direct


def topmost(nodes, keys):
    selected = {key for key in keys if key in nodes and nodes[key].kind != "section"}
    return [n for key, n in nodes.items() if key in selected
            and not any(entity_key(g) in selected for g in n.ancestors)]


def _require_root(scene):
    if scene.edit_group is not None:
        raise ValueError(tr("Salga de la edición del grupo antes de organizar el modelo."))


def valid_name(value):
    value = str(value).strip()
    if not value or len(value) > 256:
        raise ValueError(tr("Escriba un nombre de 1 a 256 caracteres."))
    return value


class Rename(Command):
    def __init__(self, entity, name):
        self.entity, self.name = entity, valid_name(name)
        self.before = entity.name
        self.changed = self.name != self.before

    def do(self, scene):
        self.entity.name = self.name
        scene.version += 1

    def undo(self, scene):
        self.entity.name = self.before
        scene.version += 1


class Reparent(Command):
    """Reparent/reorder groups with M_local = inverse(M_parent) * M_world.

    All validation and list/matrix snapshots precede the first mutation.
    Undo restores the SAME objects, meshes, sharing and list order.
    """
    def __init__(self, scene, keys, destination=None, position=None):
        _require_root(scene)
        nodes = index_scene(scene)
        self.representations_before = self._representations(nodes)
        self.representations_after = None
        self.moving = topmost(nodes, keys)
        if not self.moving:
            raise ValueError(tr("Seleccione grupos o componentes para mover."))
        self.parent = None
        dest_world = QMatrix4x4()
        dest_ancestors = ()
        if destination is not None:
            target = nodes.get(destination)
            if target is None or target.kind == "section":
                raise ValueError(tr("El destino debe ser un grupo o el modelo."))
            self.parent, dest_world = target.entity, target.world
            dest_ancestors = target.ancestors + (target.entity,)
            if target.locked:
                raise ValueError(tr("La etiqueta del destino está bloqueada."))
        groups = {node.entity for node in self.moving}
        if any(g in groups for g in dest_ancestors):
            raise ValueError(tr("Un objeto no puede contenerse a sí mismo ni a un antecesor."))
        if any(node.locked for node in self.moving):
            raise ValueError(tr("La selección contiene una etiqueta bloqueada."))
        affected = set(dest_ancestors)
        for node in self.moving:
            affected.update(node.ancestors + (node.entity,))
        if any(g.exploded or g.explode_offset is not None for g in affected):
            raise ValueError(tr("Reensamble la vista explotada antes de reorganizar estos objetos."))
        inverse, ok = dest_world.inverted()
        if not ok:
            raise ValueError(tr("El destino tiene una escala nula; no se puede invertir su matriz."))
        self.owner = self.parent.children if self.parent is not None else scene.groups
        self.lists = []
        for owner in [self.owner] + [n.parent.children if n.parent is not None
                                    else scene.groups for n in self.moving]:
            if not any(owner is previous for previous, _ in self.lists):
                self.lists.append((owner, list(owner)))
        self.after = []
        for node in self.moving:
            if node.parent is self.parent:
                self.after.append((node.entity, node.entity.xform, node.entity.component))
            else:
                self.after.append((node.entity, inverse * node.world,
                                   node.entity.component if node.entity.xform is not None else False))
        pos = len(self.owner) if position is None else max(0, min(position, len(self.owner)))
        self.position = pos - sum(1 for i, g in enumerate(self.owner) if i < pos and g in groups)
        self.result = [(owner, [g for g in contents if g not in groups])
                       for owner, contents in self.lists]
        new_owner = next(contents for owner, contents in self.result if owner is self.owner)
        new_owner[self.position:self.position] = [n.entity for n in self.moving]
        self.changed = any(old != new for (_, old), (_, new) in zip(self.lists, self.result))

    @property
    def _history_mesh(self):
        # Structural edits operate on ownership lists, independent of the
        # mesh active when Undo is pressed. Opt out of History's mesh swap
        # so closing an edit context cannot leave scene.mesh dangling.
        return None

    @_history_mesh.setter
    def _history_mesh(self, value):
        pass

    @staticmethod
    def _representations(nodes):
        # Entering a container bakes its matrix into the children WITHOUT
        # a history step. Keep these lightweight references/matrices so an
        # Undo after navigating inside it restores the original frames.
        return [(n.entity, n.entity.mesh,
                 QMatrix4x4(n.entity.xform) if n.entity.xform is not None else None,
                 QMatrix4x4(n.entity.axes) if n.entity.axes is not None else None,
                 n.entity.component) for n in nodes.values() if n.kind != "section"]

    @staticmethod
    def _restore_representations(values):
        for group, mesh, matrix, axes, component in values:
            group.mesh = mesh
            group.xform = QMatrix4x4(matrix) if matrix is not None else None
            group.axes = QMatrix4x4(axes) if axes is not None else None
            group.component = component

    def do(self, scene):
        scene.end_group_edit()
        if self.representations_after is not None:
            self._restore_representations(self.representations_after)
        for owner, contents in self.result:
            owner[:] = contents
        if self.representations_after is None:
            for group, matrix, component in self.after:
                group.xform, group.component = matrix, component
            if self.parent is not None and self.parent.xform is None:
                self.parent.xform = QMatrix4x4()
                self.parent.component = False
            self.representations_after = self._representations(index_scene(scene))
        scene.selection.clear()
        scene.version += 1

    def undo(self, scene):
        scene.end_group_edit()
        for owner, contents in self.lists:
            owner[:] = contents
        self._restore_representations(self.representations_before)
        scene.selection.clear()
        scene.version += 1


def bounds_of(nodes, keys):
    """World bounds of nested placements, without changing native selection."""
    import numpy as np
    from PySide6.QtGui import QVector3D
    from core.group import np_affine
    low, high = None, None
    for key in keys:
        node = nodes.get(key)
        if node is None or node.kind == "section":
            continue
        base = nodes[node.parent_key].world if node.parent is not None else None
        for group, matrix in iter_placements(node.entity, base):
            if not group.mesh.vertices:
                continue
            points = np.array([v.position.toTuple() for v in group.mesh.vertices], dtype=float)
            if matrix is not None:
                rotation, translation = np_affine(matrix)
                points = points @ rotation.T + translation
            a, b = points.min(axis=0), points.max(axis=0)
            low = a if low is None else np.minimum(low, a)
            high = b if high is None else np.maximum(high, b)
    return (None, None) if low is None else (QVector3D(*low), QVector3D(*high))
