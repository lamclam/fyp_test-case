import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class PalindromeTest {
    public static void main(String[] args) {
        Palindrome p = new Palindrome();

        int[][] cases = {
			    {1, 3, 3, 1}, // Case1
                {1, 2, 3, 2, 1}, // Case2
                {3, 3}, // Case3
                {2}, // Case4
                {1, 1, 3, 3, 1}, // Case5
                {1, 3, 3, 1, 1}, // Case6
                {1, 1, 4, 6, 4, 1}, // Case7
                {1, 4, 6, 4, 1, 1}, // Case8
                {1, 2, 3, 4, 2, 1}, // Case9
                {1, 3, 5, 7, 6, 3, 1}, // Case10
                {1, 3, 4, 4, 3, 2}, // Case11
                {1, 3, 4, 5, 4, 3, 2}, // Case12
                {1, 2, 4, 4, 3, 2}, // Case13
                {2, 1, 3, 4, 1, 1}, // Case14
                {7, 7, 7, 7, 7, 7, 7}, // Case15
                {8, 8, 8, 8, 8, 8} // Case16
        };

        // Save the old System.out
        PrintStream old = System.out;

        // Prepare the output array as a StringBuilder
        StringBuilder output = new StringBuilder();
        output.append("[");

        for (int i = 0; i < cases.length; i++) {
            try {
                // Redirect output to a dummy PrintStream
                System.setOut(new PrintStream(new ByteArrayOutputStream()));

                boolean result = p.isPalindrome(cases[i]); // Call the method without printing
                                                           // anything

                // Restore the original System.out
                System.setOut(old);

                // Append the result to 'output'
                output.append(result ? "1" : "0");
            } catch (Exception e) {
                // Restore the original System.out in case of an error
                System.setOut(old);

                // Append '2' to 'output' if there is an error
                output.append("2");
            }

            // Append a comma if it's not the last element
            if (i < cases.length - 1) {
                output.append(", ");
            }
        }

        output.append("]");
        System.out.println(output.toString()); // Print the final output
    }
}
