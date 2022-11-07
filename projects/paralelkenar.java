package projects;

import java.util.Scanner;

public class paralelkenar {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("paralel kenarın uzunluğunu giriniz= ");
        int n = input.nextInt();
        System.out.print("paralel kenarın yüksekliği giriniz= ");
        int b = input.nextInt();
        for (int i = 1; i <= b; i++) {
            for (int j = i; j <= b-1; j++) {
                System.out.print(" ");
            }
            for (int k = 1; k <= n; k++) {
                System.out.print("*");

            }
            System.out.print("\n");
        }
    }
}
