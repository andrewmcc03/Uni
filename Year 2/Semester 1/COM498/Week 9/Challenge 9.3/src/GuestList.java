import java.util.Arrays;
import java.util.Scanner;

public class GuestList {

    public static void displayArray(AListChain2<String> arr) {
        System.out.println("\n----------");
        System.out.println("Guest List");
        System.out.println("----------");

        // Need this to allow toArray to work with a String array as with this one
        Object[] guests = arr.toArray();
        String[] guestArray = Arrays.copyOf(guests, guests.length, String[].class); // PROBABLY INCORRECT WAY OF DOING THIS - SEE 9.2 SOLUTION NEXT WEEK

        Arrays.sort(guestArray);
        System.out.println(Arrays.toString(guestArray));
    }

    public static void main(String[] args) {

        AListChain2<String> myList = new AListChain2<>();
        Scanner input = new Scanner(System.in);

        boolean specialNameEntered = false;

        while (!specialNameEntered) {
            System.out.print("\nAdd a party guest: ");
            String name = input.nextLine();

            boolean showListEntered = false;

            while (!showListEntered) {
                if (myList.contains(name)) {
                    // Iterate over list to get index position
                    for (int i = 1; i <= myList.getLength(); i++) {
                        if (myList.getEntry(i).equals(name)) {
                            myList.remove(i);
                            break;
                        }
                    }

                    showListEntered = true;
                }
                else if (name.equals("ShowMeTheList")) {
                    displayArray(myList);

                    showListEntered = true;
                }
                else if (name.equals("xxx")) {
                    showListEntered = true;
                    specialNameEntered = true;
                }
                else {
                    myList.add(name);   // Add name if nothing else

                    showListEntered = true;
                }
            }
        }

        // Display final list after xxx/special name is entered
        displayArray(myList);
    }
}