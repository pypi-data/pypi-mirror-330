from typing import Dict

from lusid.api import InstrumentsApi
from lusid.models import InstrumentDefinition, Equity, InstrumentIdValue

from candela_kit.ignite import intent as ci
from candela_kit.ignite.intent import IObj
from candela_kit.tools.base import BaseTool
from .common import id_types, ccy_code


class CreateEquity(BaseTool):

    def intent(self) -> IObj:
        return ci.obj(
            app="lusid",
            entity="equity",
            function="create",
            input=ci.obj(
                identifiers=ci.dict(ci.str(), id_types),
                name=ci.str(),
                dom_ccy=ccy_code,
                scope=ci.str().as_nullable(),
            ),
        )

    def apply(self, intent: Dict) -> Dict:

        api = self.lusid_api(InstrumentsApi)

        vals = intent["input"]

        ins_def = InstrumentDefinition(
            name=vals["name"],
            identifiers={
                k: InstrumentIdValue(value=v) for k, v in vals["identifiers"].items()
            },
            definition=Equity(instrument_type="Equity", dom_ccy=vals["dom_ccy"]),
        )

        res = api.upsert_instruments(
            {"to_upsert": ins_def}, scope=vals.get("scope", "default")
        )

        if len(res.failed) == 1:
            raise ValueError(
                f'Instrument creation failed:\n\n{res.failed["to_upsert"]}'
            )

        ins = res.values["to_upsert"]

        return {
            "asset_class": ins.asset_class,
            "dom_ccy": ins.dom_ccy,
            "identifiers": ins.identifiers,
            "name": ins.name,
            "scope": ins.scope,
            "state": ins.state,
        }
