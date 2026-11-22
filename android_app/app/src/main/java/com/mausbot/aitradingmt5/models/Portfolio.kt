package com.mausbot.aitradingmt5.models

data class Portfolio(
    val login: Int = 0,
    val name: String = "",
    val server: String = "",
    val balance: Double = 0.0,
    val equity: Double = 0.0,
    val currency: String = "USD"
)