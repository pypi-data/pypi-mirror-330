# Func3DCad

Func3DCad - это Python-пакет для работы с 3D-моделями, включающий базовые функции по созданию, трансформации, вычислениям, экспорту и рендерингу моделей.

## Возможности

- Создание 3D-моделей (вершины и грани)
- Трансформации (масштабирование, перемещение)
- Вычисление площади поверхности и объема модели
- Экспорт и импорт моделей из файлов
- Упрощенный рендеринг модели в консоли

## Установка

```bash
pip install Func3DCad
```

## Использование

### Импорт библиотеки

```python
from Func3DCad import Model3D, Transform, calculate_volume, calculate_surface_area, export_model, import_model, render_model
```

### Создание модели

```python
model = Model3D()
model.add_vertex((0, 0, 0))
model.add_vertex((1, 0, 0))
model.add_vertex((0, 1, 0))
model.add_face((0, 1, 2))
```

### Трансформации

```python
Transform.scale(model, 2)  # Увеличить в 2 раза
Transform.translate(model, 1, 1, 1)  # Сместить на (1,1,1)
```

### Вычисления

```python
volume = calculate_volume(model)
surface_area = calculate_surface_area(model)
print(f"Объем: {volume}, Площадь поверхности: {surface_area}")
```

### Экспорт и импорт модели

```python
export_model(model, "model.txt")
new_model = import_model("model.txt")
```

### Рендеринг в консоли

```python
render_model(model)
```

## Разработка

Если вы хотите внести вклад в развитие проекта, форкните репозиторий и создайте Pull Request.

## Лицензия

Этот проект распространяется под лицензией MIT.
