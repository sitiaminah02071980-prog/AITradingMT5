package com.mausbot.aitradingmt5

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import com.mausbot.aitradingmt5.databinding.ActivityMainBinding
import com.mausbot.aitradingmt5.ui.AssetAdapter

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var viewModel: TradingViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = DataBindingUtil.setContentView(this, R.layout.activity_main)
        viewModel = TradingViewModel()

        binding.viewModel = viewModel
        binding.lifecycleOwner = this

        // Observer untuk update UI saat data berubah
        viewModel.assets.observe(this) { assets ->
            binding.assetList.adapter = AssetAdapter(assets)
        }

        viewModel.signals.observe(this) { signals ->
            binding.signalList.adapter = AssetAdapter(signals)
        }

        // Muat data awal
        viewModel.loadAssets()
        viewModel.loadSignals()
    }
}