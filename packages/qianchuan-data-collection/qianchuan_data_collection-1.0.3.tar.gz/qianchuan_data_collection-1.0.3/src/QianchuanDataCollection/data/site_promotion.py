"""
全域推广数据采集
"""

from contextlib import suppress

from DrissionPage import Chromium
from DrissionPage._pages.mix_tab import MixTab

from .._browser_utils import BrowserUtils
from .._utils import Utils
from ._dict import Dictionary
from ._utils import (
    download__report,
    pick__custom_date_range,
    pick__custom_statistic_dimension,
)


class Urls:
    push_live = 'https://qianchuan.jinritemai.com/dataV2/bidding/site-promotion?aavid=1752642459218957&tabs=live'
    push_product = 'https://qianchuan.jinritemai.com/dataV2/bidding/site-promotion?aavid=1752642459218957&tabs=product'


class DataPacketUrl:
    general_query = 'qianchuan.jinritemai.com/ad/api/data/v1/common/statQuery'
    """通用数据查询接口"""


class SitePromotion:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def _wait__general_query_packet(
        self, page: MixTab, req_from: str, data_set_key: str, timeout: float = None
    ):
        """
        等待通用数据查询接口数据包监听返回
        - 需要手动开启数据包监听
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        packet = None
        for item in page.listen.steps(count=None, gap=1, timeout=_timeout):
            reqdata: dict = item.request.postData
            query: dict = item.request.params
            if reqdata.get('DataSetKey') != data_set_key:
                continue

            if query.get('reqFrom') != req_from:
                continue

            packet = item
            break

        return packet

    def _wait__push_live__overview_packet(self, page: MixTab, timeout: float = None):
        """等待推直播-投后数据-抖音号 数据概览数据包监听返回"""

        return self._wait__general_query_packet(
            page, 'uniOverviewTrendchart', 'site_promotion_post_overview', timeout
        )

    def _wait__push_product__overview_packet(self, page: MixTab, timeout: float = None):
        """等待推商品-商品 数据概览数据包监听返回"""

        return self._wait__general_query_packet(
            page, 'overviewTrend-product', 'site_promotion_product_product', timeout
        )

    def get__push_live__overview(
        self, begin_date: str, end_date: str, timeout: float = None, raw=False
    ):
        """获取推直播-投后数据-抖音号 数据概览"""

        page = BrowserUtils.get__main_page(self._browser)
        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        page.get(Urls.push_live)
        if not self._wait__push_live__overview_packet(page, timeout):
            raise RuntimeError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        pick__custom_date_range(begin_date, end_date, page)
        packet = self._wait__push_live__overview_packet(page, timeout)
        if not packet:
            raise RuntimeError('修改日期后获取数据包超时')

        resp: dict = packet.response.body
        if 'data' not in resp:
            raise ValueError('在数据包中未找到 data 字段')
        data: dict = resp.get('data')
        if raw is True:
            return data

        if not data or not isinstance(data, dict):
            raise ValueError('数据包中的 data 字段为空或不是预期的 dict 类型')

        if 'StatsData' not in data:
            raise ValueError('在数据包中未找到 data.StatsData 字段')
        stats_data: dict = data.get('StatsData')
        if not stats_data or not isinstance(stats_data, dict):
            raise ValueError('数据包中的 data.StatsData 字段为空或不是预期的 dict 类型')

        if 'Totals' not in stats_data:
            raise ValueError('在数据包中未找到 data.StatsData.Totals 字段')
        totals: dict = stats_data.get('Totals')
        if not totals or not isinstance(totals, dict):
            raise ValueError(
                '数据包中的 data.StatsData.Totals 字段为空或不是预期的 dict 类型'
            )

        record = Utils.dict_mapping(
            totals, Dictionary.site_promotion.push_live__overview
        )
        record = {k: v.get('Value') for k, v in record.items()}

        return record

    def get__push_live__material__detail(
        self, begin_date: str, end_date: str, timeout: float = None, raw=False
    ):
        """
        获取推直播-投后数据-素材-视频 表格数据

        Args:
            raw: 如果为 True 则返回下载报表的文件路径, 否则返回处理后的数据字典列表
        """

        page = BrowserUtils.get__main_page(self._browser)
        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        page.get(Urls.push_live)
        if not self._wait__push_live__overview_packet(page, timeout):
            raise RuntimeError('首次进入页面获取数据包超时')

        data_dimension_btn_ele = page.ele(
            't:div@@class^ovui-radio-item@@text()= 素材 ', timeout=3
        )
        if not data_dimension_btn_ele:
            raise ValueError('未找到数据维度 [素材] 按钮')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        data_dimension_btn_ele.click(by_js=True)
        if not self._wait__general_query_packet(
            page, 'unitable', 'site_promotion_post_data_live', timeout
        ):
            raise RuntimeError('点击数据维度 [素材] 按钮后获取数据包超时')

        data_type_btn_ele = page.ele(
            't:div@@class^ovui-radio-item@@text()= 视频 ', timeout=3
        )
        if not data_type_btn_ele:
            raise ValueError('未找到数据类型 [视频] 按钮')

        def wait_detail_packet():
            """等待视频详情数据包监听返回"""
            return self._wait__general_query_packet(
                page, 'unitable', 'site_promotion_post_data_video', timeout
            )

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        data_type_btn_ele.click(by_js=True)
        if not wait_detail_packet():
            raise RuntimeError('点击数据类型 [视频] 按钮后获取数据包超时')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        pick__custom_date_range(begin_date, end_date, page)
        if not wait_detail_packet():
            raise RuntimeError('修改日期后获取数据包超时')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        pick__custom_statistic_dimension(page, '汇总')
        if not wait_detail_packet():
            raise RuntimeError('修改统计维度为 [汇总] 后获取数据包超时')

        report_path = download__report(page)
        if raw is True:
            return report_path

        raw_data_list = Utils.xlsx_read(report_path)
        data_list: list[dict] = []
        for data in raw_data_list:
            _record = Utils.dict_format__strip(data, suffix=['%'])
            _record = Utils.dict_format__number(_record)
            data_list.append(_record)

        Utils.file_remove(report_path)

        return data_list

    def get__push_product__overview(
        self, begin_date: str, end_date: str, timeout: float = None, raw=False
    ):
        """获取推商品-商品 数据概览"""

        page = BrowserUtils.get__main_page(self._browser)
        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        page.get(Urls.push_product)
        if not self._wait__push_product__overview_packet(page, timeout):
            raise RuntimeError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        pick__custom_date_range(begin_date, end_date, page)
        packet = self._wait__push_product__overview_packet(page, timeout)
        if not packet:
            raise RuntimeError('修改日期后获取数据包超时')

        resp: dict = packet.response.body
        if 'data' not in resp:
            raise ValueError('在数据包中未找到 data 字段')
        data: dict = resp.get('data')
        if raw is True:
            return data

        if not data or not isinstance(data, dict):
            raise ValueError('数据包中的 data 字段为空或不是预期的 dict 类型')

        if 'StatsData' not in data:
            raise ValueError('在数据包中未找到 data.StatsData 字段')
        stats_data: dict = data.get('StatsData')
        if not stats_data or not isinstance(stats_data, dict):
            raise ValueError('数据包中的 data.StatsData 字段为空或不是预期的 dict 类型')

        if 'Totals' not in stats_data:
            raise ValueError('在数据包中未找到 data.StatsData.Totals 字段')
        totals: dict = stats_data.get('Totals')
        if not totals or not isinstance(totals, dict):
            raise ValueError(
                '数据包中的 data.StatsData.Totals 字段为空或不是预期的 dict 类型'
            )

        record = Utils.dict_mapping(
            totals, Dictionary.site_promotion.push_product__overview
        )
        record = {k: v.get('Value') for k, v in record.items()}

        return record

    def get__push_product__material__detail(
        self, begin_date: str, end_date: str, timeout: float = None, raw=False
    ):
        """
        获取推商品-素材 表格数据

        Args:
            raw: 如果为 True 则返回下载报表的文件路径, 否则返回处理后的数据字典列表
        """

        page = BrowserUtils.get__main_page(self._browser)
        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        page.get(Urls.push_product)
        if not self._wait__push_product__overview_packet(page, timeout):
            raise RuntimeError('首次进入页面获取数据包超时')

        def wait_detail_packet():
            """等待视频详情数据包监听返回"""
            return self._wait__general_query_packet(
                page,
                'productListTable',
                'site_promotion_product_post_data_video',
                timeout,
            )

        data_dimension_btn_eles = page.eles(
            't:div@@class^ovui-radio-item@@text()= 素材 ', timeout=8
        )
        data_dimension_btn_ele = None
        for ele in data_dimension_btn_eles:
            with suppress(Exception):
                assert ele.rect.size
                data_dimension_btn_ele = ele
                break
        if not data_dimension_btn_ele:
            raise ValueError('未找到数据维度 [素材] 有效的可点击的按钮元素')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        data_dimension_btn_ele.click(by_js=True)
        if not wait_detail_packet():
            raise RuntimeError('点击数据维度 [素材] 按钮后获取数据包超时')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        pick__custom_date_range(begin_date, end_date, page)
        if not wait_detail_packet():
            raise RuntimeError('修改日期后获取数据包超时')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        pick__custom_statistic_dimension(page, '汇总')
        if not wait_detail_packet():
            raise RuntimeError('修改统计维度为 [汇总] 后获取数据包超时')

        report_path = download__report(page)
        if raw is True:
            return report_path

        raw_data_list = Utils.xlsx_read(report_path)
        data_list: list[dict] = []
        for data in raw_data_list:
            _record = Utils.dict_format__strip(data, suffix=['%'])
            _record = Utils.dict_format__number(_record)
            data_list.append(_record)

        Utils.file_remove(report_path)

        return data_list
