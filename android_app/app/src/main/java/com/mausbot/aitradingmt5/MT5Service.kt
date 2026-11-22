package com.mausbot.aitradingmt5

import android.content.Context
import android.content.SharedPreferences
import com.mausbot.aitradingmt5.models.Asset
import com.mausbot.aitradingmt5.models.TradeSignal
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

object MT5Service {

    private const val PREFS_NAME = "AITradingMT5Prefs"
    private const val KEY_BRIDGE_URL = "bridge_url"
    private const val DEFAULT_BRIDGE_URL = "http://192.168.1.100:5000"

    private lateinit var context: Context

    fun init(ctx: Context) {
        context = ctx.applicationContext
    }

    private fun getBridgeUrl(): String {
        val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        return prefs.getString(KEY_BRIDGE_URL, DEFAULT_BRIDGE_URL)
    }

    private fun getRetrofit(bridgeUrl: String): Retrofit {
        return Retrofit.Builder()
            .baseUrl(bridgeUrl)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    private val api: MT5Service.Mt5Api by lazy {
        getRetrofit(getBridgeUrl()).create(Mt5Api::class.java)
    }

    interface Mt5Api {
        @GET("/symbols")
        fun getSymbols(): Call<List<Asset>>

        @GET("/signal/{symbol}")
        fun getSignal(@Path("symbol") symbol: String): Call<TradeSignal>

        @GET("/daily/{symbol}")
        fun getDaily(@Path("symbol") symbol: String): Call<TradeSignal>

        @GET("/health")
        fun getHealth(): Call<Map<String, String>>
    }

    fun getSymbols(): List<Asset> {
        return withContext(Dispatchers.IO) {
            api.getSymbols().execute().body() ?: emptyList()
        }
    }

    fun getSignals(): List<TradeSignal> {
        return withContext(Dispatchers.IO) {
            val symbols = listOf("BTC", "ETH", "SOL", "XRP", "ADA")
            val signals = mutableListOf<TradeSignal>()
            for (s in symbols) {
                val sig = api.getSignal(s).execute().body()
                if (sig != null) signals.add(sig)
            }
            signals
        }
    }

    fun getDaily(symbol: String): TradeSignal {
        return withContext(Dispatchers.IO) {
            api.getDaily(symbol).execute().body() ?: TradeSignal(symbol, "HOLD", 0.0, 0.0, 0.0, "Data tidak tersedia")
        }
    }

    fun setBridgeUrl(url: String) {
        val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putString(KEY_BRIDGE_URL, url).apply()
    }

    fun getSavedBridgeUrl(): String {
        return getBridgeUrl()
    }
}