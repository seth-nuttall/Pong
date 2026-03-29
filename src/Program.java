import java.util.*;
import java.io.*;
import java.nio.*;
import java.math.*;

class Program {
    
    static int sumRange(int[] ints) {
        int sum = 0;
        // start at index 0 so the first element is included
        for (int i = 0; i < ints.length; i++) {
            int n = ints[i];
            // include only values between 10 and 100 inclusive
            if (n >= 10 && n <= 100) {
                sum += n;
            }
        }
        return sum;
    }

}
