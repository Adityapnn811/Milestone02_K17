package com.bryanahusna.kiranabotadmin;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Bundle;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

public class MainActivity extends AppCompatActivity {
    static String psqlRiwayatcakap = "riwayatcakap";
    static String psqlHost = "ec2-54-196-65-186.compute-1.amazonaws.com";
    static String psqlDatabase = "d12jneq73g7u2";
    static String psqlUser = "aaqgmutpyfxgmx";
    static short psqlPort = 5432;
    static String psqlPassword = "614e04f0ec7d6a687c0b4e8c6a9941391d70349037ac3b1384149752bd7eeacd";
    static String psqlUrl = "jdbc:postgresql://ec2-54-196-65-186.compute-1.amazonaws.com:5432/d12jneq73g7u2";
    //static String psqlUri = "postgres://aaqgmutpyfxgmx:614e04f0ec7d6a687c0b4e8c6a9941391d70349037ac3b1384149752bd7eeacd@ec2-54-196-65-186.compute-1.amazonaws.com:5432/d12jneq73g7u2";
    //static String psqlHerokucli = "heroku pg:psql postgresql-trapezoidal-98002 --app kirana-bot";

    private LocalDBHelper dbhelper;
    private SQLiteDatabase db;
    private UserRecycle usersAdapter;
    private RecyclerView usersRecyclerView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Thread mantap = new Thread(new RunBg());
        //mantap.start();

        dbhelper = new LocalDBHelper(this, "kiranabot", null, 1);
        db = dbhelper.getWritableDatabase();

        usersAdapter = new UserRecycle(this, db);
        usersRecyclerView = findViewById(R.id.main_userrecycler);
        usersRecyclerView.setAdapter(usersAdapter);
    }

    public void startChatWindow(String idUser){
        //getSupportFragmentManager().beginTransaction().add(R.id.mainchat_content, ChatFragment.newInstance(db, idUser), "chat fragment").commitNow();
        Intent dataIntent = new Intent(this, ChatActivity.class);
        dataIntent.putExtra(ChatActivity.BUNDKEY_IDUSER, idUser);
        startActivity(dataIntent);
    }
}