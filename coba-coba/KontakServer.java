import java.io.BufferedInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.HttpResponse;
import org.apache.hc.core5.http.io.entity.StringEntity;



/*import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.HttpHeaders;
import org.apache.hc.core5.http.io.entity.EntityUtils;*/


public class KontakServer{
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        String idUser = scanner.nextLine();
        String pesan = scanner.nextLine();

        String queryUrl = "https://kirana-bot.herokuapp.com/admin-chat";
        String pesanJson = String.format("{ \"id_user\" : \"%s\", \"pesan_admin\" : \"%s\" }", idUser, pesan);
        
        try {
            CloseableHttpClient httpClient = HttpClients.createDefault();
            StringEntity reqEntity = new StringEntity(pesanJson, ContentType.APPLICATION_JSON);
            HttpPost postMethod = new HttpPost(queryUrl);
            postMethod.setEntity(reqEntity);
            HttpResponse rawResponse = httpClient.execute(postMethod);
            System.out.println(rawResponse.toString());
            /*CloseableHttpClient httpClient = HttpClients.createDefault();
            HttpGet httpGet = new HttpGet(queryUrl);
            CloseableHttpResponse response = httpClient.execute(httpGet);
            System.out.println(response.getCode() + " " + response.getReasonPhrase());*/
        } catch (Exception e) {
            System.out.println(e.getMessage());
        } 

        scanner.close();
    }
}