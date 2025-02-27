#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 10 2025.

@author: npappin-wsu
@license: MIT

Updated on Feb 11 2025.
"""

from . import logger, session, metadata, bdcCache
import pandas as pd
import json, zipfile, io
from pprint import pprint

# from . import config


class availability:

    def state(
        states: int | str | list = "53",
        technology: int | str | list = "50",
        release: str | list = "2024-06-30",
        cache=False,
    ) -> pd.DataFrame:
        logger.info("Collecting availability...")
        logger.debug(f"State: {states}")
        logger.debug(f"Technology: {technology}")
        logger.debug(f"Release: {release}")
        # TODO: Handle no data here
        
        if type(states) is not list:
            states = [states]
        if type(technology) is not list:
            technology = [technology]
        if type(release) is not list:
            release = [release]
        # TODO: Add normalization code here

        # Retrieve availability data
        availability = dict()
        for r in release:
            response = session.get(
                f"https://broadbandmap.fcc.gov/api/public/map/downloads/listAvailabilityData/{r}"
            )
            if response.status_code != 200:
                logger.error(f"Failed to retrieve availability data for {r}.")
                raise Exception(f"Failed to retrieve availability data for {r}.")
            # TODO: adding dtype hints here I think would be helpful.
            availability[r] = pd.DataFrame.from_dict(response.json()["data"])
        df = pd.DataFrame()
        for r in release:
            rlocal = availability[r]
            items = rlocal[
                (rlocal.category == "State")
                & (rlocal.state_fips.isin(states))
                & (rlocal.technology_code.isin(technology))
            ].to_dict("records")
            for item in items:
                logger.debug(
                    f"State: {item['state_name']}, Technology: {item['technology_code']}, Release: {r}"
                )
                # FUCK I DONT LIKE THIS
                if cache and bdcCache.check(item["file_name"]):
                    data = bdcCache.get(item["file_name"])
                    logger.debug("Cache hit!")
                    pass
                else:
                    response = session.get(
                        f"https://broadbandmap.fcc.gov/api/public/map/downloads/downloadFile/availability/{item['file_id']}"
                    )
                    if response.status_code == 200 and cache:
                        bdcCache.save(item["file_name"], response.content)
                    data = response.content
                if response.status_code != 200:
                    logger.error(
                        f"Failed to retrieve availability data for {item['state_name']} and {item['technology_code']} in {r}."
                    )
                    raise Exception(
                        f"Failed to retrieve availability data for {item['state_name']} and {item['technology_code']} in {r}."
                    )
                else:
                    zip = zipfile.ZipFile(io.BytesIO(data))
                    localdf = pd.read_csv(
                        zip.open(zip.filelist[0].filename)
                    )  # , dtype=columnHints)
                    df = pd.concat([df, localdf], ignore_index=True)
        logger.debug(f"State: {states}, Technology: {technology}, Release: {release}")
        return df


def echo(message):
    logger.info(message)
    print(message)
    pass


def main():
    logger.info("Starting the application...")
    # Your code here


if __name__ == "__main__":
    main()
