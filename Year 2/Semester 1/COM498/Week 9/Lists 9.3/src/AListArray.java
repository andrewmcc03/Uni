import java.util.Arrays;

public class AListArray<T> implements ListInterface<T> {

   private T[] list;
   private int numberOfEntries;
   private int capacity;
   private final int DEFAULT_SIZE = 100;


   private void addCapacity() {
      capacity += DEFAULT_SIZE;
      list = Arrays.copyOf(list, capacity + 1);
   }

   public AListArray() {
      T[] tempList = (T[]) new Object[DEFAULT_SIZE + 1];
      numberOfEntries = 0;
      list = tempList;
      capacity = DEFAULT_SIZE;
   }

   public void add(T newEntry) {
      if (numberOfEntries == capacity) {
         addCapacity();
      }

      numberOfEntries++;
      list[numberOfEntries] = newEntry;
   }

   public void add(int newPosition, T newEntry) {
      if (newPosition >= 1 && newPosition <= numberOfEntries + 1) {
         if (numberOfEntries == capacity) {
            addCapacity();
         }
         for (int i = numberOfEntries; i >= newPosition; i--) {
            list[i + 1] = list[i];
         }

         list[newPosition] = newEntry;
         numberOfEntries++;
      }
      else {
         throw new IndexOutOfBoundsException("New entry position is out of bounds.");
      }
   }

   public T remove(int position) {
      if (position >= 1 && position <= numberOfEntries) {
         T valueToReturn = list[position];

         for (int i = position; i < numberOfEntries; i++) {
            list[i] = list[i + 1];

         }
         numberOfEntries--;

         return valueToReturn;
      }
      else {
         throw new IndexOutOfBoundsException("Position to remove is out of bounds.");
      }
   }

   public void clear() {
      numberOfEntries = 0;
   }

   public T replace(int position, T newEntry) {
      if (position >= 1 && position <= numberOfEntries) {
         T valueToReturn = list[position];
         list[position] = newEntry;

         return valueToReturn;
      }
      else {
         throw new IndexOutOfBoundsException("Position to replace is out of bounds.");
      }
   }

   public T getEntry(int position) {
      if (position >= 1 && position <= numberOfEntries) {
         return list[position];
      }
      else {
         throw new IndexOutOfBoundsException("Requested position is out of bounds.");
      }
   }

   public T[] toArray() {
      T[] arr = (T[]) new Object[numberOfEntries];
      System.arraycopy(list, 1, arr, 0, numberOfEntries);

      return arr;
   }

   public boolean contains(T anEntry) {
      boolean found = false;
      int i = 1;

      while (i <= numberOfEntries && !found) {
         if (list[i++].equals(anEntry)) {
            found = true;
         }
      }
      return found;
   }

   public int getLength() {
      return numberOfEntries;
   }

   public boolean isEmpty() {
      return (numberOfEntries == 0);
   }
}