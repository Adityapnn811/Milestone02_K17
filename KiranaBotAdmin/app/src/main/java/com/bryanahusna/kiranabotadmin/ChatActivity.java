package com.bryanahusna.kiranabotadmin;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.widget.TextView;

public class ChatActivity extends AppCompatActivity {
    public static String BUNDKEY_IDUSER = "id user";

    private String idUser;
    private SQLiteDatabase db;
    private Cursor mCursor;

    private RecyclerView chatRecyclerView;
    private ChatRecycle chatRecycleAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);
        idUser = getIntent().getStringExtra(BUNDKEY_IDUSER);
        //TextView namaText = findViewById(R.id.chatact_main);

        LocalDBHelper dbHelper = new LocalDBHelper(this, "kiranabot", null, 1);
        db = dbHelper.getWritableDatabase();
        mCursor = db.rawQuery("SELECT * FROM riwayatcakap WHERE id_user=?", new String[]{idUser});
        mCursor.moveToFirst();

        chatRecyclerView = findViewById(R.id.chatact_chatrecycler);
        chatRecycleAdapter = new ChatRecycle(this, db, idUser);
        chatRecyclerView.setAdapter(chatRecycleAdapter);

        //namaText.setText(mCursor.getString(mCursor.getColumnIndexOrThrow("nama_user")));;
    }
}