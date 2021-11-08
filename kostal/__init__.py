#!/usr/bin/env python3

from typing import List

import aiohttp
import async_timeout
import asyncio
import json
import operator

from kostal import const

DXS_ENDPOINT = "/api/dxs.json"
LOG_DATA_ENDPOINT = "/LogDaten.dat"

DEFAULT_USERNAME = "pvserver"
DEFAULT_PASSWORD = "pvwr"


class DxsEntry:
    def __init__(self, dxsId, value):
        super().__init__()
        self.dxsId = dxsId
        self.value = value

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class DxsSessionData:
    def __init__(self, sessionId, roleId):
        super().__init__()
        self.session_id = sessionId
        self.role_id = roleId

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class DxsStatus:
    def __init__(self, code):
        super().__init__()
        self.code = code

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class DxsResponse:
    __dxs_entries: List[DxsEntry]
    session: DxsSessionData
    status: DxsStatus

    def __init__(self, dxsEntries, session, status):
        super().__init__()
        self.__dxs_entries = list(map(DxsEntry.from_json, dxsEntries))
        self.__session = DxsSessionData.from_json(session)
        self.status = DxsStatus.from_json(status)

    def get_entry_by_id(self, dxs_id: []):
        entries_by_id = []
        for i in self.__dxs_entries:
            if i.dxsId in dxs_id:
                entries_by_id.append(i)
        return entries_by_id

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class Piko:
    """
    Interface to communicate with the Kostal Piko over http request
    Attributes:
        session     The AIO session
        url         the url for reaching of the inverter
                    (i.e. http://192.168.0.123)
        username    inverter username (default pvserver)
        password    inverter password (default pvwr)
        timeout     HTTP timeout in seconds
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        url: str = None,
        username: str = DEFAULT_USERNAME,
        password: str = DEFAULT_PASSWORD,
        timeout: int = 10,
    ):
        """Constructor"""
        if url is None:
            raise ValueError("Parameter url can not be None")

        self.__client = session
        self.__url = url + DXS_ENDPOINT
        self.__username = username
        self.__password = password
        self.__timeout = timeout

    async def __fetch_data(self, request_params):
        """fetch data"""
        auth = aiohttp.BasicAuth(self.__username, self.__password)
        try:
            async with async_timeout.timeout(self.__timeout):
                async with self.__client.get(
                    self.__url, params=request_params, auth=auth, timeout=self.__timeout
                ) as resp:
                    assert resp.status == 200
                    return await resp.json(content_type="text/plain")
        except (asyncio.TimeoutError, aiohttp.ClientError):
            raise ConnectionError(
                "Connection to Kostal device failed at {}.".format(self.__url)
            )
        except json.JSONDecodeError:
            raise ValueError(
                "Device returned a non-JSON reply at {}.".format(self.__url)
            )

    async def __fetch_dxs_entry(self, entry_ids: []):
        if len(entry_ids) > 0:
            # Kostal API is only returning max 25 entries - if entry_ids contains more than 25 entries we will split up the request
            splits = round(len(entry_ids) / 25) + 1
            dxsEntries_result = {"dxsEntries": [], "session": {}, "status": {}}
            for i in range(0, splits):
                request_params = []
                split_start = i * 25
                split_end = (i + 1) * 25
                for k in range(split_start, split_end):
                    if k < len(entry_ids):
                        request_params.append(("dxsEntries", entry_ids[k]))
                        # print(request_params)
                    else:
                        break
                # Check if any request_params (dxsId) is given, otherwise don't call the API
                if len(request_params) > 0:
                    r = await self.__fetch_data(request_params)
                    dxsEntries_result["dxsEntries"].extend(r["dxsEntries"])
                    dxsEntries_result["session"] = r["session"]
                    dxsEntries_result["status"] = r["status"]

            return DxsResponse(**dxsEntries_result).get_entry_by_id(entry_ids)

    def __generate_query_results(self, dxs_entries, query_object):
        query_results = {}
        found_matching_entry = False
        for dxs_entry in dxs_entries:
            print("Searching for ", dxs_entry.dxsId)
            for groupname, group_dxs_entries in query_object.items():
                print("Checking ", groupname)
                for (
                    query_dxs_entryname,
                    query_dxs_entryvalues,
                ) in group_dxs_entries.items():
                    if query_dxs_entryvalues["dxsId"] == dxs_entry.dxsId:
                        query_dxs_entryvalues["value"] = dxs_entry.value
                        if not groupname in query_results:
                            query_results.update({groupname: {}})
                        query_results[groupname].update(
                            {query_dxs_entryname: query_dxs_entryvalues}
                        )
                        found_matching_entry = True
                        print("Found Matching entry for ", query_dxs_entryvalues)
                        break

                if found_matching_entry:
                    found_matching_entry = False
                    break
        print(query_results)
        return query_results

    def __get_all_dxsIds(self, query_elements):
        dxsIds = []
        found_matching_entry = False
        for group in query_elements.values():
            for query_dxs_entryvalues in group.values():
                print("Checking ", query_dxs_entryvalues)
                dxsIds.append(query_dxs_entryvalues["dxsId"])
        print(dxsIds)
        return dxsIds

    async def day_yield(self):
        query_elements = {"StatisticDay": const.StatisticDay}
        entry_ids = [query_elements["StatisticDay"]["Yield"]["dxsId"]]
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_all(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "ActualAnalogInputs": const.ActualAnalogInputs,
            "ActualBattery": const.ActualBattery,
            "ActualGrid": const.ActualGrid,
            "ActualHouse": const.ActualHouse,
            "ActualPVGenerator": const.ActualPVGenerator,
            "ActualSZeroIn": const.ActualSZeroIn,
            "Home": const.Home,
            "InfoVersions": const.InfoVersions,
            "InfoInverter": const.InfoInverter,
            "StatisticDay": const.StatisticDay,
            "StatisticTotal": const.StatisticTotal,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_actual_analog_inputs(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "ActualAnalogInputs": const.ActualAnalogInputs,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_actual_battery(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "ActualBattery": const.ActualBattery,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_actual_grid(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "ActualGrid": const.ActualGrid,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_actual_house(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "ActualHouse": const.ActualHouse,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_actual_pv_generator(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "ActualPVGenerator": const.ActualPVGenerator,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_actual_szero_in(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "ActualSZeroIn": const.ActualSZeroIn,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_actual_home(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "Home": const.Home,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_info_versions(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "InfoVersions": const.InfoVersions,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_info_inverter(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "InfoInverter": const.InfoInverter,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_statistic_day(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "StatisticDay": const.StatisticDay,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result

    async def get_statistic_total(self):
        # Build List of elements that should be queried. This will be the structure for the response
        query_elements = {
            "StatisticTotal": const.StatisticTotal,
        }
        entry_ids = self.__get_all_dxsIds(query_elements)
        dxs_entries = await self.__fetch_dxs_entry(entry_ids)
        query_result = self.__generate_query_results(dxs_entries, query_elements)
        return query_result
