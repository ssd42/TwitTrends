package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;

public class Main extends Application {

    boolean DEBUG = true;

    @Override
    public void start(Stage primaryStage) throws Exception{
        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        primaryStage.setTitle("Twitter Trends");
        primaryStage.setScene(new Scene(root, 600, 600));

        Image icon;
        if(DEBUG) {
            icon = new Image(getClass().getResourceAsStream("icon.png"));
        }else{
             icon = new Image(getClass().getResourceAsStream("staticdata/icon.png"));

        }
//        primaryStage.getIcons().add(new Image("C:\\Users\\Steven\\IdeaProjects\\HolyTrends\\icon.png")); //for icon
        primaryStage.getIcons().add(icon);
        primaryStage.show();
    }
    public static void main(String[] args) {
        launch(args);
    }
}
