
/**
 * Clase principal para demostrar el funcionamiento del Algoritmo de Dijkstra
 * 
 * El Algoritmo de Dijkstra es un algoritmo de búsqueda de camino más corto
 * que encuentra la distancia mínima desde un nodo origen a todos los demás nodos
 * en un grafo ponderado con pesos no negativos.
 * 
 * Complejidad temporal: O((V + E) * log V) donde V es el número de vértices y E el número de aristas
 * Complejidad espacial: O(V)
 */
public class App {
    public static void main(String[] args) {
        System.out.println("=== ALGORITMO DE DIJKSTRA - DEMOSTRACIÓN ===\n");
        
        // Ejemplo básico
        ejemploBasico();
        
        System.out.println("\n" + "=".repeat(60) + "\n");
        
        // Ejemplo complejo
        ejemploComplejo();
    }
    
    /**
     * Ejemplo básico del algoritmo de Dijkstra
     * Crea un grafo pequeño y muestra el funcionamiento paso a paso
     */
    private static void ejemploBasico() {
        System.out.println("EJEMPLO BÁSICO:");
        System.out.println("Creando un grafo con 5 nodos (0-4)...\n");
        
        // Crear un grafo con 5 nodos
        Graph graph = new Graph(5);
        
        // Agregar aristas (origen, destino, peso)
        graph.addEdge(0, 1, 4);  // 0 -> 1 con peso 4
        graph.addEdge(0, 2, 2);  // 0 -> 2 con peso 2
        graph.addEdge(1, 2, 1);  // 1 -> 2 con peso 1
        graph.addEdge(1, 3, 5);  // 1 -> 3 con peso 5
        graph.addEdge(2, 3, 8);  // 2 -> 3 con peso 8
        graph.addEdge(2, 4, 10); // 2 -> 4 con peso 10
        graph.addEdge(3, 4, 2);  // 3 -> 4 con peso 2
        
        // Mostrar el grafo
        graph.printGraph();
        System.out.println();
        
        // Crear instancia del algoritmo
        DijkstraAlgorithm dijkstra = new DijkstraAlgorithm(graph);
        
        // Ejecutar el algoritmo desde el nodo 0
        DijkstraResult result = dijkstra.dijkstra(0);
        
        // Mostrar los resultados
        result.printResults();
        
        // Ejemplo de búsqueda de camino específico
        System.out.println("BÚSQUEDA DE CAMINO ESPECÍFICO:");
        dijkstra.shortestPath(0, 4);
    }
    
    /**
     * Ejemplo más complejo del algoritmo de Dijkstra
     * Simula una red de ciudades con distancias
     */
    private static void ejemploComplejo() {
        System.out.println("EJEMPLO COMPLEJO - RED DE CIUDADES:");
        System.out.println("Simulando una red de 6 ciudades con distancias en kilómetros...\n");
        
        // Crear un grafo con 6 ciudades
        Graph cityNetwork = new Graph(6);
        
        // Nombres de las ciudades (solo para referencia)
        String[] cityNames = {"Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Zaragoza"};
        
        // Agregar conexiones bidireccionales (carreteras)
        cityNetwork.addBidirectionalEdge(0, 1, 621);  // Madrid - Barcelona
        cityNetwork.addBidirectionalEdge(0, 2, 357);  // Madrid - Valencia
        cityNetwork.addBidirectionalEdge(0, 3, 532);  // Madrid - Sevilla
        cityNetwork.addBidirectionalEdge(0, 4, 395);  // Madrid - Bilbao
        cityNetwork.addBidirectionalEdge(1, 4, 620);  // Barcelona - Bilbao
        cityNetwork.addBidirectionalEdge(1, 5, 296);  // Barcelona - Zaragoza
        cityNetwork.addBidirectionalEdge(2, 3, 652);  // Valencia - Sevilla
        cityNetwork.addBidirectionalEdge(4, 5, 324);  // Bilbao - Zaragoza
        cityNetwork.addBidirectionalEdge(0, 5, 325);  // Madrid - Zaragoza
        
        System.out.println("Red de ciudades:");
        for (int i = 0; i < 6; i++) {
            System.out.println(i + " = " + cityNames[i]);
        }
        System.out.println();
        
        // Ejecutar Dijkstra desde Madrid (nodo 0)
        DijkstraAlgorithm cityDijkstra = new DijkstraAlgorithm(cityNetwork);
        DijkstraResult cityResult = cityDijkstra.dijkstra(0);
        
        System.out.println("DISTANCIAS MÍNIMAS DESDE MADRID:");
        for (int i = 1; i < 6; i++) {
            if (cityResult.hasPathTo(i)) {
                System.out.println("A " + cityNames[i] + ": " + cityResult.getDistance(i) + " km");
                System.out.println("Ruta: " + getRouteWithNames(cityResult.getPath(i), cityNames));
                System.out.println();
            }
        }
        
        // Ejemplo específico: ruta más corta de Madrid a Barcelona
        System.out.println("RUTA OPTIMA MADRID A BARCELONA:");
        cityDijkstra.shortestPath(0, 1);
    }
    
    /**
     * Convierte un camino de números a nombres de ciudades
     * @param path Lista de nodos en el camino
     * @param names Array de nombres correspondientes
     * @return Cadena con los nombres de las ciudades
     */
    private static String getRouteWithNames(java.util.List<Integer> path, String[] names) {
        StringBuilder route = new StringBuilder();
        for (int i = 0; i < path.size(); i++) {
            route.append(names[path.get(i)]);
            if (i < path.size() - 1) {
                route.append(" -> ");
            }
        }
        return route.toString();
    }
}
