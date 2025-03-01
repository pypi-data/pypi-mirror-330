from typing import Dict

from pandas.core.interchange.dataframe_protocol import DataFrame

from candela_kit.ignite import intent as ci
from candela_kit.ignite.intent import IObj
from candela_kit.tools.base import BaseTool


class LumiRunSql(BaseTool):

    def intent(self) -> IObj:
        return ci.obj(
            app="luminesce",
            function="run",
            sql=ci.str(),
        )

    def apply(self, intent: Dict) -> DataFrame:
        """
        Apply an action given an intent.

        Args:
            intent (Dict): An intent dictionary defining the action to take.

        Returns:
            An event wrapping the dictionary containing the csv result of the action.

        """
        sql = intent["sql"]
        if sql:
            return self.lumipy_client().run(sql, quiet=True)

        raise ValueError("No SQL was found in the intent json")
