public class Pet {
    private String cat;
    private String dog;



    public Pet() {
        this.cat = "";
        this.dog = "";
    }

    public Pet(String cat, String dog) {
        this.cat = cat;
        this.dog = dog;
    }

    public Pet(String breed) {
    }

    public Pet(String name, int age, String breed) {
    }

    public String getCat() {
        return cat;
    }

    public void setCat(String cat) {
        this.cat = cat;
    }

    public String getDog() {
        return dog;
    }

    public void setDog(String dog) {
        this.dog = dog;
    }
}