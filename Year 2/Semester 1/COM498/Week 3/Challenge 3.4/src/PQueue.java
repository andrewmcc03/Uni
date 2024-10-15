import java.util.Arrays;
import java.util.Random;

public class PQueue<T extends Comparable<T>> implements PQueueInterface<T> {
    private MyNode<T> front;

    public PQueue() {
        front = null;
    }

    public void enqueue(T newEntry) {
        MyNode<T> newNode = new MyNode<T>(newEntry);
        if (front == null) {
            front = newNode;
        }
        else if (front.getData().compareTo(newEntry) < 0) {
            newNode.setNext(front);
            front = newNode;
        }
        else {
            MyNode<T> currentNode = front;
            while (currentNode.getNext() != null && currentNode.getNext().getData().compareTo(newEntry) > 0) {
                currentNode = currentNode.getNext();
            }
            newNode.setNext(currentNode.getNext());
            currentNode.setNext(newNode);
        }
    }

    public T dequeue() {
        if (front == null) {
            return null;
        }
        else {
            T valueToReturn = front.getData();
            front = front.getNext();
            return valueToReturn;
        }
    }

    public T getFront() {
        if (front == null) {
            return null;
        }
        else {
            return front.getData();
        }
    }

    public boolean isEmpty() {
        return front == null;
    }

    public void clear() {
        front = null;
    }


    public static void main(String[] args) {
        PQueue<Integer> pQueue = new PQueue<Integer>();
        Random rdm = new Random();
        Integer[] randomValues = new Integer[10];

        // For loop to get 10 random values and queue them
        for (int i = 0; i < randomValues.length; i++) {
            randomValues[i] = rdm.nextInt(1000);
            pQueue.enqueue(randomValues[i]);
        }

        // Output array (unordered)
        System.out.println("Random array is: " + Arrays.toString(randomValues) + "\n");

        // Loop to dequeue all items until empty - dequeues in order (highest to lowest)
        while (!pQueue.isEmpty()) {
            System.out.println("Removing value " + pQueue.dequeue());
        }

        if (pQueue.isEmpty()) {
            System.out.println("\nQueue is empty...");
        }
    }
}