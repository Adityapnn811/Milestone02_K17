package com.bryanahusna.kiranabotadmin;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

public class RunBg implements Runnable{
    @Override
    public void run() {
        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = DriverManager.getConnection(MainActivity.psqlUrl, MainActivity.psqlUser, MainActivity.psqlPassword);
            Statement st = conn.createStatement();
            st.execute("SELECT * FROM riwayatcakap");
            ResultSet rs = st.getResultSet();
            ResultSetMetaData rsmd = rs.getMetaData();
            while(rs.next()){
                for(int i=1; i<=rsmd.getColumnCount(); i++){
                    System.out.print(rs.getString(i) + " ");
                }
                System.out.println("");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
