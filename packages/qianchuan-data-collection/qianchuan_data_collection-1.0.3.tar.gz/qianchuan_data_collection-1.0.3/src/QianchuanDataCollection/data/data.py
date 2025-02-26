"""
数据模块页面采集
"""

from DrissionPage import Chromium

from .site_promotion import SitePromotion


class Data:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._site_promotion = None

    @property
    def site_promotion(self):
        if not self._site_promotion:
            self._site_promotion = SitePromotion(self._browser)

        return self._site_promotion
