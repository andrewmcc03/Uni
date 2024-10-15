public class PetTest {
    public static void main(String[] args) {
        Cat c1 = new Cat("Pixel", 4, "tabby");
        Dog d1 = new Dog("Rex", 9, "terrier");

        System.out.println(c1.speak());
        System.out.println(d1.speak());
    }
}