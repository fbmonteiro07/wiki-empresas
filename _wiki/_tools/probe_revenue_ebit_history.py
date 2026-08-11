#!/usr/bin/env python3
"""Probe Bloomberg actual/estimate revenue and EBIT fields/overrides."""

import datetime as dt
import json
from pathlib import Path

import blpapi


def simplify(element):
    if element.isArray():
        values = []
        for i in range(element.numValues()):
            try:
                values.append(simplify(element.getValueAsElement(i)))
            except blpapi.exception.InvalidConversionException:
                values.append(element.getValue(i))
        return values
    if element.isComplexType():
        return {str(element.getElement(i).name()): simplify(element.getElement(i)) for i in range(element.numElements())}
    if element.isNull():
        return None
    value = element.getValue()
    if isinstance(value, (dt.date, dt.datetime, dt.time)):
        return value.isoformat()
    return str(value) if isinstance(value, blpapi.Name) else value


class Client:
    def __init__(self):
        options = blpapi.SessionOptions()
        options.setServerHost("localhost")
        options.setServerPort(8194)
        self.session = blpapi.Session(options)
        if not self.session.start() or not self.session.openService("//blp/refdata"):
            raise RuntimeError("Bloomberg Desktop API unavailable")
        self.service = self.session.getService("//blp/refdata")

    def close(self):
        self.session.stop()

    def ref(self, securities, fields, overrides=None):
        request = self.service.createRequest("ReferenceDataRequest")
        for security in securities:
            request.append("securities", security)
        for field in fields:
            request.append("fields", field)
        if overrides:
            array = request.getElement("overrides")
            for field_id, value in overrides.items():
                item = array.appendElement()
                item.setElement("fieldId", field_id)
                item.setElement("value", value)
        self.session.sendRequest(request)
        result = {}
        while True:
            event = self.session.nextEvent(10_000)
            for message in event:
                if message.hasElement("securityData"):
                    data = message.getElement("securityData")
                    for i in range(data.numValues()):
                        item = data.getValueAsElement(i)
                        security = item.getElementAsString("security")
                        row = {}
                        if item.hasElement("fieldData"):
                            fields_data = item.getElement("fieldData")
                            for j in range(fields_data.numElements()):
                                field = fields_data.getElement(j)
                                row[str(field.name())] = simplify(field)
                        if item.hasElement("fieldExceptions"):
                            row["_exceptions"] = simplify(item.getElement("fieldExceptions"))
                        result[security] = row
            if event.eventType() == blpapi.Event.RESPONSE:
                return result


def main():
    securities = ["AAPL US Equity", "005930 KS Equity", "2330 TT Equity", "SAP GY Equity"]
    client = Client()
    try:
        result = {
            "actual_default": client.ref(securities, ["NAME", "EQY_FISCAL_YR_END", "SALES_REV_TURN", "EBIT", "IS_OPER_INC", "OPER_MARGIN"]),
            "actual_2024_usd": client.ref(securities, ["NAME", "EQY_FUND_CRNCY", "SALES_REV_TURN", "EBIT", "IS_OPER_INC", "OPER_MARGIN"], {"EQY_FUND_YEAR": "2024", "FUND_PER": "Y", "EQY_FUND_CRNCY": "USD"}),
            "actual_2025_usd": client.ref(securities, ["NAME", "EQY_FUND_CRNCY", "SALES_REV_TURN", "EBIT", "IS_OPER_INC", "OPER_MARGIN"], {"EQY_FUND_YEAR": "2025", "FUND_PER": "Y", "EQY_FUND_CRNCY": "USD"}),
            "best_default": client.ref(securities, ["NAME", "BEST_SALES", "BEST_EBIT", "BEST_EBIT_MARGIN"]),
            "best_1fy": client.ref(securities, ["NAME", "BEST_SALES", "BEST_EBIT", "BEST_EBIT_MARGIN"], {"BEST_FPERIOD_OVERRIDE": "1FY"}),
            "best_1fy_usd_fund": client.ref(securities, ["NAME", "BEST_SALES", "BEST_EBIT", "BEST_EBIT_MARGIN"], {"BEST_FPERIOD_OVERRIDE": "1FY", "EQY_FUND_CRNCY": "USD"}),
            "best_2026": client.ref(securities, ["NAME", "BEST_SALES", "BEST_EBIT", "BEST_EBIT_MARGIN"], {"BEST_FPERIOD_OVERRIDE": "2026"}),
        }
    finally:
        client.close()
    output = Path("revenue_ebit_history_probe.json")
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(output.resolve())


if __name__ == "__main__":
    main()
