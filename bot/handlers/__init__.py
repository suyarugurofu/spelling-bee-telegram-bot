from aiogram import Router
from .start import router as start_router
from .stats import router as stats_router
from .voice import router as voice_router      # ← новое
from .training import router as training_router

router = Router()
router.include_router(start_router)
router.include_router(stats_router)
router.include_router(voice_router)           # ← добавь эту строку
router.include_router(training_router)