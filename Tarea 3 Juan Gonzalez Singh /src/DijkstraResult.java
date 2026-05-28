import java.util.*;

/**
 * Clase que encapsula los resultados del algoritmo de Dijkstra
 * Contiene las distancias mínimas, predecesores y métodos para reconstruir caminos
 */
public class DijkstraResult {
    private int[] distances;      // Distancias mínimas desde el nodo origen
    private int[] predecessors;   // Predecesores para reconstruir caminos
    private int source;          // Nodo origen
    
    /**
     * Constructor para crear un resultado de Dijkstra
     * @param distances Array con las distancias mínimas
     * @param predecessors Array con los predecesores
     * @param source Nodo origen
     */
    public DijkstraResult(int[] distances, int[] predecessors, int source) {
        this.distances = distances.clone();
        this.predecessors = predecessors.clone();
        this.source = source;
    }
    
    /**
     * Obtiene la distancia mínima a un nodo específico
     * @param destination Nodo destino
     * @return Distancia mínima al nodo destino
     */
    public int getDistance(int destination) {
        if (destination < 0 || destination >= distances.length) {
            throw new IllegalArgumentException("Nodo destino fuera de rango");
        }
        return distances[destination];
    }
    
    /**
     * Obtiene el predecesor de un nodo en el camino más corto
     * @param node El nodo del cual obtener el predecesor
     * @return El predecesor del nodo (-1 si no tiene predecesor)
     */
    public int getPredecessor(int node) {
        if (node < 0 || node >= predecessors.length) {
            throw new IllegalArgumentException("Nodo fuera de rango");
        }
        return predecessors[node];
    }
    
    /**
     * Reconstruye el camino más corto desde el origen hasta un nodo destino
     * @param destination Nodo destino
     * @return Lista con el camino (desde origen hasta destino)
     */
    public List<Integer> getPath(int destination) {
        if (destination < 0 || destination >= distances.length) {
            throw new IllegalArgumentException("Nodo destino fuera de rango");
        }
        
        List<Integer> path = new ArrayList<>();
        
        // Si no hay camino al destino
        if (DijkstraConstants.isInfinite(distances[destination])) {
            return path; // Retorna lista vacía
        }
        
        // Reconstruir el camino desde el destino hacia el origen
        int current = destination;
        while (current != DijkstraConstants.NO_PREDECESSOR) {
            path.add(current);
            current = predecessors[current];
        }
        
        // Invertir el camino para que vaya desde origen hasta destino
        Collections.reverse(path);
        return path;
    }
    
    /**
     * Obtiene el camino como una cadena de texto
     * @param destination Nodo destino
     * @return Cadena con el camino
     */
    public String getPathAsString(int destination) {
        List<Integer> path = getPath(destination);
        
        if (path.isEmpty()) {
            return "No existe camino";
        }
        
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < path.size(); i++) {
            sb.append(path.get(i));
            if (i < path.size() - 1) {
                sb.append(" -> ");
            }
        }
        return sb.toString();
    }
    
    /**
     * Verifica si existe un camino a un nodo destino
     * @param destination Nodo destino
     * @return true si existe camino, false en caso contrario
     */
    public boolean hasPathTo(int destination) {
        if (destination < 0 || destination >= distances.length) {
            return false;
        }
        return !DijkstraConstants.isInfinite(distances[destination]);
    }
    
    /**
     * Obtiene todas las distancias calculadas
     * @return Copia del array de distancias
     */
    public int[] getAllDistances() {
        return distances.clone();
    }
    
    /**
     * Obtiene todos los predecesores
     * @return Copia del array de predecesores
     */
    public int[] getAllPredecessors() {
        return predecessors.clone();
    }
    
    /**
     * Obtiene el nodo origen
     * @return Nodo origen
     */
    public int getSource() {
        return source;
    }
    
    /**
     * Imprime un resumen de los resultados
     */
    public void printResults() {
        System.out.println("=== Resultados del Algoritmo de Dijkstra ===");
        System.out.println("Nodo origen: " + source);
        System.out.println();
        
        for (int i = 0; i < distances.length; i++) {
            String distance = DijkstraConstants.formatDistance(distances[i]);
            String path = getPathAsString(i);
            
            System.out.println("Nodo " + i + ":");
            System.out.println("  Distancia: " + distance);
            System.out.println("  Camino: " + path);
            System.out.println();
        }
    }
}
