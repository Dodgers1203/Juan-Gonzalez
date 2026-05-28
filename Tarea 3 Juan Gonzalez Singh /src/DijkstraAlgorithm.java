import java.util.*;

/**
 * Implementación del Algoritmo de Dijkstra para encontrar 
 * el camino más corto desde un nodo origen a todos los demás nodos
 */
public class DijkstraAlgorithm {
    protected Graph graph; // El grafo sobre el cual ejecutar el algoritmo
    
    /**
     * Constructor que recibe el grafo
     * @param graph El grafo sobre el cual ejecutar Dijkstra
     */
    public DijkstraAlgorithm(Graph graph) {
        this.graph = graph;
    }
    
    /**
     * Ejecuta el algoritmo de Dijkstra desde un nodo origen
     * @param source Nodo origen desde el cual calcular las distancias
     * @return DijkstraResult con las distancias y predecesores
     */
    public DijkstraResult dijkstra(int source) {
        int numVertices = graph.getNumberOfVertices();
        
        // Validar el nodo origen
        if (source < 0 || source >= numVertices) {
            throw new IllegalArgumentException("El nodo origen debe estar en el rango [0, " + (numVertices - 1) + "]");
        }
        
        // Inicializar estructuras de datos
        int[] distances = new int[numVertices];     // Distancias mínimas
        int[] predecessors = new int[numVertices];  // Predecesores para reconstruir caminos
        boolean[] visited = new boolean[numVertices]; // Nodos visitados
        
        // Inicializar todas las distancias como infinito y predecesores como -1
        Arrays.fill(distances, DijkstraConstants.INFINITY);
        Arrays.fill(predecessors, DijkstraConstants.NO_PREDECESSOR);
        
        // La distancia del nodo origen a sí mismo es 0
        distances[source] = 0;
        
        // Cola de prioridad para seleccionar siempre el nodo con menor distancia
        PriorityQueue<Node> priorityQueue = new PriorityQueue<>();
        priorityQueue.offer(new Node(source, 0));
        
        System.out.println("=== Iniciando Algoritmo de Dijkstra desde el nodo " + source + " ===");
        
        while (!priorityQueue.isEmpty()) {
            // Extraer el nodo con menor distancia
            Node current = priorityQueue.poll();
            int currentId = current.getId();
            int currentDistance = current.getDistance();
            
            // Si ya fue visitado, continuar (puede haber duplicados en la cola)
            if (visited[currentId]) {
                continue;
            }
            
            // Marcar como visitado
            visited[currentId] = true;
            
            System.out.println("Procesando nodo " + currentId + " con distancia " + currentDistance);
            
            // Explorar todos los vecinos
            for (Edge edge : graph.getNeighbors(currentId)) {
                int neighbor = edge.getDestination();
                int edgeWeight = edge.getWeight();
                
                // Calcular nueva distancia a través del nodo actual
                if (!DijkstraConstants.isInfinite(distances[currentId])) {
                    int newDistance = distances[currentId] + edgeWeight;
                    
                    // Si encontramos un camino más corto, actualizar
                    if (newDistance < distances[neighbor]) {
                        System.out.println("  Actualizando distancia al nodo " + neighbor + 
                                         " de " + DijkstraConstants.formatDistance(distances[neighbor]) + 
                                         " a " + newDistance);
                        
                        distances[neighbor] = newDistance;
                        predecessors[neighbor] = currentId;
                        priorityQueue.offer(new Node(neighbor, newDistance));
                    }
                }
            }
        }
        
        System.out.println("=== Algoritmo completado ===\n");
        return new DijkstraResult(distances, predecessors, source);
    }
    
    /**
     * Encuentra el camino más corto entre dos nodos específicos
     * @param source Nodo origen
     * @param destination Nodo destino
     * @return DijkstraResult con la información del camino
     */
    public DijkstraResult shortestPath(int source, int destination) {
        DijkstraResult result = dijkstra(source);
        
        if (DijkstraConstants.isInfinite(result.getDistance(destination))) {
            System.out.println("No existe camino desde el nodo " + source + " al nodo " + destination);
        } else {
            System.out.println("Distancia más corta desde " + source + " hasta " + destination + ": " + 
                             result.getDistance(destination));
            System.out.println("Camino: " + result.getPathAsString(destination));
        }
        
        return result;
    }
}
