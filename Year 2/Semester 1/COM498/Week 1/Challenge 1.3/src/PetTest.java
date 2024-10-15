// PROGRAM BY ANDREW MCCORMICK
// Student ID: B00988875

import java.util.Scanner;
import java.util.Random;
import java.util.ArrayList;

public class PetTest {
    public static void main(String[] args) {
        // Initialise Scanner for input and Random
        Scanner input = new Scanner(System.in);
        Random rdm = new Random();

        // Create arrays for cat and dog breeds to be assigned later
        String[] catBreeds = {"tabby", "siamese", "persian", "bengal", "burmese"};
        String[] dogBreeds = {"terrier", "beagle", "pug", "bulldog", "labrador"};

        // Array for storing the pets
        ArrayList<Pet> Pets = new ArrayList<>();
        int numCats = 0;
        int numDogs = 0;

        // For loop to prompt and store pets
        for (int i = 0; i < 5; i++) {
            System.out.println("Would you like to add a Cat or a Dog to the list? ");
            String petType = input.nextLine();

            System.out.println("Please enter it's name: ");
            String name = input.nextLine();

            // Randomise the age of each pet within a realistic age
            int age = rdm.nextInt(15) + 1;

            // If statement to determine if it's a cat or dog - ignores case
            if (petType.equalsIgnoreCase("Cat")) {
                String breed = catBreeds[rdm.nextInt(catBreeds.length)];
                Pets.add(new Cat(name, age, breed));

                // Increment number of cats in the array
                numCats++;
            } else if (petType.equalsIgnoreCase("Dog")) {
                String breed = dogBreeds[rdm.nextInt(dogBreeds.length)];
                Pets.add(new Dog(name, age, breed));

                // Increment number of dogs in the array
                numDogs++;
            } else {
                System.out.println("Invalid. Please enter either 'Dog' or 'Cat'.");

                // Decrement the index
                i--;
            }
        }

        // Output total num of cats and dogs
        System.out.println("\nThere are a total of " + numCats + " cats and " + numDogs + " dogs.");

        // While loop - while the user continues to enter a valid cat or dog name, the program will continue. Otherwise, it will display that it doesn't know a cat/dog by that name
        while (true) {
            System.out.println("\nWhich cat/dog would you like to speak next? (Type 'exit' to quit)");
            String searchName = input.nextLine().trim();

            // Exit the loop if the user types 'exit'
            if (searchName.equalsIgnoreCase("exit")) {
                System.out.println("Exiting program...");
                break;
            }

            // Variable to check if the pet is found
            boolean petFound = false;

            // Search for the pet by name in the Pets list
            for (Pet pet : Pets) {
                if (pet instanceof Cat && ((Cat) pet).getName().equalsIgnoreCase(searchName)) {
                    System.out.println("Pet found: " + ((Cat) pet).speak());
                    petFound = true;
                    break;
                } else if (pet instanceof Dog && ((Dog) pet).getName().equalsIgnoreCase(searchName)) {
                    System.out.println("Pet found: " + ((Dog) pet).speak());
                    petFound = true;
                    break;
                }
            }

            // If the pet is not found, display a suitable message
            if (!petFound) {
                System.out.println("I don't know a cat/dog by the name " + searchName + ".");
            }
        }

        // Close scanner
        input.close();
    }
}