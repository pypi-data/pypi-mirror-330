def render_model(model):
    """Выводит модель в консоль (очень упрощенный рендеринг)."""
    print("Rendering 3D Model:")
    for v in model.vertices:
        print(f"Vertex: {v}")
    for f in model.faces:
        print(f"Face: {f}")
