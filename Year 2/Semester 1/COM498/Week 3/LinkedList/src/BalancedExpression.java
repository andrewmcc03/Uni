import java.util.Scanner;

public class BalancedExpression {
    private static boolean isBalanced(String expression) {
        char nextChar, openDelimiter;
        Stack<Character> stack = new Stack<Character>();

        boolean isBalanced = true;
        while (isBalanced && expression.length() > 0) {
            nextChar = expression.charAt(0);
            switch (nextChar) {
                case '(':
                case '[':
                case '{': {
                    stack.push(nextChar);
                    break;
                }
                case ')':
                case ']':
                case '}': {
                    if (stack.isEmpty()) isBalanced = false;
                    else {
                        openDelimiter = stack.pop();
                        if (openDelimiter == '(' && nextChar != ')' ||
                            openDelimiter == '[' && nextChar != ']' ||
                            openDelimiter == '{' && nextChar != '}' ) {
                            isBalanced = false;
                        }
                    }
                    break;
                }
            }
            if (expression.length() > 1) expression = expression.substring(1);
            else expression = "";
        }
        if (!stack.isEmpty()) isBalanced = false;

        return isBalanced;
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter an expression (no spaces): ");
        String inputString = input.nextLine();
        System.out.print("\n" + inputString + " balanced? " + isBalanced(inputString) + "\n");

        // Enter: A+(B*{D-E}+F)-[I/J]
        //        A+(B+C)
        //        A+(B+C)+{D*E/F-[G+H]}
        //        A+(B+C}
    }
}