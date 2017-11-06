package sample;
import javafx.scene.shape.Path;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Scanner;


public class FileManager {

    public FileManager(){
        String db_name = getFileName();
    }

    public  String getFileData(String filename) throws IOException{
        byte[] encoded = Files.readAllBytes(Paths.get(filename));
        return new String(encoded);
    }
    // may not be the best option but i can come back to it later (hashmap might be better for scaling)
    public static String typeToVal(String input){
//        int return_val = 0;
//        input = input.toLowerCase();

        if(input == "% of total"){
            return "2";
        }else if(input == "% of max"){
            return "3";
        }

        // otherwise just revert to the default
        return "1"; // "Score":"1"
    }
    public String getFileName(){
        return "temp name";
    }
}
