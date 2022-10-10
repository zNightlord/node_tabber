# node_tabber

Node Tabber is a Houdini/Nuke style node adding tool for Blender's Node tree graphs; namely the Shader, Compositing, Texture and Geometry.

Instead of having to press SHIFT+A and then scrolling the sub menus to fins the correct node, or even clicking on the search menu and maybe getting the correct node; you can just press the TAB button which will bring up an intelligent search list which even supports node acronyms. For example, typing SX would bring up the Seperate XYZ node.
This saves a lot of time when working with large node trees.

# Fork

This is a fork which includes:
- Additional sub node entries for new vector math operations
- Geometry Nodes sub node entries (i.e. switch/random value nodes)
- Fix for appending custom nodegroups (see https://github.com/jiggymoon69/node_tabber/pull/10)
- Workaround for [this commit(Blender 3.4+)](https://github.com/blender/blender/commit/837144b4577f161baf1625f8a5478c83a088ea0f) which breaks the add-on with geonodes. See [D15973](https://developer.blender.org/D15973).
  
## Installation (Blender 3.4+)
Download this [repository](https://github.com/williamchange/node_tabber/archive/refs/heads/master.zip) and install from Blender's preferences, just like any other add-on (no need to unzip)