public class RankedCards {
    public static void main(String[] args) {

        Card myCards[] = new Card[10];
        int biggestValue = -1, biggestPos = -1;
        Card tempCard;

        for (int i = 0; i < 10; i++) {
            myCards[i] = new Card();
            if (myCards[i].getRankValue() > biggestValue) {
                biggestValue = myCards[i].getRankValue();
                biggestPos = i;
            }
        }

        System.out.println("myCards are ... ");
        for (int i = 0; i < 10; i++) {
            System.out.println(myCards[i]);
        }
        System.out.println("\nBiggest rank value is at position " + biggestPos);

        // Now we do the swap...
        tempCard = myCards[9];
        myCards[9] = myCards[biggestPos];
        myCards[biggestPos] = tempCard;

        System.out.println("\nAfter swapping ... ");
        for (int i = 0; i < 10; i++) {
            System.out.println(myCards[i]);
        }
    }
}