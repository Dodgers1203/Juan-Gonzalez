import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArbolBinario<Integer> arbol = new ArbolBinario<>();
        System.out.println("Ingrese números para el árbol binario (0 para terminar):");
        int valor;
        while (true) {
            System.out.print("Valor: ");
            valor = sc.nextInt();
            if (valor == 0) break;
            arbol.insertar(valor);
        }
        System.out.println("Recorrido inOrden:");
        arbol.imprimir();
        sc.close();
    }
}
