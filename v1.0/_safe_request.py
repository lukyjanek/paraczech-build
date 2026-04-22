#!/usr/bin/env python3
# coding: utf-8

import time
import requests


session = requests.Session()


def safe_api_call(url, params, max_retries=5, initial_wait=0.05):
    """
    Request API and catch HTTPS 429 (Too many requests), plus waits a bit.
    """
    wait = initial_wait

    for attempt in range(max_retries):
        time.sleep(wait)

        try:
            response = session.get(url, params=params, timeout=10)

            # HTTPS 429 (Too Many Requests)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                print(f"Status 429: Above limit. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            wait_time = 2 ** attempt
            print(f"Network error ({e}). Try n. {attempt+1}/{max_retries}. Waiting {wait_time}s...")
            time.sleep(wait_time)

    return None
