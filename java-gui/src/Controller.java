package sample;
import sample.FileManager;
import sample.ProcHandler;

import com.sun.xml.internal.ws.policy.privateutil.PolicyUtils;
import javafx.collections.FXCollections;
import javafx.scene.control.cell.ChoiceBoxListCell;
import javafx.scene.control.cell.PropertyValueFactory;
import sample.Entry;

import javafx.fxml.FXML;
import javafx.scene.control.*;

import java.util.concurrent.TimeUnit;

import java.io.IOException;
import java.util.ArrayList;


public class Controller {

    public boolean production = true;

    public String keyword;
    public String db_name;


    public ArrayList<Process> processAL;
    Process proc;
    Process tempProc;

    public String jar_loc = getJarPath();
    public String python_exe = jar_loc.substring(0, jar_loc.lastIndexOf('/')) + "/Scripts/python.exe";
    public String streamtweets_loc = jar_loc + "TwitStream/streamtweets.py";
    public String main_loc = jar_loc + "TwitStream/main.py";

    String datatxt = "output_main.txt";


    // Buttons from the UI that will be used in this controller
    // Other controllers may be implemented later on

    @FXML
    public Button startstream;
    public Button killstream;
    public Button grabdata;
    public TextField keywordtxt;
    public TextArea output_area;
    public ChoiceBox display_choice;




    @FXML
    public void initialize(){


        System.out.println(python_exe);

        String intro = "Before going on and using this program please read the README.txt" +
                " file for instructions on how to handle this software optimally\n";



        // inserting the choices for  the button (hard code cause might be easier to change later on)
        display_choice.setItems(FXCollections.observableArrayList("Score", "% of total", "% of max"));

        //testing to see what i can get from the multi asker
        String data = display_choice.getSelectionModel().getSelectedItem().toString();
//        output_area.setText(data + '\n');
        output_area.setText(intro);
        output_area.setStyle("-fx-text-fill: red;");

//        output_area.appendText(python_exe);
    }



    @FXML
    public void startStream() throws InterruptedException {

        keyword = keywordtxt.getText().trim().toLowerCase();

        if(keyword.isEmpty()){
            output_area.setText("No input provided stream did not start");
        }
        else {

            // get the name of the file we're saving //
            db_name = assignDBname(keyword.toLowerCase());

            System.out.println(keyword);
            System.out.println(db_name);
//        String final_command = genCommand("py", getJarPath()+"main.py", keyword);

            String main = "C:/Users/Steven/IdeaProjects/HolyTrends/src/sample/main.py";
            String other = getJarPath() + "main.py";
            String py = "/C:/Python35/python.exe/";
//        String final_command = genCommand(py, other, keyword);

            String cmd;
            if(production) {
                cmd = String.format("%s streamtweets.py %s", python_exe,keyword);
            }else{
                cmd = String.format("py main.py %s", keyword);
            }

            // Initiate given the current parameters
            StartProcess(cmd);
        }
    }

    // only for the twitter stream process
    @FXML
    public void killStream(){

        proc.destroy();
        output_area.setStyle("-fx-text-fill: red;");
        output_area.appendText("\nCurrent stream has stopped");
    }


    // just a waiting mechanism for giving the user a heads up that the data is being parsed
    @FXML
    public void printwait(){
        output_area.setStyle("-fx-text-fill: #ff3333;");
        output_area.setText("Waiting while reading data this can take a while");
    }

    // ok so here i need to start a process like main and wait for it to die
    // once that is over I can load in the data from the text file it will output

    @FXML
    public void grabdata(){

        // why do i complicate this, fix later ALERT!!!!!!!!!!!!!!!1
        FileManager fm = new FileManager();


        keyword = keywordtxt.getText().trim().toLowerCase();
        String method = display_choice.getSelectionModel().getSelectedItem().toString();
        System.out.println(method);
        String value = fm.typeToVal(method);

        if(keyword.isEmpty()){output_area.setText("PLEASE INSERT A KEYWORD TO GET THE RIGHT SEARCH " +
                "\nYou might need to start a stream to search get data on a new keyword");}
        else {

            String command_main;

            if(production==true){
                command_main = String.format("%s main.py %s %s", python_exe,keyword, value);
            }else {
                command_main = String.format("py main.py %s %s", keyword, value);
            }
            System.out.println(command_main);

            try {
                tempProc = Runtime.getRuntime().exec(command_main);
            } catch (IOException ioEx) {
                System.out.println("Could not find main to run");
                ioEx.printStackTrace();
                output_area.setText("An Error has occured: " + ioEx);
            }


            // THIS IS THE WAIT CODE
            // wait for the main file to be completed so init should be before this comment
            boolean isDone = false;
            while (!isDone) {
                isDone = ProcHandler.isProcDone(tempProc);
            }

            System.out.println("done with proc");

            // This is the portion that will now go to the text file and grab the data and display it as is in the UI
            // The data here are strings and will be dificult to parse in mass, rewrite the python code later

            try {
                String plotdata;
                if (production) {
                    plotdata = fm.getFileData(datatxt);
                }else {
                    plotdata = fm.getFileData("data.txt");
                }
                output_area.setStyle("-fx-text-fill: black;");
                output_area.setText(plotdata);
            } catch (IOException ioEX) {
                output_area.appendText("\nERROR: Something has occured for the data to not be readable, corruption possible. Contact Dev.");
            }
        }
    }


//    public String genCommand(String command, String filename, String cmd_args){ return command+' '+filename+' '+cmd_args; }

    public void StartProcess(String instructions) throws InterruptedException {

//        Initialization info to keep the user aware

//        output_area.setText("Attempting to init process\n");
        output_area.setText("\nProcess initializing...\n");
        output_area.setStyle("-fx-text-fill: red;");
//        for(String inst: instructions){
//            output_area.appendText(inst + " ");
//        }
//        output_area.appendText(instructions); // for now I think its functional so it should be good

        try{
            proc = Runtime.getRuntime().exec(instructions);
        }catch(IOException ioEx){
            ioEx.printStackTrace();
            output_area.setText("An Error has occured: " + ioEx);
        }

        boolean isDone = false;

//        while(!isDone){
//            isDone = ProcHandler.isProcDone(proc);
////            Thread.sleep(1000);
//        }

        if(ProcHandler.isProcDone(proc)){
            System.out.println("Processdone");
        }
        else{
            System.out.println("Done");
        }

    }

    // BASIC FUNCTIONS THAT NEED CLEANING UP LATER

    private String assignDBname(String name){
        return name + ".txt";
    }

    // get the location of the current jar file to allow everything to be moved
    private String getJarPath(){
        return getClass().getProtectionDomain().getCodeSource().getLocation().getPath();
    }

}

