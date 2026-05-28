import java.util.*;

/**
 * Clase que representa un grafo dirigido ponderado
 * Utiliza una lista de adyacencia para almacenar las conexiones
 */
public class Graph {
    private Map<Integer, List<Edge>> adjacencyList; // Lista de adyacencia
    private int numberOfVertices; // Número de vértices
    
    /**
     * Constructor que inicializa el grafo
     * @param numberOfVertices Número de vértices en el grafo
     */
    public Graph(int numberOfVertices) {
        this.numberOfVertices = numberOfVertices;
        this.adjacencyList = new HashMap<>();
        
        // Inicializar la lista de adyacencia para cada vértice
        for (int i = 0; i < numberOfVertices; i++) {
            adjacencyList.put(i, new ArrayList<>());
        }
    }
    
    /**
     * Agrega una arista al grafo
     * @param source Nodo de origen
     * @param destination Nodo de destino
     * @param weight Peso de la arista
     */
    public void addEdge(int source, int destination, int weight) {
        // Validar que los nodos existan
        if (source < 0 || source >= numberOfVertices || 
            destination < 0 || destination >= numberOfVertices) {
            throw new IllegalArgumentException("Los nodos deben estar en el rango [0, " + (numberOfVertices - 1) + "]");
        }
        
        if (weight < 0) {
            throw new IllegalArgumentException("El peso debe ser no negativo");
        }
        
        adjacencyList.get(source).add(new Edge(destination, weight));
    }
    
    /**
     * Agrega una arista bidireccional (para grafos no dirigidos)
     * @param node1 Primer nodo
     * @param node2 Segundo nodo
     * @param weight Peso de la arista
     */
    public void addBidirectionalEdge(int node1, int node2, int weight) {
        addEdge(node1, node2, weight);
        addEdge(node2, node1, weight);
    }
    
    /**
     * Obtiene la lista de vecinos de un nodo
     * @param node El nodo del cual obtener los vecinos
     * @return Lista de aristas (vecinos) del nodo
     */
    public List<Edge> getNeighbors(int node) {
        if (node < 0 || node >= numberOfVertices) {
            throw new IllegalArgumentException("El nodo debe estar en el rango [0, " + (numberOfVertices - 1) + "]");
        }
        return adjacencyList.get(node);
    }
    
    // Getters
    public int getNumberOfVertices() {
        return numberOfVertices;
    }
    
    public Map<Integer, List<Edge>> getAdjacencyList() {
        return adjacencyList;
    }
    
    /**
     * Muestra la representación del grafo
     */
    public void printGraph() {
        System.out.println("Grafo (Lista de Adyacencia):");
        for (int i = 0; i < numberOfVertices; i++) {
            System.out.print("Nodo " + i + ": ");
            for (Edge edge : adjacencyList.get(i)) {
                System.out.print("(" + edge.getDestination() + ", peso: " + edge.getWeight() + ") ");
            }
            System.out.println();
        }
    }
}
