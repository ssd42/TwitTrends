package sample;

/**
 * Created by Steven on 7/20/2017.
 */

public class ProcHandler {

    Process proc;

    // function checks wheather a certain process has terminated
    // this is so I can get the output values before displaying them on the UI
    public static boolean isProcDone(Process process){

        // if there is an exit value we know the process has completed
        try {
            process.exitValue();
            return true;
        } catch (Exception e) {

            return false;
        }
    }

//    public void waitTillDone(Process aproc){
//        try
//        aproc.waitFor();
//    }



}
