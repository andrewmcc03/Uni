import java.util.Scanner;

public class Infix2Postfix {

    // 1. Infix to Postfix (Infix2Postfix)

    private static int precedence(char operator) {
        switch (operator) {
            case '^' : return 3;
            case '*': case '/' : return 2;
            case '+' : case '-' : return 1;
        }
        return 0;
    }
    
    public static String infixToPostfix(String infix)
    {
        // 1.1. Initialising empty String for result
        String result = new String("");

        //    Initialising empty stack
        Stack<Character> stack = new Stack<Character>();

        // 1.2. Iterate across each character in the infix string
        for (int i = 0; i < infix.length(); i++)
        {
            char nextChar = infix.charAt(i);

            // 1.3. If the scanned character is an operand (number), add it to output.
            if (Character.isDigit(nextChar))
                result = result + nextChar;

                // 1.5. If the scanned character is an '(', push it to the stack.
            else if (nextChar == '(')
                stack.push(nextChar);

                // 1.6. If the scanned character is an ')', pop and output from the stack until an '(' is encountered.
            else if (nextChar == ')')
            {
                while (stack.peek() != '(')
                    result = result + stack.pop();

                stack.pop(); // 1.6. Get rid of the '(' that is now on top of the stack
            }
            // 1.4.2 Operator encountered
            else {
                // 1.4.2 Add to the output, every operator on the stack with a precedence greater than or equal to the precedence of the operator found
                while (!stack.isEmpty() && precedence(nextChar) <= precedence(stack.peek())){
                    result = result + stack.pop();
                }
                stack.push(nextChar);
            }
        }

        // 1.8. Pop all operators from the stack while stack is not empty
        while (!stack.isEmpty()){
            result = result + stack.pop();
        }
        return result;
    }

    // 2. Evaluating Postfix

    static int evaluatePostfix(String postfix)
    {
        // 2.1. Create a stack
        Stack<Integer> stack = new Stack<Integer>();

        // 2.2. Scan all characters one by one
        for (int i = 0; i <postfix.length(); i++)
        {
            char nextChar = postfix.charAt(i);

            // 2.2.1. If the scanned character is an operand (number here), push it to the stack.
            if (Character.isDigit(nextChar)) stack.push(nextChar - '0'); // Convert the character into the equivalent integer

                // 2.2.2. If the scanned character is an operator, pop 2 elements from stack apply the operator
            else {
                int value1 = stack.pop();
                int value2 = stack.pop();

                switch(nextChar)
                {
                    case '+':
                        stack.push(value2 + value1);
                        break;
                    case '-':
                        stack.push(value2 - value1);
                        break;
                    case '/':
                        stack.push(value2 / value1);
                        break;
                    case '*':
                        stack.push(value2 * value1);
                        break;
                    case '^':
                        stack.push((int)Math.pow(value2, value1));
                        break;
                }
            }
        }
        return stack.pop(); // 2.3. When the expression has ended, the number in the stack is the final answer
    }


    // Test input and output with valid/invalid expressions
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.print("Enter an infix expression (no spaces): ");
        String infix = input.nextLine();

        System.out.println("\nPostfix is:   " + infixToPostfix(infix));
        System.out.println("Result is:    " + evaluatePostfix(infixToPostfix(infix)));
    }
}