package com.bryanahusna.kiranabotadmin;

import android.content.Context;
import android.database.DatabaseErrorHandler;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import androidx.annotation.Nullable;

public class LocalDBHelper extends SQLiteOpenHelper {


    public LocalDBHelper(Context context, String name, SQLiteDatabase.CursorFactory factory, int version) {
        super(context, name, factory, version);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS riwayatcakap (id_user TEXT, nama_user TEXT, time_epoch INTEGER, pesan TEXT);");
        db.execSQL("INSERT INTO riwayatcakap VALUES ('U2cc53b28669cf7c907d47e8653c08c6a', 'Bryan Amirul Husna', 1628368186, 'Selamat pagi bot, mau tanya nih');");
        db.execSQL("INSERT INTO riwayatcakap VALUES ('U2cc53b28669cf7c907d47e8653c08c6a', 'Bryan Amirul Husna', 1628369361, '\"Apa kabar kamu\", kata di''a sih Ini bahasa alien: ѲѹҷҔ');");
        db.execSQL("INSERT INTO riwayatcakap VALUES ('Ua68faad875d238f2b77e6f4b1df027ab', 'Alif Yasa', 1628377910, 'Tes lagi');");
        db.execSQL("INSERT INTO riwayatcakap VALUES ('Ua68faad875d238f2b77e6f4b1df027ab', 'Alif Yasa', 1628377954, 'Ajiah');");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS riwayatcakap;");
        onCreate(db);
    }
}
