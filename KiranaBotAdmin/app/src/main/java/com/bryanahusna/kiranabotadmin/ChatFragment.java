package com.bryanahusna.kiranabotadmin;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link ChatFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class ChatFragment extends Fragment {
    public SQLiteDatabase db;
    public String idUser;
    private Cursor mCursor;

    public ChatFragment() {
        // Required empty public constructor
    }

    public static ChatFragment newInstance(SQLiteDatabase db, String idUser){
        ChatFragment newFragment = new ChatFragment();
        newFragment.db = db;
        newFragment.idUser = idUser;
        return newFragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_chat, container, false);
        /*TextView namaText = v.findViewById(R.id.chat_nama);
        mCursor = db.rawQuery("SELECT * FROM riwayatcakap WHERE id_user=?", new String[]{idUser});
        mCursor.moveToFirst();
        namaText.setText(mCursor.getString(mCursor.getColumnIndexOrThrow("nama_user")));*/
        return v;
    }
}