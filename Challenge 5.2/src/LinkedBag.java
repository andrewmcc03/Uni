public final class LinkedBag<T> implements BagInterface<T> {
    private MyNode<T> firstNode;
    private int numberOfEntries;

    private MyNode<T> findEntry(T anEntry) {
        MyNode<T> currentNode = firstNode;
        boolean found = false;
        while (!found && currentNode != null) {
            if (currentNode.getData().equals(anEntry)) found = true;
            else currentNode = currentNode.getNext();
        }
        if (found) return currentNode; else return null;
    }

    public LinkedBag() {
        firstNode = null;
        numberOfEntries = 0;
    }

    public int getCurrentSize() {
        return 0;
    }


    public boolean isEmpty() {
        return (numberOfEntries == 0);
    }


    public boolean addNewEntry(T newEntry) {
        MyNode<T> newNode = new MyNode<T>(newEntry);
        newNode.setNext(firstNode);
        firstNode = newNode;
        numberOfEntries++;
        return true;
    }


    public T remove() {
        if (firstNode != null) {
            T result = firstNode.getData();
            firstNode = firstNode.getNext();
            numberOfEntries--;
            return result;
        }
        else return null;
    }

    public boolean remove (T anEntry) {
        MyNode<T> nodeToRemove = findEntry(anEntry);
        if (nodeToRemove == null) return false;
        nodeToRemove.setData(firstNode.getData());
        firstNode = firstNode.getNext();
        numberOfEntries--;
        return true;
    }


    public void clear() {
        firstNode = null;
        numberOfEntries = 0;
    }


    public int getFrequencyOf(T anEntry) {
        int count = 0;
        MyNode<T> currentNode = firstNode;
        while (currentNode != null) {
            if (currentNode.getData().equals(anEntry)) count++;
            currentNode = currentNode.getNext();
        }
        return count;
    }

    public boolean contains(T anEntry) {
        MyNode<T> currentNode = firstNode;
        boolean found = false;
        while (!found && currentNode != null) {
            if (currentNode.getData().equals(anEntry)) found = true;
            currentNode = currentNode.getNext();
        }
        return found;
    }


    public T[] toArray() {
        T[] resultArray = (T[]) new Object[numberOfEntries];
        int index = 0;
        MyNode<T> currentNode = firstNode;
        while (currentNode != null) {
            resultArray[index++] = currentNode.getData();
            currentNode = currentNode.getNext();
        }
        return resultArray;
    }

    public String toString() {
        MyNode<T> currentNode = firstNode;
        String result = "Bag [ ";
        while (currentNode != null) {
            result += currentNode.getData() + " ";
            currentNode = currentNode.getNext();
        }
        result += "]";
        return result;
    }
}