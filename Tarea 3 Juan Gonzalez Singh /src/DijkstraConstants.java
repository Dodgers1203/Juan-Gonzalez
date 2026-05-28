/**
 * Clase que contiene las constantes utilizadas en el algoritmo de Dijkstra
 */
public class DijkstraConstants {
    
    /**
     * Valor que representa infinito en el algoritmo de Dijkstra
     * Se usa Integer.MAX_VALUE para representar una distancia infinita
     */
    public static final int INFINITY = Integer.MAX_VALUE;
    
    /**
     * Representación en texto del valor infinito para impresión en consola
     */
    public static final String INFINITY_SYMBOL = "INFINITO";
    
    /**
     * Valor que indica que un nodo no tiene predecesor
     */
    public static final int NO_PREDECESSOR = -1;
    
    /**
     * Método utilitario para formatear una distancia
     * @param distance La distancia a formatear
     * @return String con la representación de la distancia
     */
    public static String formatDistance(int distance) {
        return (distance == INFINITY) ? INFINITY_SYMBOL : String.valueOf(distance);
    }
    
    /**
     * Método utilitario para verificar si una distancia es infinita
     * @param distance La distancia a verificar
     * @return true si la distancia es infinita, false en caso contrario
     */
    public static boolean isInfinite(int distance) {
        return distance == INFINITY;
    }
}
