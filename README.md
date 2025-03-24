# c4maker-server

Modern software, often is composed of several components that can interact with each other. 
To explain well how it works, it is necessary different diagrams and documentation making the organization a challenge task. 
C4maker is project that aims to make easier the documentation of complex software by integrating different type of documentation 
and creating meaningful linking between them.

## Entities

- Workspace: is the highest hierarchy entity that represents the whole software. Inside a workspace, we can create different diagrams or documentations that share the same items.
- Diagram: represents each diagram or documentation
- DiagramItem: the items that each diagram has. It could be a component, database, software entity, etc.
- WorkspaceItem: each DiagramItem is a WorkspaceItem. This is entity belongs to Workspace and is used to link the different Diagrams in the same Workspace