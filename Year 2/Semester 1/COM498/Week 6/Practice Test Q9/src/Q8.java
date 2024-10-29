public class Q8 {
    public static void testArray(char[] myLetter) {
        myLetter[2] = 'U';
        myLetter[3] = 'T';
        myLetter[4] = 'Q';
    }

    public static void main(String[] args) {
        char[] temp = { 'X', 'P', 'A', 'N', 'D' };

        System.out.print("START: \t");

        System.out.println(temp[1] + "*" + temp[2] + "*" + temp[3]);

            testArray(temp);

        System.out.print("END: \t");

        System.out.println(temp[1] + "*" + temp[2] + "*" + temp[3]);
    }
}