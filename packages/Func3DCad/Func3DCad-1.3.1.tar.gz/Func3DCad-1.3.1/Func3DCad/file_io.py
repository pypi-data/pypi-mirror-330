from core import *

def export_model(model, filepath):
    """Экспорт 3D-модели в файл."""
    with open(filepath, "w") as file:
        file.write("vertices:\n")
        for v in model.vertices:
            file.write(f"{v}\n")
        file.write("faces:\n")
        for f in model.faces:
            file.write(f"{f}\n")

def import_model(filepath):
    """Импорт 3D-модели из файла."""
    model = Model3D()
    with open(filepath, "r") as file:
        lines = file.readlines()
        parsing_vertices = True
        for line in lines:
            line = line.strip()
            if line == "faces:":
                parsing_vertices = False
                continue
            if line and parsing_vertices:
                model.add_vertex(tuple(map(float, line.strip("()").split(","))))
            elif line:
                model.add_face(tuple(map(int, line.strip("()").split(","))))
    return model
