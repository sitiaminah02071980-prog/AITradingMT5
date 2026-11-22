package com.mausbot.aitradingmt5.models

data class Asset(
    val symbol: String = "",
    val bid: Double = 0.0,
    val ask: Double = 0.0,
    val bidHigh: Double = 0.0,
    val bidLow: Double = 0.0,
    val volume: Double = 0.0
)