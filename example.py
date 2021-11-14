#!/usr/bin/env python
"""Basic usage example and testing of kostal."""
import asyncio
import logging

import aiohttp

import kostal


async def main(loop, host):
    async with aiohttp.ClientSession(loop=loop) as session:
        inverter = kostal.Piko(session, host)

        res = await inverter.day_yield()
        print(f"day yield: {res}")

        res = await inverter.get_info_inverter()
        print(f"all inverter info: {res}")

        res = await inverter.get_all_entries()
        print(f"all entries: {res}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, "http://192.168.178.86"))
