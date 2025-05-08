import pandas as pd
import re
from treelib import Tree

def clean_key(key):
    return re.sub(r'[^a-zA-Z0-9]', '', key)

def get_format_mask(key):
    return re.sub(r'\d', '0', re.sub(r'[a-zA-Z]', 'A', key))

def get_prefixes(key):
    return [key[:i] for i in range(1, len(key) + 1)]

def build_hierarchy(df):
    # Desduplicar claves antes de limpiar
    keys = df['clave'].drop_duplicates().tolist()
    if len(keys) != len(df['clave']):
        raise ValueError("Duplicados encontrados en la columna 'clave' antes de limpiar.")
    
    # Limpiar claves
    cleaned_keys = [clean_key(key) for key in keys]
    # Verificar duplicados después de limpiar
    if len(cleaned_keys) != len(set(cleaned_keys)):
        raise ValueError("Duplicados encontrados después de limpiar las claves.")
    
    # Verificar consistencia en el formato usando máscara
    format_masks = [get_format_mask(key) for key in cleaned_keys]
    if len(set(format_masks)) > 1:
        raise ValueError(f"Inconsistencia en el formato de las claves: {set(format_masks)}")
    
    # Mapa de clave limpia a original
    clean_to_original = {clean_key(key): key for key in keys}
    
    # Encontrar todos los prefijos
    all_prefixes = set()
    for key in cleaned_keys:
        all_prefixes.update(get_prefixes(key))
    
    # Identificar padres implícitos
    implicit_parents = {prefix for prefix in all_prefixes if prefix not in cleaned_keys}
    
    # Construir la jerarquía
    hierarchy = {}
    levels = {}
    for key in cleaned_keys:
        prefixes = get_prefixes(key)[:-1]  # Excluir la propia clave
        parent = None
        for prefix in reversed(prefixes):  # Buscar el prefijo más largo
            if prefix in cleaned_keys or prefix in implicit_parents:
                parent = prefix
                break
        hierarchy[key] = parent
        if parent is None:
            levels[key] = 1  # Nivel inicial
        else:
            levels[key] = levels.get(parent, 0) + 1
    
    # Generar la salida
    output = []
    for clean_key, original_key in clean_to_original.items():
        parent_clean = hierarchy.get(clean_key)
        if parent_clean:
            parent_original = clean_to_original.get(parent_clean, parent_clean)
            tipo_padre = "explícito" if parent_clean in cleaned_keys else "implícito"
        else:
            parent_original = None
            tipo_padre = None
        nivel = levels[clean_key]
        output.append({
            "clave": original_key,
            "padre": parent_original,
            "nivel": nivel,
            "tipo_padre": tipo_padre
        })
    
    return pd.DataFrame(output)

def visualize_tree(df_hierarchy):
    tree = Tree()
    roots = df_hierarchy[df_hierarchy['padre'].isna()]
    for _, row in roots.iterrows():
        tree.create_node(row['clave'], row['clave'])
    
    for _, row in df_hierarchy.iterrows():
        if row['padre']:
            tree.create_node(row['clave'], row['clave'], parent=row['padre'])
    
    tree.show()

# Ejemplo de uso
if __name__ == "__main__":
    df = pd.DataFrame({"clave": ["ZZZ", "ZZA", "ZZB"]})
    try:
        df_hierarchy = build_hierarchy(df)
        print(df_hierarchy)
        visualize_tree(df_hierarchy)
    except ValueError as e:
        print(f"Error: {e}")