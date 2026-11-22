package com.mausbot.aitradingmt5

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.mausbot.aitradingmt5.models.Asset
import com.mausbot.aitradingmt5.models.TradeSignal
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class TradingViewModel : ViewModel() {

    private val _assets = MutableLiveData<List<Asset>>()
    val assets: LiveData<List<Asset>> = _assets

    private val _signals = MutableLiveData<List<TradeSignal>>()
    val signals: LiveData<List<TradeSignal>> = _signals

    private val scope = CoroutineScope(Dispatchers.Main.immediate)

    fun loadAssets() {
        scope.launch {
            val list = withContext(Dispatchers.IO) {
                MT5Service.getSymbols()
            }
            _assets.value = list
        }
    }

    fun loadSignals() {
        scope.launch {
            val list = withContext(Dispatchers.IO) {
                MT5Service.getSignals()
            }
            _signals.value = list
        }
    }

    fun getDailyHighLow(symbol: String) {
        scope.launch {
            val data = withContext(Dispatchers.IO) {
                MT5Service.getDaily(symbol)
            }
            _signals.value = listOf(data)
        }
    }
}