public class Dog extends Pet {
    private String name;
    private int age;
    private String breed;

    public Dog() {
        super();
        this.breed = "";
    }

    public Dog(String breed) {
        super(breed);
        this.breed = breed;
    }

    public Dog(String name, int age, String breed) {
        super(name, age, breed);
        this.name = name;
        this.age = age;
        this.breed = breed;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return this.age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getBreed() {
        return breed;
    }

    public void setBreed(String breed) {
        this.breed = breed;
    }

    public String toString() {
        return super.toString() + "  ";
    }

    public String speak() {
        return "Woof! I am " + name + ", a " + age + "yr old " + breed + ".";
    }
}