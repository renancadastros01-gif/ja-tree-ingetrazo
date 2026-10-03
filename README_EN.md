# JA Tree for IngeTrazo

**0.1.0 · Julio Angulo · IngeTrazo 0.5.7 / Extension API 2**

A side panel for exploring and organizing native groups, components and section
planes. Includes search, synchronized selection, visibility, drag-and-drop
organization, tags, zoom to selection and native undo/redo. Changes are saved
in the model's IGZ file.

## Install

1. Extract **JA_Tree_v0.1.0.zip**.
2. In IngeTrazo, choose **Extensions → Open plugins folder**.
3. Copy the complete **outliner** folder there, including icons and locales.
   This internal identifier preserves the previous installation's preferences.
4. Restart IngeTrazo and choose **Extensions → JA Tree…**.

The archive includes **Ejemplo_JA_Tree.igz**, a sample model. No additional
dependencies are required. To update, replace the previous outliner folder.

## Language and controls

Open the panel's options button and choose **Language → English / Français /
Español**. Changes apply immediately and persist across restarts. **Automatic
(IngeTrazo)** follows the host's language, using English for unsupported languages.
Object names and tags written by the user are preserved.

Click a name to select; double-click or Enter to edit; F2 to rename; Esc to leave
one editing level; F to frame the selection. Click an eye to hide/show an object.
Drag onto another group to nest, or onto Model to move to the root. Turn off
A–Z sorting to reorder siblings. Multiple selection works within one container.
Right-click for tag assignment, visibility, renaming, deletion and framing.
Section indicators activate/deactivate cuts; only one cut can be active.

## Scope

Reorganizing preserves world positions, shared meshes, materials and plugin data.
Tag locks are respected; IngeTrazo 0.5.7 has no native individual group lock.
Section planes remain at model level. Restructure only after reassembling an
exploded view. Renaming affects the selected instance; changing the hierarchy
does not automatically restructure other component copies. Narrow panels hide
the tag column automatically.

Verified against the real IngeTrazo 0.5.7 source, commit 6be29fe. Other 0.x
versions need compatibility checks. Close IngeTrazo and remove the outliner
folder to uninstall. See [the detailed Spanish guide](README.md) for development
commands and further behavior notes.

## Open source

JA Tree **0.1.0** is the first version prepared for public release. Licensed under
**GPL-3.0-or-later**; see [LICENSE](LICENSE), [notices](NOTICES.md),
[contribution and build instructions](CONTRIBUTING.md) and [changes](CHANGELOG.md).
Both an installable ZIP and a corresponding source archive are provided.
