package projects;

import java.util.Scanner;

public class yildizstun {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("karonun uzunluğu= ");
        int n = input.nextInt();
        for (int i = 1; i <= n; i++) {
            for (int j = i; j <= n; j++) {
                System.out.print(" ");
            }
            for (int k = 1; k <= i; k++) {
                System.out.print("O");
                System.out.print(" ");
            }
            System.out.println(" ");
        }
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i + 1; j++) {
                System.out.print(" ");
            }
            for (int j = i + 1; j <= n; j++) {
                System.out.print("O");
                System.out.print(" ");
            }
            System.out.println(" ");
        }
    }
}
