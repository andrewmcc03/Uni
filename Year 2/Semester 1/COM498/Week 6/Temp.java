public class Temp {
    public static void main(String[] args) {
        int[] myArray = { 45, 13, 47, 28, 33 };
        int biggest = myArray[0];

        for (int i = 1; i < myArray.length; i++) {
            if (myArray[i] > biggest) {
                biggest = myArray[i];
            }
        }

        System.out.println("Biggest integer in myArray: " + biggest);
    }
}