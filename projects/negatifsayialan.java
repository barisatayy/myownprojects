package schoolProject;
import java.util.Scanner;

public class negatifsayialan {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int k = 0;
        while (true) {
            System.out.println("bir sayı girin");
            int n = input.nextInt();
            if (n > 0) {
                if (n % 2 != 0) {
                    k = k + n;
                }
            } else {
                break;
            }
        }
        System.out.println("pozitif tek sayıların toplamı = " + k);
    }
}
