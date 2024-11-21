/*
adım1: başla
adım2: kullanıcıdan a sayısı al
adım3: fakt=1 değerini ata
adım4: for değeri için f değerini 2'ye ata, f a'ya kadar olsun ve birer birer artsın
adım5: fakt=fakt*f;
adım6: faktöriyel değerini yazdır
adım7: bitir
 */
package schoolProject;

import java.util.Scanner;

public class faktoriyel {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("bir sayıyı giriniz");
        int a = input.nextInt();
        int fakt = 1;
        for (int f = 2; f <= a; f++) {
            fakt = fakt * f;
        }
        System.out.println("Sayının faktöriyeli= " + fakt);

    }

}
