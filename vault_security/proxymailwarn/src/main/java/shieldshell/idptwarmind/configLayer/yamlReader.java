package shieldshell.idptwarmind.configLayer;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import shieldshell.idptwarmind.mailutil.emailSender;

import java.io.File;
import java.util.ArrayList;

public class yamlReader {

    ObjectMapper resolver = new ObjectMapper();
    //Well Actually🤓
    //this is Json...... for now.

    private File configFile;
    private ConfigFile config;
    private ArrayList<String> audiences;
    private emailSender theRunner;
    public JsonNode rootnode;

    public yamlReader(String filepath) throws Exception {
        this.openConfigFile(filepath);
        this.rootnode = this.resolver.readTree(this.configFile);
        this.config = this.resolver.treeToValue(this.rootnode.path("proxyconfig"), ConfigFile.class);
        this.theRunner = this.resolver.treeToValue(this.rootnode.path("emailrunnerconfig"), emailSender.class);

        this.audiences = this.resolver.treeToValue(this.rootnode.path("receiverconfig"), ArrayList.class);
    }

    private void openConfigFile(String filepathname)throws Exception{
        configFile = new File(filepathname);
    }

    public String readAddr() throws Exception{

        return this.config.address;
    }

    public String readUserName() throws Exception{

        return this.config.username;
    }

    public String readPassword() throws Exception{

        return this.config.password;
    }

    public String[] readSenderConfig() throws Exception{
        String[] result = new String[]{
                this.theRunner.addr, this.theRunner.port,
                this.theRunner.email,
                this.theRunner.secret ,this.theRunner.password,
                };
        return result;
    }

    public ArrayList<String> readReceiverConfig() throws Exception{
        return this.audiences;
    }

}

//test pass!
//@author: independent anonymous developer
