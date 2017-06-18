import java.util.ArrayList;
import java.util.Arrays;

public class JavaSum {

    public static void main(String[] args) {
        int param1 = Integer.parseInt(args[0]);
        String[] param2 = Arrays.copyOfRange(args, 1, args.length);
        ArrayList<Integer> arrayParam2 = new ArrayList<>();
        for(String s : param2) {
            arrayParam2.add(Integer.parseInt(s));
        }
        int sum = param1;
        for(Integer i : arrayParam2) {
            sum += i;
        }
        System.out.println(sum);
    }

}
