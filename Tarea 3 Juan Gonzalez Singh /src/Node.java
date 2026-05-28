/**
 * Clase que representa un nodo en la cola de prioridad del algoritmo de Dijkstra
 * Implementa Comparable para poder ser usado en una PriorityQueue
 */
public class Node implements Comparable<Node> {
    private int id;       // Identificador del nodo
    private int distance; // Distancia desde el nodo origen
    
    /**
     * Constructor para crear un nuevo nodo
     * @param id Identificador del nodo
     * @param distance Distancia desde el nodo origen
     */
    public Node(int id, int distance) {
        this.id = id;
        this.distance = distance;
    }
    
    // Getters
    public int getId() {
        return id;
    }
    
    public int getDistance() {
        return distance;
    }
    
    // Setters
    public void setId(int id) {
        this.id = id;
    }
    
    public void setDistance(int distance) {
        this.distance = distance;
    }
    
    /**
     * Compara dos nodos basándose en su distancia
     * Necesario para la cola de prioridad (menor distancia tiene prioridad)
     */
    @Override
    public int compareTo(Node other) {
        return Integer.compare(this.distance, other.distance);
    }
    
    @Override
    public String toString() {
        return "Node{id=" + id + ", distance=" + distance + "}";
    }
}
