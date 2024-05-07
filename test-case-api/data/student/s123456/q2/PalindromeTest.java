import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;

public class PalindromeTest {
    public static void main(String[] args) {
        try {
            // Setup to read from standard input
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            String line = reader.readLine(); // Read one line of input

            // Parse the input line into an array of integers
            String[] stringNumbers = line.split(",\\s*");
            int[] numbers = new int[stringNumbers.length];
            for (int i = 0; i < stringNumbers.length; i++) {
                numbers[i] = Integer.parseInt(stringNumbers[i].trim());
            }

            // Create an instance of Palindrome and check the array
            Palindrome p = new Palindrome();
            boolean result = p.isPalindrome(numbers);

            // Print the result as 1 for true and 0 for false
            System.out.println(result ? "It is a palindrome" : "It is not a palindrome");

        } catch (Exception e) {
            // In case of any error during reading or processing, print an error code
            System.out.println("Error: " + e.getMessage());
        }
    }
}