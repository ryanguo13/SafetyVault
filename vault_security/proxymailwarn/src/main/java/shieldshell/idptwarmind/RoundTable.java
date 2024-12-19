package shieldshell.idptwarmind;

import shieldshell.idptwarmind.configLayer.yamlReader;
import shieldshell.idptwarmind.infoLayer.*;
import shieldshell.idptwarmind.mailutil.hullStone;

public class RoundTable {
    public static void main(String[] args) {

        try{

            yamlReader configRead = new yamlReader("config.json");

            abstractInfoRunner infoRunner = new NewOkhttpRunner(configRead);
            infoRunner.InfoRunnerLogin();

            var what = infoRunner.InfoRunnerReturnInfo();

            hullStone amaltheaOutpost = new hullStone(configRead);
            amaltheaOutpost.sendMessage(configRead, what[0], what[1]);
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
