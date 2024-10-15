public class Animal {
    private String foodType;
    private int lifeExpectancy;

    public Animal() {
        foodType = null;
        lifeExpectancy = 0;
    }

    public Animal(String food) {
        foodType = food;
        lifeExpectancy = 0;
    }

    public Animal(int life) {
        foodType = null;
        lifeExpectancy = life;
    }

    public Animal(String food, int life) {
        foodType = food;
        lifeExpectancy = life;
    }

    public String toString() {
        String result = "This ";
        if (foodType != null) result += foodType + " eater ";
        if (lifeExpectancy == 0)
            result += "lives for an unknown number of years.";
        else result += "typically lives for " + lifeExpectancy + " years.";

        return result;
    }

    public static void main(String[] args) {
        Animal animal1 = new Animal();
        Animal animal2 = new Animal(3);
        Animal animal3 = new Animal("grass");
        Animal animal4 = new Animal("meat", 10);

        System.out.println(animal1);
        System.out.println(animal2);
        System.out.println(animal3);
        System.out.println(animal4);
    }
}