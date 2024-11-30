import java.util.Random;
import java.util.Arrays;

public class AListClient {

   public static void main(String[] args) {

      AListChain2 myList = new AListChain2();

      //int[] myList = new int[100];
      Random random = new Random();
      int[] randomValues = new int[10];
      int numSteps = 0;

      for (int i = 0; i < 100; i++) {
         myList.add(i + 1);
      }
      for (int i = 0; i < 10; i++) {
         randomValues[i] = random.nextInt(100) + 1;
      }
      //Arrays.sort(myList);

      System.out.println("\nList: " + Arrays.toString(myList.toArray()) + "\n");
      System.out.println("Random Values: " + Arrays.toString(randomValues) + "\n");


      for (int randomValue : randomValues) {
         myList.getNodeAt(randomValue);

         if (randomValue >= 1 && randomValue <= 50) {
            numSteps = randomValue - 1;
         }
         else {
            numSteps = 100 - randomValue;
         }

         System.out.println("getNodeAt(" + randomValue + ") returns " + randomValue + " in " + numSteps + " steps");
      }
   }
}