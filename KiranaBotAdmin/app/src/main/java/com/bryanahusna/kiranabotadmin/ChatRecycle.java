package com.bryanahusna.kiranabotadmin;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class ChatRecycle extends RecyclerView.Adapter<ChatRecycle.ViewHolder> {
    private Context context;
    private SQLiteDatabase db;
    private String idUser;
    private Cursor mCursor;

    public ChatRecycle(Context context, SQLiteDatabase db, String idUser){
        this.context = context;
        this.db = db;
        mCursor = db.rawQuery("SELECT * FROM riwayatcakap WHERE id_user=? ORDER BY time_epoch ASC", new String[]{idUser});
        mCursor.moveToFirst();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.singlerecy_chat, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        mCursor.moveToPosition(position);
        holder.singleChat.setText(mCursor.getString(mCursor.getColumnIndex("pesan")));
    }

    @Override
    public int getItemCount() {
        return mCursor.getCount();
    }


    public static class ViewHolder extends RecyclerView.ViewHolder{
        public TextView singleChat;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            singleChat = itemView.findViewById(R.id.chatact_singlechat);
        }
    }
}
