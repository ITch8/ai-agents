from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models.schemas import BacktestRequest, HedgeFundRequest
from app.backend.routes.hedge_fund import backtest as legacy_backtest
from app.backend.routes.hedge_fund import get_agents as legacy_get_agents
from app.backend.routes.hedge_fund import run as legacy_run

router = APIRouter(prefix="/trade-decision")


@router.post("/run")
async def run_trade_decision(
    request_data: HedgeFundRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Alias endpoint for foreign trade decision execution."""
    return await legacy_run(request_data=request_data, request=request, db=db)


@router.post("/backtest")
async def backtest_trade_decision(
    request_data: BacktestRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Alias endpoint kept for compatibility (currently deprecated)."""
    return await legacy_backtest(request_data=request_data, request=request, db=db)


@router.get("/agents")
async def get_trade_agents():
    """Return available decision agents."""
    return await legacy_get_agents()
