package schoolProject;

import java.util.Scanner;

public class calculator {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        Boolean d = true;
        while (true) {
            System.out.println("işlem yapmak istediğiniz iki sayıyı giriniz");
            double a = input.nextDouble();
            double b = input.nextDouble();
            System.out.println("işlem menüsü \n 1-toplama \n 2-çıkarma\n 3-çarpma\n 4-bölme");
            int islem = input.nextInt();
            if (islem == 1) {
                System.out.println("sayıların toplamı= " + (a + b));
            } else if (islem == 2) {
                System.out.println("sayıların farkı= " + (a - b));
            } else if (islem == 3) {
                System.out.println("sayıların çarpımı= " + (a * b));
            } else if (islem == 4) {
                System.out.println("sayıların oranı= " + (a / b));
            } else {
                System.out.println("yanlış tanımlı fonksiyon girdiniz tekrar deneyin");
                continue;
            }
            System.out.println("başka bir işlem yapmak istiyor musunuz? 1(evet) // 2(hayır)");
            int cevap = input.nextInt();
            if (cevap == 1) {
                continue;
            } else if (cevap == 2) {
                break;
            } else {
                System.out.println("yanlış cevap verdiniz tekrar deneyiniz");
                continue;
            }
        }
    }

}
