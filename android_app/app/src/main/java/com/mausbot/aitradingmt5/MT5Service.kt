package com.mausbot.aitradingmt5

import com.mausbot.aitradingmt5.models.Asset
import com.mausbot.aitradingmt5.models.TradeSignal
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path

object MT5Service {

    // Ganti dengan IP desktop tempat bridge_server.py berjalan
    private const val BRIDGE_URL = "http://192.168.1.100:5000"

    private val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(BRIDGE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val api: Mt5Api = retrofit.create(Mt5Api::class.java)

    interface Mt5Api {
        @GET("/symbols")
        fun getSymbols(): Call<List<Asset>>

        @GET("/signal/{symbol}")
        fun getSignal(@Path("symbol") symbol: String): Call<TradeSignal>

        @GET("/daily/{symbol}")
        fun getDaily(@Path("symbol") symbol: String): Call<TradeSignal>
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
}