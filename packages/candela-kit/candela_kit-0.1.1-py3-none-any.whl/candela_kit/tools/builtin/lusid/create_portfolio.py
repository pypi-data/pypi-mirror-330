from typing import Dict

from lusid.api import TransactionPortfoliosApi
from lusid.models import CreateTransactionPortfolioRequest

from candela_kit.ignite import intent as ci
from candela_kit.ignite.intent import IObj
from candela_kit.tools.base import BaseTool
from .common import resource_id, to_resource_id, to_datetime, ccy_code


class CreatePortfolio(BaseTool):

    def intent(self) -> IObj:

        acc_method_vals = [
            "Default",
            "AverageCost",
            "FirstInFirstOut",
            "LastInFirstOut",
            "HighestCostFirst",
            "LowestCostFirst",
        ]
        amortisation_vals = [
            "NoAmortisation",
            "StraightLine",
            "EffectiveYield",
            "StraightLineSettlementDate",
            "EffectiveYieldSettlementDate",
        ]

        return ci.obj(
            app="lusid",
            entity="portfolio",
            function="create",
            inputs=ci.obj(
                scope=ci.str(),
                name=ci.str(),
                code=ci.str(),
                created=ci.date(),
                base_currency=ccy_code,
                description=ci.str().as_nullable(),
                corporate_action_source=resource_id.as_nullable(),
                accounting_method=ci.enum(*acc_method_vals).as_nullable(),
                sub_holding_keys=ci.arr(ci.str(), 0, 100).as_nullable(),
                instrument_scopes=ci.arr(ci.str(), 0, 1).as_nullable(),
                amortisation_method=ci.enum(*amortisation_vals).as_nullable(),
                transaction_type_scope=ci.str().as_nullable(),
                cash_gain_loss_calculation_date=ci.enum(
                    "TransactionDate", "SettlementDate"
                ).as_nullable(),
            ),
        )

    def apply(self, intent: Dict):

        api = self.lusid_api(TransactionPortfoliosApi)

        vals = intent["inputs"]

        res = api.create_portfolio(
            scope=vals["scope"],
            create_transaction_portfolio_request=CreateTransactionPortfolioRequest(
                display_name=vals["name"],
                description=vals["description"],
                code=vals["code"],
                created=to_datetime(vals["created"]),
                base_currency=vals["base_currency"],
                corporate_action_source_id=to_resource_id(
                    vals["corporate_action_source"]
                ),
                accounting_method=vals["accounting_method"],
                sub_holding_keys=vals["sub_holding_keys"],
                instrument_scopes=vals["instrument_scopes"],
                amortisation_method=vals["amortisation_method"],
                transaction_type_scope=vals["transaction_type_scope"],
                cash_gain_loss_calculation_date=vals["cash_gain_loss_calculation_date"],
            ),
        )

        output = {
            "display_name": res.display_name,
            "description": res.description,
            "code": res.id.code,
            "scope": res.id.scope,
            "type": res.type,
            "created": res.created,
            "base_currency": res.base_currency,
            "instrument_scopes": res.instrument_scopes,
            "accounting_method": res.accounting_method,
            "amortisation_method": res.amortisation_method,
            "transaction_type_scope": res.transaction_type_scope,
            "cash_gain_loss_calculation_date": res.cash_gain_loss_calculation_date,
        }
        return output
