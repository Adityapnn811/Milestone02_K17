package com.bryanahusna.kiranabotadmin;

import android.app.Activity;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.progressindicator.LinearProgressIndicator;

public class UserRecycle extends RecyclerView.Adapter<UserRecycle.ViewHolder>{
    private Context context;
    private SQLiteDatabase db;
    private Cursor mcursor;

    public UserRecycle(Context context, SQLiteDatabase db){
        this.context = context;
        this.db = db;
        mcursor = db.rawQuery("SELECT DISTINCT id_user, nama_user FROM riwayatcakap", null);
        mcursor.moveToFirst();
    }

    @NonNull
    @Override
    public UserRecycle.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.singlerecy_user, parent, false);
        return new UserRecycle.ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        mcursor.moveToPosition(position);
        holder.namaUser.setText(mcursor.getString(mcursor.getColumnIndex("nama_user")));
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ((MainActivity)context).startChatWindow(mcursor.getString(mcursor.getColumnIndex("id_user")));
            }
        });
    }

    @Override
    public int getItemCount() {
        return mcursor.getCount();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder{
        public TextView namaUser;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            namaUser = itemView.findViewById(R.id.singlerecyuser_namauser);
        }
    }
}