import java.lang.Comparable;

public class ArbolBinario<T extends Comparable<T>> {
    private Nodo<T> raiz;

    public ArbolBinario() {
    }

    public boolean isEmpty(){
        return this.raiz == null;
    }
    public boolean exists(T valor){
        return buscar(valor) != null;
    }
    public void insertar(T data){
        if (isEmpty()){
            this.raiz = new Nodo<>(data);
            return;
        }
        insertar(this.raiz, new Nodo<T>(data));
    }

    public void insertar(Nodo<T> raiz, Nodo<T> hijo) {
       if(hijo.getData().compareTo(raiz.getData()) < 0){
            if(raiz.getIzquierdo() == null){
                raiz.setIzquierdo(hijo);
            } else {
                insertar(raiz.getIzquierdo(), hijo);
            }
       } else {
            if(raiz.getDerecho() == null){
                raiz.setDerecho(hijo);
            } else {
                insertar(raiz.getDerecho(), hijo);
            }
       }
    }

    public T buscar(T seeked) {
       return buscar(this.raiz, seeked);
    }

    private T buscar(Nodo<T> nodo, T seeked) {
       if(nodo == null) return null;
       if(nodo.getData().equals(seeked)) return nodo.getData();
       if(seeked.compareTo(nodo.getData()) < 0) {
           return buscar(nodo.getIzquierdo(), seeked);
       } else {
           return buscar(nodo.getDerecho(), seeked);
       }
    }
    public void imprimir(){
        if(!isEmpty()){
            imprimir(this.raiz);
        }
    }

    private void imprimir(Nodo<T> nodo) {
        if(nodo == null){
            return;
        }
        imprimir(nodo.getIzquierdo());
        System.out.println(nodo.getData().toString());
        imprimir(nodo.getDerecho());
    }
}

