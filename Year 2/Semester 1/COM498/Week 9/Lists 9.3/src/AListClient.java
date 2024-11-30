import java.util.Arrays;

public class AListClient {

   public static void main(String[] args) {

      // USING CHAIN LIST THIS TIME - AListChain or AListChain2
      AListChain2 myList = new AListChain2();

      myList.add(1);
      myList.add(2);
      myList.add(3);
      myList.add(2, 4);

      System.out.println("\nList should be: 1, 4, 2, 3");
      System.out.println(Arrays.toString(myList.toArray()));

      myList.remove(2);

      System.out.println("\nList should be: 1, 2, 3");
      System.out.println(Arrays.toString(myList.toArray()));

      myList.replace(2, 22);

      System.out.println("\nList should be: 1, 22, 3");
      System.out.println(Arrays.toString(myList.toArray()));

      ////

      int value = (int) myList.getEntry(3);
      System.out.println("\nValue retrieved is: " + value);

      System.out.println("\nList of " + myList.getLength() + " elements contains 22 is " + myList.contains(22));
      System.out.println("List of " + myList.getLength() + " elements contains 2 is " + myList.contains(2));

      System.out.println("\nIs the list empty? " + myList.isEmpty());

      myList.clear();
      System.out.println("\nList cleared.");

      System.out.println("\nIs the list empty now? " + myList.isEmpty());

      for (int i = 1; i <= 250; i++) {
         myList.add(i);
      }
      System.out.println(Arrays.toString(myList.toArray()));
   }
}