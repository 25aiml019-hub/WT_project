    import java.util.*;

    public class Main {



        
        public static void main(String[] args) {

            Scanner scanner = new Scanner(System.in);

            System.out.print("Enter a line: ");

            String line = scanner.nextLine();
        
          String[] s = line.split("");

          String longestWord = "";
          int maxLength = 0;

            for (int i = 0; i < s.length; i++) {
            
            if(s[i].length() > maxLength) {
                maxLength = s[i].length();
                longestWord = s[i];
 
            }

        }
        System.out.println("The longest word is: " + longestWord);
        System.out.println("The longest word is: " + maxLength);
    }
    }