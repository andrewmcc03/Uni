public class TestAnimal {
    public static void main(String[] args) {
        Lion lion1 = new Lion("Leo", 3, "vegetation", 10);
        Lion lion2 = new Lion();

        System.out.println(lion1.toString());
        System.out.println(lion2.toString());
        System.out.println(Lion.getNumOfLions());
    }
}