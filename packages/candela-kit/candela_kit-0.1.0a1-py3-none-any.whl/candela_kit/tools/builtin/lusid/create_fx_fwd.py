from typing import Dict

from lusid.api import InstrumentsApi
from lusid.models import FxForward, InstrumentDefinition, InstrumentIdValue

from candela_kit.ignite import intent as ci
from candela_kit.ignite.intent import IObj
from candela_kit.tools.base import BaseTool
from .common import id_types, to_datetime, ccy_code


class CreateFxFwd(BaseTool):

    def intent(self) -> IObj:
        return ci.obj(
            app="lusid",
            entity="fx_forward",
            function="create",
            inputs=ci.obj(
                identifiers=ci.dict(ci.str(), id_types),
                start_date=ci.date(),
                maturity_date=ci.date(),
                dom_amount=ci.real(),
                dom_ccy=ccy_code,
                fgn_amount=ci.real(),
                fgn_ccy=ccy_code,
                fixing_date=ci.date().as_nullable(),
                ref_spot_rate=ci.real().as_nullable(),
                name=ci.str(),
                scope=ci.str().as_nullable(),
            ),
        )

    def apply(self, intent: Dict) -> Dict:

        api = self.lusid_api(InstrumentsApi)

        vals = intent["inputs"]
        fx_fwd_def = FxForward(
            instrument_type="FxForward",
            dom_amount=vals["dom_amount"],
            dom_ccy=vals["dom_ccy"],
            fgn_amount=vals["fgn_amount"],
            fgn_ccy=vals["fgn_ccy"],
            ref_spot_rate=vals["ref_spot_rate"],
            start_date=to_datetime(vals["start_date"]),
            maturity_date=to_datetime(vals["maturity_date"]),
            fixing_date=to_datetime(vals["fixing_date"]),
        )

        ins_def = InstrumentDefinition(
            name=vals["name"],
            identifiers={
                k: InstrumentIdValue(value=v) for k, v in vals["identifiers"].items()
            },
            definition=fx_fwd_def,
        )
        res = api.upsert_instruments(
            {"to_upsert": ins_def}, scope=vals.get("scope", "default")
        )

        if len(res.failed) == 1:
            raise ValueError(
                f'Instrument creation failed:\n\n{res.failed["to_upsert"]}'
            )

        ins = res.values["to_upsert"]

        output = {
            "asset_class": ins.asset_class,
            "dom_ccy": ins.dom_ccy,
            "identifiers": ins.identifiers,
            "name": ins.name,
            "scope": ins.scope,
            "state": ins.state,
        }
        return output
