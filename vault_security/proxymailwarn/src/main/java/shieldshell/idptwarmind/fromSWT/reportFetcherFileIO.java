package shieldshell.idptwarmind.fromSWT;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

public class reportFetcherFileIO extends reportFetcher{
    File file;

    public reportFetcherFileIO(String filepath) {
        file = new File(filepath);
    }

    @Override
    public String fetchReport() throws Exception {
        BufferedReader br = new BufferedReader(new FileReader(file));
        String wholefile = "";
        String line;
        while ((line = br.readLine())!= null) {
            wholefile += line + "\n";
        }
        return wholefile;
    }
}
