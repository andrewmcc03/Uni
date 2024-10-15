public class Cat extends Pet {
    private String name;
    private int age;
    private String breed;

    public Cat() {
        super();
        this.breed = "";
    }

    public Cat(String breed) {
        super(breed);
        this.breed = breed;
    }

    public Cat(String name, int age, String breed) {
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

    public String speak() {
        return "Meow! I am " + name + ", a " + age + "yr old " + breed + ".";
    }
}