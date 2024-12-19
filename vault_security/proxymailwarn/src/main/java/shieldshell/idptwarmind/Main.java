package shieldshell.idptwarmind;

import shieldshell.idptwarmind.fromSWT.reportFetcher;
import shieldshell.idptwarmind.fromSWT.reportFetcherFileIO;
import shieldshell.idptwarmind.infoLayer.NewOkhttpRunner;
import shieldshell.idptwarmind.infoLayer.OkhttpRunner;
import shieldshell.idptwarmind.configLayer.yamlReader;
import shieldshell.idptwarmind.infoLayer.abstractInfoRunner;
import shieldshell.idptwarmind.mailutil.hullStone;

public class Main {
    public static void main(String[] args) {

        if(args.length==1){
            System.out.println("Please start with args1:configfile path, and arg2: reportfile path");
            System.exit(1);
        }
        try{

            yamlReader configRead = new yamlReader(args[1]);

            reportFetcher infoextractor = new reportFetcherFileIO(args[2]);
            var myfile = infoextractor.fetchReport();

            hullStone amaltheaOutpost = new hullStone(configRead);
            amaltheaOutpost.sendMessage(configRead, myfile);
        } catch (Exception e) {
            e.printStackTrace();
        }

        /*
         */
    }
}