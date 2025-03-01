import os
from ctb_writer import CherryTree, CherryTreeNodeBuilder

if os.path.exists("my_notes.ctb"):
    ctb_document = CherryTree.load("my_notes.ctb")
    ctb_document.save("copy.ctb")
    exit(0)

ctb_document = CherryTree() # Init the cherry tree document
root_id = ctb_document.add_child("Root node") # Add a node with a name

ctb_document.add_child("child node1", parent_id=root_id) # Add a child to the root node
node2_id = ctb_document.add_child("Root node 2", text="Content of this node", icon="add") # Add another root node, with some meta_infos

new_node = CherryTreeNodeBuilder("New node").icon("star")\
                                            .text("Content of the node\n", style={'fg': '#ff5445', 'bg': '#ffffff', "bold": True, "size": "h4"})\
                                            .image("images/ghost.png", justification="center")\
                                            .text("\nUnder image")\
                                            .set_read_only()\
                                            .get_node() # build the node from the previous infos

multicolor_node = CherryTreeNodeBuilder("New node").icon("pizza")\
                                                   .texts([("bold", "Hey !\n"),
                                                           ("fg:orange|bg:#ff0000", "This is a multi color texts\n"),
                                                           ("fg:orange", "123456 bgrt12345rtg\n12345\n"),
                                                           ("underline|size:h2", "END\n\n")]).get_node()

multicolor_node.replace("multi color", "reaaly multi color", style={"fg": "red"})
multicolor_node.replace("12345", "yellow??", style={"bg": "bisque", "bold": True, "size": "h1"})

other_node = CherryTreeNodeBuilder("New node", bold=True, color='darkorange').icon("python")\
                                                                             .text("tests\n", style={"underline": True, "size":"h1"})\
                                                                             .codebox("import os\nprint('test')\n", syntax='python')\
                                                                             .get_node()
text_content = """
[(bold|underline)]Title:[/]
 - [(fg:orange)]orange[/]
 - [(bg:sun)]yellow background[/]
 - [(fg:blue|underline)]blue underlined[/]

[(bg:sun|fg:orange)]                                                [/]

"""

table = [["Content1", "C2"], ["Content2", "C3"], ["Col1", "Col2"]]
table_node = CherryTreeNodeBuilder("Table").icon("maths").table(content=table).texts(text_content).get_node()


new_node_id = ctb_document.add_child(new_node, parent_id=root_id) # Add this node as the child of the first root node

print(new_node_id)
other_node_id = ctb_document.add_child(other_node, parent_id=new_node_id)
ctb_document.add_child(table_node, parent_id=other_node_id)

print(ctb_document.get_node_by_id(new_node_id))
print(ctb_document.get_node_by_id(other_node_id))


code_node = CherryTreeNodeBuilder("Configuration", type="code", syntax="ini", color="lightsalmon")\
                                 .icon("building")\
                                 .text("[Test]\ncode=test\n\n[Account]\nuser=test\nprivs=Admin\n")\
                                 .set_read_only()\
                                 .get_node()

plain_node = CherryTreeNodeBuilder("Configuration", type="plain").icon("cloud").text("ljbdezjlbflnkfzelknflez").get_node()

ctb_document.add_child(code_node, parent_id=node2_id)
ctb_document.add_child(plain_node, parent_id=node2_id)
ctb_document.add_child(multicolor_node, parent_id=root_id)

ctb_document.save("my_notes.ctb") # Save your CherryTree in "my_notes.ctb"
