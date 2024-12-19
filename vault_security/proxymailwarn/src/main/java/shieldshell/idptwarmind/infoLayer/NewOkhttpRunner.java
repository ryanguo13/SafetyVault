package shieldshell.idptwarmind.infoLayer;

import okhttp3.FormBody;
import okhttp3.Headers;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import shieldshell.idptwarmind.configLayer.yamlReader;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class NewOkhttpRunner extends abstractInfoRunner {
    OkHttpClient client;
    String cookieMainStation;
    String cookieLoginSuccesser;
    private String username;
    private String password;
    Map<String, String> cookieMap = new HashMap<String, String>();

    public NewOkhttpRunner(yamlReader configReader) throws Exception {
        this.client = new OkHttpClient.Builder()
                .proxy(new Proxy(Proxy.Type.HTTP,new InetSocketAddress("127.0.0.1",7890)))
                .followRedirects(true)
                .readTimeout(1000L, TimeUnit.MINUTES).build();

        this.username = configReader.readUserName();
        this.password = configReader.readPassword();
    }

    @Override
    public void InfoRunnerLogin() throws Exception{
        //start request the first part of cookie
        Request requestMainCookie = new Request.Builder()
                .url("https://flyingbird.pro/")
                .build();

        var cookieOneTmp = this.client.newCall(requestMainCookie).execute();
        this.cookieMainStation = cookieOneTmp.header("Set-Cookie");
        //to here, complete collect first cookie

        //start request the second part of cookie
        FormBody postBody = new FormBody.Builder()
                .add("email",username)
                .add("passwd",password)
                .add("code", "")
                .build();
        Request requestSecondCookie = new Request.Builder()
                .url("https://flyingbird.pro/auth/login")
                .addHeader("Cookie",this.cookieMainStation)
                .post(postBody)
                .build();
        var cookieTwoTmp = this.client.newCall(requestSecondCookie).execute();
        this.cookieLoginSuccesser= NewOkhttpRunner.stringListConcate(cookieTwoTmp.headers("Set-Cookie"));
        //second phase cookie collect complete
    }


    @Override
    public String[] InfoRunnerReturnInfo() throws Exception{
        var headers = this.getCookieMap();
        Request getInfoPage = new Request.Builder()
                .url("https://flyingbird.pro/user")
                .addHeader("Cookie", headers)
                .build();

        var response = this.client.newCall(getInfoPage).execute().body().string();

        String[] resultStrAry = new String[2];
        String regex = "<span class=\"counter\">(\\d+\\.\\d+)</span>";
        Pattern pattern = Pattern.compile(regex);

        Matcher matcher = pattern.matcher(response);
        if (matcher.find()) {
            resultStrAry[0] = matcher.group(1);
        }
        regex = "今日已用: (\\d+\\.\\d+)GB";
        pattern = Pattern.compile(regex);

        // 创建匹配器
        matcher = pattern.matcher(response);
        if (matcher.find()) {
            resultStrAry[1] = matcher.group(1);
        }

        return resultStrAry;
    }


    private static String stringListConcate(List<String> list) {
        String result = new String();
        for(String i: list) {
            result += i + " ";
        }
        return result;
    }


    public String getCookieMap() throws Exception {
        var mapper = NewOkhttpRunner.cookieConstruct(this.cookieMainStation,this.cookieLoginSuccesser);
        StringBuilder result = new StringBuilder();
        for (Map.Entry<String, String> entry : mapper.entrySet()) {
            result.append(entry.getKey()+"="+ entry.getValue()+"; ");
        }
        return result.toString();
    }

    private static HashMap<String, String> cookieConstruct(String ccokieOne, String ccokieTwo) throws Exception {
        HashMap<String, String> resultMap = new HashMap<>();

        Matcher matcher = Pattern.compile("(?<=NB_SRVID=)[^;]+").matcher(ccokieOne);
        matcher.find();
        resultMap.put("NB_SRVID", matcher.group());

        matcher = Pattern.compile("(?<=uid=)[^;]+").matcher(ccokieTwo);
        matcher.find();
        resultMap.put("uid", matcher.group());

        matcher = Pattern.compile("(?<=email=)[^;]+").matcher(ccokieTwo);
        matcher.find();
        resultMap.put("email", matcher.group());

        matcher = Pattern.compile("(?<=key=)[^;]+").matcher(ccokieTwo);
        matcher.find();
        resultMap.put("key", matcher.group());

        matcher = Pattern.compile("(?<=ip=)[^;]+").matcher(ccokieTwo);
        matcher.find();
        resultMap.put("ip", matcher.group());

        matcher = Pattern.compile("(?<=expire_in=)[^;]+").matcher(ccokieTwo);
        matcher.find();
        resultMap.put("expire_in", matcher.group());

        matcher = Pattern.compile("(?<=PHPSESSID=)[^;]+").matcher(ccokieTwo);
        matcher.find();
        resultMap.put("PHPSESSID", matcher.group());

        return resultMap;
    }

    private static String[] infoConstruct(String htmlpage) throws Exception {

        return null;
    }
}
