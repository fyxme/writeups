![](https://i.imgur.com/OgDknej.png)


> [50 points]
> BowShock
> Can you find out how to minimize bow shock and prevent everything from turning into dust?

We are provided with a jar file and the challenge is a reversing challenge. 

My goto tool for reversing jar files to java source code is jd-gui. Its a great tool which does the job well and is super simple to use (no overly complicated navbar with 1000s of buttons).

Decompiling the provided jar yields the following source code:
![](https://i.imgur.com/w5LdmJV.png)


```
import java.util.InputMismatchException;
import java.util.Scanner;

class BowShock {
  public static int totalInput;
  
  public static int getInput() {
    int i;
    System.out.println("Set the amount of plasma to the correct amount to minimize bow shock: ");
    Scanner scanner = new Scanner(System.in);
    while (true) {
      try {
        i = scanner.nextInt();
        break;
      } catch (InputMismatchException inputMismatchException) {
        System.out.print("Invalid input. Please reenter: ");
        scanner.nextLine();
      } 
    } 
    totalInput += i;
    return i;
  }
  
  public static void bowShock() {
    System.out.println("And all was dust in the wind.");
    System.exit(-99);
  }
  
  public static void main(String[] paramArrayOfString) {
    System.out.println("Oh damn, so much magnetosphere around here!");
    if (getInput() != 333)
      bowShock(); 
    System.out.println("We survive another day!");
    if (getInput() != 942)
      bowShock(); 
    if (getInput() != 142)
      bowShock(); 
    System.out.println("Victory!");
    System.out.println("CTF{bowsh0ckd_" + totalInput + "}");
  }
}
```

Sometimes when reversing its easier to go backwords.

We see that the flag is printed at the end:
```
System.out.println("CTF{bowsh0ckd_" + totalInput + "}");
```

We have part of the flag but we're missing totalInput so we need to figure what that is.

The name does give us some details as to what totalInput might be (ie. the sum of all inputs aka the total).

This is confirmed by looking at the `getInput()` function which takes user input using `Scanner scanner = new Scanner(System.in);`, convert that input to an integer `i = scanner.nextInt();` and then adds that to the totalInput variable `totalInput += i;`.

Now we need to figure out what input we need to give in order to get the correct total. In the main function, we can see that the application is checking if the return value is equal to specific numbers:
```
if (getInput() != 333)
if (getInput() != 942)
if (getInput() != 142)
```
and if the value returned is not equal to those than the `bowshock()` function is called and forces the program to stop via `System.exit(-99);`.

With those numbers we can now calculate the expected value of `totalInput` using the following python code:
```
print(333+942+142)
```
Combining this with the other parts of the flag gives us the following python script we can use to get the flag:
```
print("CTF{{bowsh0ckd_{}}}".format(333+942+142))
# CTF{bowsh0ckd_1417}
```

> Flag: CTF{bowsh0ckd_1417}