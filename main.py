from httpx import URL

from net.CanvasClient import CanvasClient
from util import AppSettings

client = CanvasClient(canvas_url=URL(AppSettings.canvas_url()), api_key=AppSettings.canvas_api_key())