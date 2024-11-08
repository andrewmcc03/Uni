public class Q8 {
//    public static void testArray(char[] myLetter) {
//        myLetter[2] = 'U';
//        myLetter[3] = 'T';
//        myLetter[4] = 'Q';
//    }
//
//    public static void main(String[] args) {
//        char[] temp = { 'X', 'P', 'A', 'N', 'D' };
//
//        System.out.print("START: \t");
//
//        System.out.println(temp[1] + "*" + temp[2] + "*" + temp[3]);
//
//            testArray(temp);
//
//        System.out.print("END: \t");
//
//        System.out.println(temp[1] + "*" + temp[2] + "*" + temp[3]);


    public static int doSomething(int[] arr, int val) {
        if (val >= arr.length) {
//            System.out.println("Val: " + val + " and " + arr.length);
            return 0;
        }
        else return arr[val] + doSomething(arr, val + 1);
    }

    public static void main(String args[]) {

        int[] newArr = {1,2,3,4};

        System.out.println(doSomething(newArr, 6));

    }
//        int[] myArray = {1, 2, 3, 6, 5, 4};
//
//        int position = 0;
//        int largest = myArray[0];
//
//        for (int i = 1; i < myArray.length; i++) {
//            if (myArray[i] > largest) {
//                largest = myArray[i];
//                position = i;
//            }
//        }
//
//        System.out.println("Largest: " + largest);
//        System.out.println("Index position of largest: " + position);
//
//    }


}