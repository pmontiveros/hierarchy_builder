# Explicación del Script `hierarchy_builder.py`

Este script en Python procesa una columna de claves alfanuméricas en un DataFrame para deducir su relación jerárquica, generando una tabla con las claves, sus padres, niveles jerárquicos y tipo de padre (explícito o implícito). También visualiza la jerarquía como un árbol textual.

## Propósito
- Analizar una columna de claves alfanuméricas para identificar su estructura jerárquica, incluso si los padres son implícitos o los formatos varían (ancho fijo/variable, con/sin delimitadores).
- Generar una tabla con la jerarquía y visualizarla como un árbol.

## Entradas
- **Formato**: Un DataFrame de pandas con una columna llamada `clave` que contiene valores alfanuméricos (e.g., `["ZZZ", "ZZA", "ZZB"]` o `["10-00", "10-01", "10-01-01"]`).
- **Restricciones**:
  - Las claves deben ser únicas antes de limpiar delimitadores.
  - Todas las claves deben seguir un formato consistente (detectado mediante máscaras de formato).
  - Las claves vacías se ignoran; los duplicados generan un error.

## Salidas
- **Tabla (DataFrame)**:
  - Columnas:
    - `clave`: Clave original (con delimitadores si los hay).
    - `padre`: Clave del padre (o `None` si no tiene padre explícito).
    - `nivel`: Nivel jerárquico (1 para claves sin padre explícito, 2 para sus hijos, etc.).
    - `tipo_padre`: Indica si el padre es "explícito" (presente en los datos) o "implícito" (inferido).
  - Ejemplo para `["ZZZ", "ZZA", "ZZB"]`:
    ```plaintext
       clave  padre  nivel tipo_padre
    0   ZZZ     ZZ      1   implícito
    1   ZZA     ZZ      1   implícito
    2   ZZB     ZZ      1   implícito
    ```
- **Visualización**:
  - Árbol textual generado con `treelib`.
  - Ejemplo para `["ZZZ", "ZZA", "ZZB"]`:
    ```plaintext
    ZZ (implícito)
    ├── ZZA
    ├── ZZB
    └── ZZZ
    ```

## Estrategia (alto nivel)
- Leer la columna `clave` del DataFrame.
- Desduplicar claves y verificar consistencia de formato usando máscaras.
- Eliminar delimitadores para obtener claves alfanuméricas puras.
- Identificar prefijos (explícitos e implícitos) para deducir la jerarquía.
- Asignar padres y niveles (nivel 1 para claves sin padre explícito, incrementando para hijos).
- Generar tabla con `clave`, `padre`, `nivel`, `tipo_padre`.
- Visualizar la jerarquía como árbol textual con `treelib`.

## Manejo de Errores
- **Duplicados**: Error si hay claves duplicadas antes o después de limpiar.
- **Inconsistencias**: Error si las claves no comparten un formato consistente (e.g., `["20", "AA"]`).
- **Advertencia**: Si todas las claves son raíces, se notifica pero se continúa.

## Librerías
- `pandas`: Manejo de DataFrame.
- `re`: Eliminación de delimitadores.
- `treelib`: Visualización de árboles.

## Uso
```python
import pandas as pd
from hierarchy_builder import build_hierarchy, visualize_tree

df = pd.DataFrame({"clave": ["ZZZ", "ZZA", "ZZB"]})
try:
    df_hierarchy = build_hierarchy(df)
    print(df_hierarchy)
    visualize_tree(df_hierarchy)
except ValueError as e:
    print(f"Error: {e}")
```
