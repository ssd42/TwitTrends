package sample;

/**
 * Created by Steven on 7/6/2017.
 */
public class Entry {

    private String type;
    private String name;
    private String count;


    public Entry(String type, String name, String repr){
        this.type = type;
        this.name = name;
        this.count = repr;

    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCount() {
        return count;
    }

    public void setCount(String count) {
        this.count = count;
    }
}
