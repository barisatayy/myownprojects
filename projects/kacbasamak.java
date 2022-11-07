package projects;

import java.util.Scanner;

public class kacbasamak {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("bir sayı giriniz");
        int k = input.nextInt();
        int r = 0;
        int t = 0;
        for (int i = 0; i < 3; i++) {
            t = k % 10;
            r += t;
            k = k / 10;

        }

        System.out.println(r);
    }

    private boolean charAt(int k) {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

}
