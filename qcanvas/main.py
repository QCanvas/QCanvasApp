from httpx import URL

from net.canvas_client import CanvasClient
from util import AppSettings

client = CanvasClient(canvas_url=URL(AppSettings.canvas_url()), api_key=AppSettings.canvas_api_key())