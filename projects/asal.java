package schoolProject;
import java.util.Scanner;
public class asal {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String alinanCevap;

        while(true){
        System.out.println("Bir Sayı Giriniz");
        int sayi = input.nextInt();
        boolean asal=true;
        for (int i = 2; i < sayi; i++) {
            if (sayi % i == 0) {
                asal = false;
                break;
                
            } else {
                asal = true;
            }    
        }
        if (asal && sayi!=1) {
            System.out.println("Sayınız Asal");
        } else {
            System.out.println("Sayınız Asal Değil");
        }

         System.out.println("devam etmek istiyor musunuz? evet/hayir");
         alinanCevap = input.next();
         if (alinanCevap.equals("evet")) {
                continue;
            }
         else if (alinanCevap.equals("hayir")){
                break;
            }
         
        
       
        
        }
    }
}
