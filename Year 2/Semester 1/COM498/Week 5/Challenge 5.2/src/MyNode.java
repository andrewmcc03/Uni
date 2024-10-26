public class MyNode<T> {
    private T data;
    private MyNode<T> next;

    public MyNode(T dataValue) {
        data = dataValue;
        next = null;
    }

    public T getData() {
        return data;
    }

    public void setData(T dataValue) {
        data = dataValue;
    }

    public MyNode<T> getNext() {
        return next;
    }

    public void setNext(MyNode<T> nextNode) {
        next = nextNode;
    }

    public static void main(String[] args) {
        MyNode<Integer> node1 = new MyNode<Integer>(1);
        MyNode<Integer> node2 = new MyNode<Integer>(2);
        MyNode<Integer> node3 = new MyNode<Integer>(3);

        node1.setNext(node2);
        node2.setNext(node3);

        System.out.println("Value of node1: " + node1.getData());
        System.out.println("Value of node2: " + node1.getNext().getData());
        System.out.println("Value of node3: " + node1.getNext().getNext().getData());
    }
}