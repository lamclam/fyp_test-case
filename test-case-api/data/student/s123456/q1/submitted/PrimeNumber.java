import java.util.Scanner;
public class PrimeNumber {
    public static void main(String[] args){
        Scanner scan = new Scanner(System.in);
        System.out.println("Please enter a number n");
        int n = scan.nextInt();
        int count = 0;
        if ( n < 0 ){
            System.out.println("Please enter a positive number");
            count++;
        }
        if (n==0||n==1){
            System.out.println(n+" is not prime number");   
            count++;
        } else if ( n > 2 && n % 2 == 0){
            System.out.println(n+" is not prime number");   
            count++;
        }
        else{
            for (int i=2;i<Math.sqrt(n);i++){     
                if ( n % i == 0){                
                    System.out.println(n + " is not a prime number.");               
                    count++;
                    break;
                }
            }
        }
        if ( n >= 0 && count == 0){
            System.out.println(n + " is a prime number.");
        }
    }
}