public class Queue<T> implements QueueInterface<T> {
    private MyNode<T> front, rear;

    public Queue() {
        front = null;
        rear = null;
    }

    public void enqueue(T newEntry) {
        MyNode<T> newNode = new MyNode<T>(newEntry);
        if (front == null) {
            front = newNode;
            rear = newNode;
        }
        else {
            rear.setNext(newNode);
            rear = newNode;
        }
    }

    public T dequeue() {
        if (front == null) return null;
        else {
            T valueToReturn = front.getData();
            front = front.getNext();
            if (front == null) rear = null;
            return valueToReturn;
        }
    }

    public T getFront() {
        if (front == null) return null;
        else return front.getData();
    }

    public boolean isEmpty() {
        return (front == null);
    }

    public void clear() {
        front = null;
        rear = null;
    }


    public static void main(String[] args) {
        Queue<String> queue = new Queue<String>();

        queue.enqueue("Milk");
        queue.enqueue("Eggs");
        queue.enqueue("Bread");

        for (int i = 1; i <= 4; i++) {
            System.out.println("Front   = " + queue.getFront());
            System.out.println("Dequeue = " + queue.dequeue() + "\n");
        }

        queue.enqueue("Cheese");
        queue.enqueue("Steak");
        queue.enqueue("Fish");

        System.out.println("\nQueue empty? " + queue.isEmpty());
        System.out.println("Clearing queue..."); queue.clear();
        System.out.println("Queue empty? " + queue.isEmpty());
    }
}