import requests
from http import HTTPStatus
from tqdm import tqdm
from requests.exceptions import HTTPError, Timeout, RequestException


def get_token() -> str | None:
    """
    Sends a POST request to retrieve a token needed for the download of the csv.
    :return: The response token from the server.
    :raises requests.HTTPError: For HTTP-related errors.
    :raises requests.Timeout: If the request times out.
    :raises requests.RequestException: For other request-related errors.
    """
    url = "https://fioriappslibrary.hana.ondemand.com/sap/fix/externalViewer/services/downloadApplistHelper.xsjs"
    payload = {
        "U": "1NA",
        "FS": "1NA",
        "BS": "1NA",
        "H": "1NA",
        "isDownload": "true",
        "FIT": "false",
        "productSuite": "SAP S/4HANA (Private Cloud and OP)",
        "whereClause": "%20where%20(%20%201%3D1%20%20)%20%20and%20(%20%22releaseGroupText%22%20%3D%20'SAP%20S%2F4HANA%20(Private%20Cloud%20and%20On-Premise)'%20)%20",
        "userLang": "None",
        "columns": [
            "fioriId",
            "RoleNameBusinessDescCombo",
            "AppName",
            "ApplicationType",
            "CombinedTitle",
            "highlightKey",
            "FormFactors",
            "ProductCategory",
            "Database",
            "GTMAppDescription",
        ],
        "variantSelected": "*standard*",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, json=payload)
    response.raise_for_status()
    return response.text


def download_csv(token: str) -> bytes | None:
    """
    Downloads a csv file containing all fiori applications from the fiori app library.
    :param token: The token needed to download the csv file from the fiori app library.
    :return: The downloaded file content as bytes, or None if the download fails.
    :raises requests.exceptions.RequestException: If there is an issue with the network request.
    :raises ValueError: If the content-length header is not present or invalid.
    :raises Exception: For any other unexpected errors.
    """
    url = f"https://fioriappslibrary.hana.ondemand.com/sap/fix/externalViewer/services/downloadResult.xsjs?id={token}"
    response = requests.request("GET", url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    content = bytearray()
    with tqdm(total=total_size, unit="B", unit_scale=True, desc="Downloading") as progress_bar:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            content.extend(data)
    response.raise_for_status()
    return bytes(content)


def download_fiori_apps_csv():
    """
    Downloads a csv file containing all fiori applications from the fiori app library.
    :return: The downloaded file content as bytes, or None if the download fails.
    :raises requests.exceptions.RequestException: If there is an issue with the network request.
    :raises ValueError: If the content-length header is not present or invalid.
    :raises Exception: For any other unexpected errors.
    """
    token = get_token()
    return download_csv(token)  # type: ignore
