// PROGRAM BY ANDREW MCCORMICK
// Student ID: B00988875

import java.util.Scanner;

/**
 * Lab Session 2
 * LongestCommonSubsequence class is a program that will determine the longest string
 * that is a subsequence of two stings input by the user (in the command line).
 * The program applies a brute force solution to finding the subsequence.
 *  Uses the ArrayBag class for the Bag implementation.
 */

public class LongestCommonSubsequence {
    public static void main(String args[]) {
        String strBestSubsequence;

        Scanner input;
        input = new Scanner(System.in);

        System.out.println("-------------------------------------------------------------------------------------");
        System.out.println("This program determines the longest string that is a subsequence of two input strings.");
        System.out.print("Please enter the first string: ");
        String strFirst = input.next();

        System.out.print("Please enter the second string: ");
        String strSecond = input.next();
        System.out.println("\n");

        // (Done) TODO (2): Add code to create an instance of the Bag (ArrayBag) then add the initial (first) string:
        BagInterface<String> testBag = new ArrayBag<>();
        testBag.addNewEntry(strFirst);

        // Print out the current contents of the bag:
        System.out.println("The strings to check are: " + testBag);

        // Assign the empty string to the longest match subsequence:
        strBestSubsequence = new String("");

        // Loop to check the strings in the Bag:
        while (testBag.getCurrentSize() > 0) {

            // (Done) TODO (3): Remove a test string from the bag: (modify the line below this one)
            String strTest = testBag.remove();
            System.out.println("Now checking: " + strTest);

            // Check if strTest is a subsequence of strSecond
            if (isSubsequence(strTest, strSecond)) {
                System.out.println(strTest + " is a subsequence of " + strSecond + ".");

                // If the subsequence is longer than the current best subsequence > update it
                if (strTest.length() > strBestSubsequence.length()) {
                    strBestSubsequence = strTest;
                    //System.out.println("Found " + strBestSubsequence + " for the longest common subsequence");
                }
            }
            else {
                System.out.println(strTest + " is NOT a subsequence of " + strSecond + ".");
            }

//            for (int i = 0; i < strTest.length(); i++) {
//                String strNew = strTest.substring(0, i) + strTest.substring(i + 1); // Remove character at position 'i'
//                // If strNew is NOT empty AND the testBag DOES NOT contain strNew - avoids adding empty/duplicate strings
//                if (!strNew.isEmpty() && !testBag.contains(strNew)) {
//                    testBag.addNewEntry(strNew);
//                    //System.out.println("Adding new string to the bag: " + strNew);
//                }
//            }

            // If longest match is shorter than test string:
            if (strTest.length() > strBestSubsequence.length()) {
                if (isSubsequence(strTest, strSecond) /* (Done) TODO (4): Change this line to test if the string is a subsequence of the second string */) {
                    // (Done) TODO (4): If it is a subsequence, then set the longest match to the test string
                    //                  by adding a line of code immediately below this one
                    strBestSubsequence = strTest;

                    System.out.println("Found a subsequence: " + strBestSubsequence);
                }
                else {
                    // If the test string is at least two longer than the longest match:
                    if (strTest.length() - 1 > strBestSubsequence.length()) {
                        // TODO (5): Generate new strings from test by removing each single character and
                        //           place each new string in the bag. Add the new code into this 'if' block
                        for (int i = 0; i < strTest.length(); i++) {
                            String strNew = strTest.substring(0, i) + strTest.substring(i + 1); // Remove character at position 'i'
                            // If strNew is NOT empty AND the testBag DOES NOT contain strNew - avoids adding empty/duplicate strings
                            if (!strNew.isEmpty() && !testBag.contains(strNew)) {
                                testBag.addNewEntry(strNew);    // Add newly generated strings
                            }
                        }
                    }
                }
            }

            // Print the bag of strings to check:
            System.out.println("The bag of new strings to check is now: " + testBag);
            System.out.println("Size: " + testBag.getCurrentSize());
            System.out.println();

        }

        // Print the longest match:
        System.out.println("Found " + strBestSubsequence + " for the longest common subsequence.");
        System.out.println("-------------------------------------------------------------------------------------");

    }

    /**
     * Method to determine if one string is a subsequence of the other.
     * @param strCheck See if this is a subsequence of the other argument.
     * @param strAgainst The string to check against.
     * @return     A boolean if check is a subsequence of other.
     */
    public static boolean isSubsequence(String strCheck, String strAgainst) {

        boolean bResult = false;

        // Check if a subsequence exists
        // Only check if it is no longer than the against string:
        if (strCheck.length() <= strAgainst.length()) {
            int i = 0;
            for (int j = 0; i < strCheck.length() && j < strAgainst.length(); j++) {
                if (strCheck.charAt(i) == strAgainst.charAt(j)) {
                    i++;
                }
            }
            bResult = (i == strCheck.length());
        }
        return bResult;
    }
}