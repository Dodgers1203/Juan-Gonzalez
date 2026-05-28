import java.lang.Comparable;

public class Nodo<T extends Comparable<T>>{
    private T data;
    private Nodo<T> izquierdo;
    private Nodo<T> derecho;

    public Nodo(T data) {
        this.data = data;
    }

    public T getData() {
        return data;
    }
    public void setData(T data) {
        this.data = data;
    }

    public Nodo<T> getIzquierdo() {
        return izquierdo;
    }
    public void setIzquierdo(Nodo<T> izquierdo) {
        this.izquierdo = izquierdo;
    }

    public Nodo<T> getDerecho() {
        return derecho;
    }
    public void setDerecho(Nodo<T> derecho) {
        this.derecho = derecho;
    }
    
}
