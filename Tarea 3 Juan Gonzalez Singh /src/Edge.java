/**
 * Clase que representa una arista en el grafo
 * Cada arista tiene un nodo destino y un peso
 */
public class Edge {
    private int destination; // Nodo de destino
    private int weight;      // Peso de la arista
    
    /**
     * Constructor para crear una nueva arista
     * @param destination Nodo de destino
     * @param weight Peso de la arista
     */
    public Edge(int destination, int weight) {
        this.destination = destination;
        this.weight = weight;
    }
    
    // Getters
    public int getDestination() {
        return destination;
    }
    
    public int getWeight() {
        return weight;
    }
    
    // Setters
    public void setDestination(int destination) {
        this.destination = destination;
    }
    
    public void setWeight(int weight) {
        this.weight = weight;
    }
    
    @Override
    public String toString() {
        return "Edge{destination=" + destination + ", weight=" + weight + "}";
    }
}
