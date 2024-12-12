public class MyNode<T> {

    private T data;
    private MyNode<T> next;

    public MyNode(T dataValue) {
        data = dataValue;
        next = null;
    }

    public MyNode<T> getNextNode() {
        return next;
    }

    public T getData() {
        return data;
    }

    public void setData(T dataValue) {
        data = dataValue;
    }

    public void setNextNode(MyNode<T> nextNode) {
        next = nextNode;
    }
}