package com.mausbot.aitradingmt5.models

data class TradeSignal(
    val symbol: String = "",
    val signal: String = "HOLD",
    val bid: Double = 0.0,
    val bidHigh: Double = 0.0,
    val bidLow: Double = 0.0,
    val reason: String = "",
    val lotSize: Double = 0.01
)