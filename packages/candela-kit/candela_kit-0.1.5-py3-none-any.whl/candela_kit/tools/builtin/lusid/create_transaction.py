from typing import Dict

from lusid.api import TransactionPortfoliosApi
from lusid.models import TransactionRequest, TransactionPrice, CurrencyAndAmount

from candela_kit.ignite import intent as ci
from candela_kit.ignite.intent import IObj
from candela_kit.tools.base import BaseTool
from candela_kit.tools.builtin.lusid.common import id_types, resource_id, to_resource_id


class CreateTransaction(BaseTool):

    def intent(self) -> IObj:

        txn_price = ci.obj(
            price=ci.real(), type=ci.enum("Price", "Yield", "Spread", "CashFlowPerUnit")
        )
        ccy_and_amount = ci.obj(amount=ci.real(), currency=ci.iso_ccys())

        return ci.obj(
            app="lusid",
            entity="transaction",
            function="create",
            inputs=ci.obj(
                portfolio_scope=ci.str(),
                portfolio_code=ci.str(),
                transaction_id=ci.str(),
                type=ci.enum("Buy", "Sell", "StockIn", "StockOut"),
                instrument_identifiers=ci.dict(ci.str(), id_types),
                transaction_date=ci.date(),
                settlement_date=ci.date(),
                units=ci.real(),
                total_consideration=ccy_and_amount,
                transaction_price=txn_price.as_nullable(),
                exchange_rate=ci.real().as_nullable(),
                transaction_currency=ci.iso_ccys().as_nullable(),
                counterparty_id=ci.str().as_nullable(),
                transaction_source=ci.str().as_nullable(),
                otc_confirmation=ci.obj(
                    counterparty_agreement_id=resource_id
                ).as_nullable(),
                order_id=resource_id.as_nullable(),
                allocation_id=resource_id.as_nullable(),
                custodian_account_id=resource_id.as_nullable(),
            ),
        )

    def apply(self, intent: Dict) -> Dict:

        api = self.lusid_api(TransactionPortfoliosApi)

        vals = intent["inputs"]

        def to_txn_price(x: Dict | None) -> TransactionPrice | None:
            if x is None:
                return None

            return TransactionPrice(**x)

        def to_ccy_and_amount(x: Dict | None) -> CurrencyAndAmount | None:
            if x is None:
                return None
            return CurrencyAndAmount(**x)

        res = api.upsert_transactions(
            scope=vals["portfolio_scope"],
            code=vals["portfolio_code"],
            transaction_request=[
                TransactionRequest(
                    transaction_id=vals["transaction_id"],
                    type=vals["type"],
                    instrument_identifiers={
                        f"Instrument/default/{k}": v
                        for k, v in vals["instrument_identifiers"].items()
                    },
                    transaction_date=vals["transaction_date"],
                    settlement_date=vals["settlement_date"],
                    units=vals["units"],
                    transaction_price=to_txn_price(vals["transaction_price"]),
                    total_consideration=to_ccy_and_amount(vals["total_consideration"]),
                    exchange_rate=vals["exchange_rate"],
                    transaction_currency=vals["transaction_currency"],
                    counterparty_id=vals["counterparty_id"],
                    source=vals["transaction_source"],
                    otc_confirmation=None,
                    order_id=to_resource_id(vals["order_id"]),
                    allocation_id=to_resource_id(vals["allocation_id"]),
                    custodian_account_id=to_resource_id(vals["custodian_account_id"]),
                )
            ],
        )

        return {
            "effective_from": res.version.effective_from,
            "as_at_date": res.version.as_at_date,
            "request_id_created": res.version.request_id_created,
            "request_id_modified": res.version.request_id_modified,
        }
