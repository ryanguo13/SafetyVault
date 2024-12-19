package shieldshell.idptwarmind.infoLayer;

import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.UrlEncodedFormEntity;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.message.BasicNameValuePair;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class apacheRunner {

    public static void running() throws Exception {
        HttpHost proxy = new HttpHost("localhost", 7890);

        // 创建HttpClient并设置代理
        CloseableHttpClient httpClient = HttpClients.custom()
                .setProxy(proxy)
                .build();

        // 创建POST请求
        HttpPost post = new HttpPost("https://flyingbird.pro/auth/login");

        // 创建表单数据
        List<BasicNameValuePair> formParams = new ArrayList<>();
        formParams.add(new BasicNameValuePair("email", "a3386026757@gmail.com"));
        formParams.add(new BasicNameValuePair("passwd", "Z9vTjt6Z9VA7-eh"));
        formParams.add(new BasicNameValuePair("code", ""));
        post.setEntity(new UrlEncodedFormEntity(formParams));

        // 发送请求并获取响应
        CloseableHttpResponse response = httpClient.execute(post);
        String result = EntityUtils.toString(response.getEntity(), StandardCharsets.UTF_8);

        System.out.println("bra" + result);
        System.out.println("\u767b\u5f55\u6210\u529f" );
    }








}
