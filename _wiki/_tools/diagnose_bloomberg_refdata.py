#!/usr/bin/env python3
"""Print raw Bloomberg refdata events to diagnose an empty Desktop API response."""

import blpapi


def main():
    options = blpapi.SessionOptions()
    options.setServerHost("localhost")
    options.setServerPort(8194)
    session = blpapi.Session(options)
    try:
        print("start", session.start())
        print("open", session.openService("//blp/refdata"))
        service = session.getService("//blp/refdata")
        request = service.createRequest("ReferenceDataRequest")
        request.append("securities", "AAPL US Equity")
        request.append("fields", "NAME")
        session.sendRequest(request)
        while True:
            event = session.nextEvent(10_000)
            print("EVENT", event.eventType())
            for message in event:
                print(message.toString())
            if event.eventType() == blpapi.Event.RESPONSE:
                break
    finally:
        session.stop()


if __name__ == "__main__":
    main()
