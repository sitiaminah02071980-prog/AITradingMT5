package com.mausbot.aitradingmt5

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class SettingsActivity : AppCompatActivity() {

    private lateinit var etBridgeUrl: EditText
    private lateinit var tvStatus: TextView
    private lateinit var btnSave: Button
    private lateinit var btnTest: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        etBridgeUrl = findViewById(R.id.etBridgeUrl)
        tvStatus = findViewById(R.id.tvStatus)
        btnSave = findViewById(R.id.btnSave)
        btnTest = findViewById(R.id.btnTest)

        // Muat URL yang tersimpan
        val savedUrl = MT5Service.getSavedBridgeUrl()
        etBridgeUrl.setText(savedUrl)

        btnSave.setOnClickListener {
            val url = etBridgeUrl.text.toString().trim()
            if (url.isNotEmpty()) {
                MT5Service.init(applicationContext)
                MT5Service.setBridgeUrl(url)
                tvStatus.text = "URL disimpan: $url"
                tvStatus.setTextColor(android.graphics.Color.GREEN)
                Toast.makeText(this, "Bridge URL disimpan", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "URL tidak boleh kosong", Toast.LENGTH_SHORT).show()
            }
        }

        btnTest.setOnClickListener {
            val url = etBridgeUrl.text.toString().trim()
            if (url.isNotEmpty()) {
                testConnection(url)
            } else {
                Toast.makeText(this, "Masukkan URL terlebih dahulu", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun testConnection(url: String) {
        // Sederhana: coba ping endpoint /health
        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
            tvStatus.text = "Menguji koneksi..."
            tvStatus.setTextColor(android.graphics.Color.YELLOW)
        }, 100)

        val thread = java.lang.Thread {
            try {
                val urlObj = java.net.URL("$url/health")
                val conn = urlObj.openConnection() as java.net.HttpURLConnection
                conn.requestMethod = "GET"
                conn.connectTimeout = 5000
                conn.readTimeout = 5000
                val code = conn.responseCode

                android.os.Handler(android.os.Looper.getMainLooper()).post {
                    if (code == 200) {
                        tvStatus.text = "Koneksi OK (status: $code)"
                        tvStatus.setTextColor(android.graphics.Color.GREEN)
                        Toast.makeText(this@SettingsActivity, "Bridge terhubung!", Toast.LENGTH_SHORT).show()
                    } else {
                        tvStatus.text = "Koneksi gagal (status: $code)"
                        tvStatus.setTextColor(android.graphics.Color.RED)
                    }
                }
            } catch (e: Exception) {
                android.os.Handler(android.os.Looper.getMainLooper()).post {
                    tvStatus.text = "Koneksi gagal: ${e.message}"
                    tvStatus.setTextColor(android.graphics.Color.RED)
                    Toast.makeText(this@SettingsActivity, "Bridge tidak terhubung", Toast.LENGTH_SHORT).show()
                }
            }
        }
        thread.start()
    }
}