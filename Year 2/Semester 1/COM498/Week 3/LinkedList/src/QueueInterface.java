public interface QueueInterface<T> {
    public void enqueue(T newEntry);
    /* Add new entry to the back of the queue */

    public T dequeue();
    /* Remove entry from the front of the queue */

    public T getFront();
    /* Return, but DON'T REMOVE the entry from the front of the queue */

    public boolean isEmpty();
    /* Return true if the queue is empty, otherwise false */

    public void clear();
    /* Remove all entries from the queue */
}