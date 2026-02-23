class ArrierroNode:
    """
    Nodo para el problema del Arriero.
    
    Estado: (Hi, Pi, Ci, Li, B, Hf, Pf, Cf, Lf)
    donde:
    - Hi, Pi, Ci, Li: 1 si esta en izquierda, 0 si esta en derecha
    - B: 'i' si bote esta en izquierda, 'f' si esta en derecha
    - Hf, Pf, Cf, Lf: 1 si esta en derecha, 0 si esta en izquierda (redundantes pero explicitos)
    
    Restricciones:
    - El Puma y la Cabra no pueden estar juntos sin el Hombre
    - La Cabra y la Lechuga no pueden estar juntas sin el Hombre
    - El bote tiene capacidad para el Hombre + solo 1 cosa mas
    - El Hombre siempre se mueve con el bote
    """
    
    def __init__(self, hi=1, pi=1, ci=1, li=1, b='i'):
        """
        hi, pi, ci, li: posicion en izquierda (1) o derecha (0)
        b: posicion del bote ('i' o 'f')
        """
        self.hi = hi
        self.pi = pi
        self.ci = ci
        self.li = li
        self.b = b
        
        # Los valores en derecha son inversos
        self.hf = 1 - hi
        self.pf = 1 - pi
        self.cf = 1 - ci
        self.lf = 1 - li
    
    def get_state(self):
        """Retorna el estado como tupla"""
        return (self.hi, self.pi, self.ci, self.li, self.b)
    
    def get_left(self):
        """Retorna los elementos en la orilla izquierda"""
        elements = []
        if self.hi == 1: elements.append("H")
        if self.pi == 1: elements.append("P")
        if self.ci == 1: elements.append("C")
        if self.li == 1: elements.append("L")
        return elements
    
    def get_right(self):
        """Retorna los elementos en la orilla derecha"""
        elements = []
        if self.hi == 0: elements.append("H")
        if self.pi == 0: elements.append("P")
        if self.ci == 0: elements.append("C")
        if self.li == 0: elements.append("L")
        return elements
    
    def __str__(self):
        """Representacion legible del estado"""
        lado_bote = "Derecha" if self.b == 'f' else "Izquierda"
        left = self.get_left()
        right = self.get_right()
        return f"Izq: {str(left):20s} Der: {str(right):20s} Bote: {lado_bote:8s} ({self.get_state()})"
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def is_valid_state(hi, pi, ci, li):
        """
        Verifica que el estado sea valido.
        No puede haber combinaciones peligrosas en ninguna orilla
        a menos que el Hombre este alli.
        """
        # Si Puma y Cabra estan en la misma orilla sin el Hombre
        if pi == ci and pi != hi:
            return False
        
        # Si Cabra y Lechuga estan en la misma orilla sin el Hombre
        if ci == li and ci != hi:
            return False
        
        return True
    
    def generate_children(self, previous_states, parent_map):
        """
        Genera todos los hijos validos del nodo actual.
        El Hombre SIEMPRE se mueve (el bote solo se mueve con el hombre).
        El bote puede transportar al Hombre + solo 1 cosa mas.
        """
        children = []
        
        # El Hombre debe estar donde esta el bote para poder moverse
        if (self.b == 'i' and self.hi != 1) or (self.b == 'f' and self.hi != 0):
            return children
        
        # El Hombre siempre se mueve, asi que el bote siempre cambia de lado
        new_b = 'f' if self.b == 'i' else 'i'
        
        # Identificar que elementos estan en el mismo lado que el Hombre
        same_side = []
        if (self.b == 'i' and self.pi == 1) or (self.b == 'f' and self.pi == 0):
            same_side.append('P')
        if (self.b == 'i' and self.ci == 1) or (self.b == 'f' and self.ci == 0):
            same_side.append('C')
        if (self.b == 'i' and self.li == 1) or (self.b == 'f' and self.li == 0):
            same_side.append('L')
        
        # Opcion 1: Mover solo al Hombre (sin elementos)
        new_hi = 0 if self.hi == 1 else 1
        new_pi = self.pi
        new_ci = self.ci
        new_li = self.li
        
        if ArrierroNode.is_valid_state(new_hi, new_pi, new_ci, new_li):
            new_state = (new_hi, new_pi, new_ci, new_li, new_b)
            if new_state not in previous_states:
                child = ArrierroNode(new_hi, new_pi, new_ci, new_li, new_b)
                children.append(child)
                parent_map[child] = self
        
        # Opcion 2: Mover al Hombre con 1 elemento (capacidad del bote: H + 1)
        for element in same_side:
            new_hi = 0 if self.hi == 1 else 1
            new_pi = (0 if self.pi == 1 else 1) if element == 'P' else self.pi
            new_ci = (0 if self.ci == 1 else 1) if element == 'C' else self.ci
            new_li = (0 if self.li == 1 else 1) if element == 'L' else self.li
            
            if ArrierroNode.is_valid_state(new_hi, new_pi, new_ci, new_li):
                new_state = (new_hi, new_pi, new_ci, new_li, new_b)
                if new_state not in previous_states:
                    child = ArrierroNode(new_hi, new_pi, new_ci, new_li, new_b)
                    children.append(child)
                    parent_map[child] = self
        
        return children


def find_solution(root_node, use_bfs=False):
    """
    Encuentra una solucion al problema del Arriero.
    
    use_bfs: 
        False para DFS (Depth-First Search)
        True para BFS (Breadth-First Search)
    
    Retorna: Lista de estados desde el inicio hasta la meta, numero de iteraciones
    """
    to_visit = [root_node]
    previous_states = set()
    parent_map = {root_node.get_state(): None}
    
    iterations = 0
    
    while to_visit:
        iterations += 1
        
        # DFS: pop del final (-1) | BFS: pop del inicio (0)
        node = to_visit.pop(0 if use_bfs else -1)
        node_state = node.get_state()
        
        # Agregar a estados visitados
        if node_state not in previous_states:
            previous_states.add(node_state)
        
        # Generar hijos
        children = node.generate_children(previous_states, parent_map)
        
        # Agregar referencias en el mapa de padres
        for child in children:
            parent_map[child.get_state()] = node_state
        
        # Agregar hijos a la cola
        to_visit.extend(children)
        
        # Verificar si alcanzamos la meta: todos en la derecha (0,0,0,0,'f')
        if node.hi == 0 and node.pi == 0 and node.ci == 0 and node.li == 0 and node.b == 'f':
            # Reconstruir el camino desde la raiz hasta la meta
            solution = []
            current_state = node.get_state()
            
            while current_state is not None:
                hi, pi, ci, li, b = current_state
                solution = [ArrierroNode(hi, pi, ci, li, b)] + solution
                current_state = parent_map.get(current_state)
            
            return solution, iterations
    
    return None, iterations


def print_solution(solution, iterations, search_type):
    """Imprime la solucion de forma legible"""
    if solution is None:
        print(f"No se encontro solucion usando {search_type}")
        return
    
    print(f"\nSOLUCION ENCONTRADA USANDO {search_type}")
    print("=" * 100)
    
    for i, state in enumerate(solution):
        print(f"Paso {i}: {state}")
    
    print("=" * 100)
    print(f"Total de pasos: {len(solution) - 1}")


if __name__ == "__main__":
    print("\nPROBLEMA DEL ARRIERO")
    print("=" * 100)
    print("Restricciones:")
    print("  - El Puma y la Cabra no pueden estar juntos sin el Hombre")
    print("  - La Cabra y la Lechuga no pueden estar juntas sin el Hombre")
    print("  - El Hombre siempre se mueve con el bote")
    print("  - El bote tiene capacidad para el Hombre + solo 1 cosa mas")
    print("  - Estado inicial: todos en orilla izquierda, bote en izquierda")
    print("  - Estado objetivo: todos en orilla derecha, bote en derecha")
    print("=" * 100)
    
    # Solucion con DFS
    print("\nBUSQUEDA EN PROFUNDIDAD (DFS)")
    root = ArrierroNode(1, 1, 1, 1, 'i')
    solution_dfs, iterations_dfs = find_solution(root, use_bfs=False)
    print_solution(solution_dfs, iterations_dfs, "DFS")
    print(f"Iteraciones totales: {iterations_dfs}")
    
    # Solucion con BFS
    print("\n" + "=" * 100)
    print("\nBUSQUEDA EN AMPLITUD (BFS)")
    root = ArrierroNode(1, 1, 1, 1, 'i')
    solution_bfs, iterations_bfs = find_solution(root, use_bfs=True)
    print_solution(solution_bfs, iterations_bfs, "BFS")
    print(f"Iteraciones totales: {iterations_bfs}")
    
    # Comparacion
    print("\n" + "=" * 100)
    print("\nCOMPARACION DFS vs BFS:")
    if solution_dfs and solution_bfs:
        print(f"  DFS - Pasos: {len(solution_dfs) - 1}, Iteraciones: {iterations_dfs}")
        print(f"  BFS - Pasos: {len(solution_bfs) - 1}, Iteraciones: {iterations_bfs}")
        
        if len(solution_dfs) - 1 < len(solution_bfs) - 1:
            print(f"  DFS encontro una solucion mas corta ({len(solution_dfs) - 1} vs {len(solution_bfs) - 1} pasos)")
        elif len(solution_dfs) - 1 > len(solution_bfs) - 1:
            print(f"  BFS encontro una solucion mas corta ({len(solution_bfs) - 1} vs {len(solution_dfs) - 1} pasos)")
        else:
            print(f"  Ambos encontraron soluciones con igual numero de pasos ({len(solution_dfs) - 1})")
