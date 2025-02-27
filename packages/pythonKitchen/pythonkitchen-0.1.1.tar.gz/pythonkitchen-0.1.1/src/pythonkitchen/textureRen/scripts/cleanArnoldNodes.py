import hou

def clean_arImgNodes(matlib: hou.Node):
    for arnold_mat in matlib.children():
        if arnold_mat.type().name() == 'arnold_materialbuilder':
            for arnold_image_node in arnold_mat.children():
                if arnold_image_node.type().name()=='arnold::image':
                    current_node_name = arnold_image_node.name()
                    corrected_node_name = current_node_name.split('.')[0]
                    arnold_image_node.setName(corrected_node_name)

clean_arImgNodes(hou.selectedNodes()[0])
