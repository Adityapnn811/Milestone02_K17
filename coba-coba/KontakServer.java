import java.io.BufferedInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;



public class KontakServer{
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        String idUser = scanner.nextLine();
        String pesan = scanner.nextLine();

        String queryUrl = "https://kirana-bot.herokuapp.com/admin-chat";
        String pesanJson = String.format("{ \"id_user\" : \"%s\", \"pesan_admin\" : \"%s\" }", idUser, pesan);

        try {
            URL url = new URL(queryUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(20000);
            conn.setRequestProperty("Content-Type", "application/json; utf-8");
            conn.setRequestProperty("Accept", "application/json");

            conn.setDoOutput(true);
            //conn.setDoInput(true);
            //conn.setRequestMethod("GET");
            conn.setRequestMethod("POST");
            conn.connect();
            //conn.getRequestMethod();
            OutputStream os = conn.getOutputStream();
            os.write(pesanJson.getBytes("utf-8"));
            os.close();
            //InputStream is = conn.getInputStream();
            //is.readAllBytes();
            //is.close();
            //InputStream in = new BufferedInputStream(conn.getInputStream());
            //String result = IOUtils.toString(in, "UTF-8");

            //System.out.println(result);
            
        } catch (Exception e) {
            e.printStackTrace();
        }

        scanner.close();
    }
}