import os
import json
import logging
import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
STATION_NAME_FILTER = os.getenv("STATION_NAME_FILTER", "BNA12").upper()
BOUND_BOX = json.loads(os.getenv("BOUND_BOX_JSON"))

def lambda_handler(event, context):
    url = "https://account.chargepoint.com/map-prod/v2/station_list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": "https://account.chargepoint.com/map.html",
        "Origin": "https://account.chargepoint.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9"
    }

    payload = {
        "screen_width": 1206,
        "screen_height": 473,
        "page_size": 20,
        "page_offset": "",
        "sort_by": "distance",
        "include_map_bound": True,
        "reference_lat": (BOUND_BOX["ne_lat"] + BOUND_BOX["sw_lat"]) / 2,
        "reference_lon": (BOUND_BOX["ne_lon"] + BOUND_BOX["sw_lon"]) / 2,
        "filter": {"status_available": True},
        "bound_output": True,
        "ne_lat": BOUND_BOX["ne_lat"],
        "ne_lon": BOUND_BOX["ne_lon"],
        "sw_lat": BOUND_BOX["sw_lat"],
        "sw_lon": BOUND_BOX["sw_lon"]
    }

    logger.info("Polling ChargePoint API...")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        logger.info(f"Response status: {resp.status_code}")
        logger.info(f"Response body: {resp.text[:200]}...")  # Log first 200 chars
        
        # If we got a successful response, process it
        if resp.status_code == 200:
            data = resp.json()
            matching = [s for s in data.get("station_list", []) if STATION_NAME_FILTER in s.get("name", "").upper()]
            logger.info(f"Found {len(matching)} matching available stations.")

            if matching and SNS_TOPIC_ARN:
                sns = boto3.client("sns")
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="🚗 Charger Available",
                    Message=json.dumps(matching, indent=2)
                )
        else:
            logger.error(f"API request failed with status code: {resp.status_code}")
            
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return
