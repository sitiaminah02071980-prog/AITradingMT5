package com.mausbot.aitradingmt5.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.mausbot.aitradingmt5.R
import com.mausbot.aitradingmt5.databinding.ItemAssetBinding
import com.mausbot.aitradingmt5.databinding.ItemSignalBinding
import com.mausbot.aitradingmt5.models.Asset
import com.mausbot.aitradingmt5.models.TradeSignal

class AssetAdapter(private val items: List<Any>) : RecyclerView.Adapter<RecyclerView.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        return when (viewType) {
            1 -> {
                val binding = ItemSignalBinding.inflate(inflater, parent, false)
                SignalViewHolder(binding)
            }
            else -> {
                val binding = ItemAssetBinding.inflate(inflater, parent, false)
                AssetViewHolder(binding)
            }
        }
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        val item = items[position]
        when (holder) {
            is AssetViewHolder -> {
                val asset = item as Asset
                holder.bind(asset)
            }
            is SignalViewHolder -> {
                val signal = item as TradeSignal
                holder.bind(signal)
            }
        }
    }

    override fun getItemCount(): Int = items.size

    override fun getItemViewType(position: Int): Int {
        return if (items[position] is TradeSignal) 1 else 0
    }

    class AssetViewHolder(private val binding: ItemAssetBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(asset: Asset) {
            binding.tvSymbol.text = asset.symbol
            binding.tvBid.text = "Bid: " + asset.bid
            binding.tvAsk.text = "Ask: " + asset.ask
            binding.tvHigh.text = "High: " + asset.bidHigh
            binding.tvLow.text = "Low: " + asset.bidLow
        }
    }

    class SignalViewHolder(private val binding: ItemSignalBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(signal: TradeSignal) {
            binding.tvSymbol.text = signal.symbol
            binding.tvSignal.text = "Sinyal: " + signal.signal
            binding.tvBid.text = "Bid: " + signal.bid
            binding.tvHigh.text = "High: " + signal.bidHigh
            binding.tvLow.text = "Low: " + signal.bidLow
            binding.tvReason.text = signal.reason
        }
    }
}
