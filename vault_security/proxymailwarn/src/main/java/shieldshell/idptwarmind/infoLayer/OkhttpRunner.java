package shieldshell.idptwarmind.infoLayer;

import okhttp3.*;
import shieldshell.idptwarmind.configLayer.yamlReader;

import java.net.InetSocketAddress;
import java.net.Proxy;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class OkhttpRunner {
    OkHttpClient client ;
    Request request;
    Response response;
    FormBody formBody;
    Headers headers;
    List<String> successer;


    public OkhttpRunner(yamlReader configReader) throws Exception {

        this.headers = new Headers.Builder()
                .add("accept", "application/json, text/javascript, */*; q=0.01")
                .add("accept-language", "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6")
                .add("content-type", "application/x-www-form-urlencoded; charset=UTF-8")
                .add("content-length", "58")
                .add("origin", "https://flyingbird.pro")
                .add("priority", "u=1, i")
                .add("referer", "https://flyingbird.pro/auth/login")
                .add("sec-ch-ua", "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"")
                .add("sec-ch-ua-arch", "\"x86\"")
                .add("sec-ch-ua-bitness", "\"64\"")
                .add("sec-ch-ua-full-version", "\"127.0.2651.105\"")
                .add("sec-ch-ua-mobile", "?0")
                .add("sec-ch-ua-model", "\"\"")
                .add("sec-ch-ua-platform", "\"Linux\"")
                .add("user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0")
                .add("x-requested-with", "XMLHttpRequest")
                .add("sec-ch-ua-platform-version","6.1.0")
                .build();

        this.client = new OkHttpClient.Builder()
                .proxy(new Proxy(Proxy.Type.HTTP,new InetSocketAddress("127.0.0.1",7890)))
                .followRedirects(true)
                //.cookieJar(new CookieJar() {})
                .readTimeout(1000L, TimeUnit.MINUTES).build();


        var username = configReader.readUserName();
        var password = configReader.readPassword();
        System.out.println(username + " " + password);
        this.formBody = new FormBody.Builder()
            .add("email",username)
                .add("passwd",password)
                .add("code", "")
                .build();


        this.request = new Request.Builder()
                .url("https://flyingbird.pro/auth/login")
                .post(this.formBody)
                .headers(this.headers)
                .build();
    }

    public void sendRequest() throws Exception {

        this.response = this.client.newCall(this.request).execute();

        /*
        Field[] responseFields = this.response.getClass().getDeclaredFields();
        for(Field field : responseFields) {
            field.setAccessible(true);
            System.out.println(field + " " + field.get(this.response));
        }

        */
        //var testVal = this.response
        this.successer = this.response.headers("Set-Cookie");
    }

    public String[] testCookieAvailability() throws Exception {
        var cookie = OkhttpRunner.stringListConcate(this.successer);

        Headers headers = new Headers.Builder()
                .add(":authority", "flyingbird.pro")
                .add(":method", "GET")
                .add(":path", "/user")
                .add(":scheme", "https")
                .add("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
                .add("accept-language", "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6")
                .add("Cookie", cookie)
                .add("priority", "u=0, i")
                .add("referer", "https://flyingbird.pro/auth/login")
                .add("sec-ch-ua", "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"")
                .add("sec-ch-ua-arch", "\"x86\"")
                .add("sec-ch-ua-bitness", "\"64\"")
                .add("sec-ch-ua-full-version", "\"127.0.2651.105\"")
                .add("sec-ch-ua-full-version-list", "\"Not)A;Brand\";v=\"99.0.0.0\", \"Microsoft Edge\";v=\"127.0.2651.105\", \"Chromium\";v=\"127.0.6533.120\"")
                .add("sec-ch-ua-mobile", "?0")
                .add("sec-ch-ua-model", "\"\"")
                .add("sec-ch-ua-platform", "\"Linux\"")
                .add("sec-ch-ua-platform-version", "\"6.1.0\"")
                .add("sec-fetch-dest", "document")
                .add("sec-fetch-mode", "navigate")
                .add("sec-fetch-site", "same-origin")
                .add("sec-fetch-user", "?1")
                .add("upgrade-insecure-requests", "1")
                .add("user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0")
                .build();
        Request testReq = new Request.Builder()
                .url("https://flyingbird.pro/user")
                .headers(headers)
                .build();

        var response = this.client.newCall(testReq).execute().body().string();

        String[] resultStrAry = new String[2];

        String regex = "<span class=\"counter\">(\\d+\\.\\d+)</span>";
        Pattern pattern = Pattern.compile(regex);

        // 创建匹配器
        Matcher matcher = pattern.matcher(response);

        // 查找并提取匹配的数字
        if (matcher.find()) {
            resultStrAry[0] = matcher.group(1);
        }
        regex = "今日已用: (\\d+\\.\\d+)GB";
        pattern = Pattern.compile(regex);

        // 创建匹配器
        matcher = pattern.matcher(response);

        // 查找并提取匹配的数字
        if (matcher.find()) {
            resultStrAry[1] = matcher.group(1);
        }

        return resultStrAry;
    }

    public static String stringListConcate(List<String> list) {
        String result = new String();
        for(String i: list) {
            result += i + " ";
        }
        return result;
    }



    public void IamCacheTmp(){
    }
}