from enum import Enum

class SourceTier(Enum):
    """Уровни источников данных для планирования архитектуры"""
    STABLE = "stable"        # avito - синхронный, стабильный
    LIMITED = "limited"      # wb - асинхронный, rate-limited
    HEAVY = "heavy"          # ozon - отдельный воркер, Playwright, очередь

# Будущая архитектура:
# Avito: sync, быстро, часто
# WB: async, раз в N часов, через прокси
# Ozon: отдельный воркер, Playwright, очередь задач
