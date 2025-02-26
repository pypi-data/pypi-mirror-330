"""
商家后台-数据中心数据采集器
"""

from DrissionPage import Chromium
from PxxFontDecrypt.decrypt import FontDecrypter

from .._utils import Utils
from ._dict import Dictionary
from ._utils import Pagination, download__font, pick__custom_date


class Urls:
    flow_plate = (
        'https://mms.pinduoduo.com/sycm/search_data/plate?dateFlag=5&day={date}'
    )
    goods_effect = 'https://mms.pinduoduo.com/sycm/goods_effect?msfrom=mms_sidenav'
    transaction__overview = (
        'https://mms.pinduoduo.com/sycm/stores_data/operation?dateFlag=5&day={date}'
    )
    service__comment = (
        'https://mms.pinduoduo.com/sycm/goods_quality/comment?dateFlag=5&day={date}'
    )
    service__exp = 'https://mms.pinduoduo.com/sycm/goods_quality/help'
    service__detail = (
        'https://mms.pinduoduo.com/sycm/goods_quality/detail?dateFlag=5&day={date}'
    )


class DataPacketUrls:
    flow_plate__overview = (
        'mms.pinduoduo.com/sydney/api/mallFlow/queryMallFlowOverViewList'
    )
    goods_effect__overview = (
        'mms.pinduoduo.com/sydney/api/goodsDataShow/queryGoodsPageOverView'
    )
    goods_effect__detail = '/sydney/api/goodsDataShow/queryGoodsDetailVOListForMMS'
    transaction__overview = 'mms.pinduoduo.com/sydney/api/mallTrade/queryMallTradeList'
    service__comment__overview = (
        'mms.pinduoduo.com/sydney/api/saleQuality/queryMallDsrVO'
    )
    service__exp__overview = (
        'mms.pinduoduo.com/sydney/api/mallService/getMallServeScoreV2'
    )
    service__detail__overview = (
        'mms.pinduoduo.com/sydney/api/saleQuality/querySaleQualityDetailInfo'
    )


class DataCenter:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def get__flow_plate__overview(
        self, date: str, timeout: float = None, raw=False
    ) -> dict | None:
        """
        [流量数据-流量看板-数据概览] 数据获取

        Args:
            date: 日期，格式：YYYY-MM-DD
            timeout: 超时时间，默认 15 秒
            raw: 是否返回原始数据，默认 False
        Returns:
            看板数据
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.flow_plate__overview,
            method='POST',
            res_type='Fetch',
        )

        uri = Urls.flow_plate.format(date=date)
        page.get(uri)

        packet = page.listen.wait(timeout=_timeout)

        page.close()

        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: list[dict] = resp.get('result')
        if not result or not isinstance(result, list):
            raise TypeError('数据包中的 result 字段空的或不是预期的 list 类型')

        target_record: dict = next(
            filter(lambda x: x.get('statDate') == date, result), None
        )
        if not target_record or raw is True:
            return target_record

        record = Utils.dict_mapping(
            target_record, Dictionary.data_center.flow_plate__overview
        )
        record = Utils.dict_format__ratio(record, fields=['成交转化率'])
        record = Utils.dict_format__round(
            record, fields=['成交转化率', '客单价', '成交UV价值']
        )

        return record

    def get__goods_effect__overview(self, date: str, timeout: float = None, raw=False):
        """
        [商品数据-商品概况] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods_effect__overview + '$',
            is_regex=True,
            method='POST',
            res_type='Fetch',
        )
        page.get(Urls.goods_effect)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrls.goods_effect__overview + '$',
            is_regex=True,
            method='POST',
            res_type='Fetch',
        )
        if Utils.date_yesterday() == date:
            yesterday_btn = page.ele('t:label@@text()=昨日', timeout=2)
            yesterday_btn.click(by_js=True)
        else:
            pick__custom_date(date=date, page=page)

        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('获取数据包超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段不是预期的 dict 类型')

        # 下载加密字体
        font_filepath = download__font(page=page)
        font_decrypter = FontDecrypter(font_path=font_filepath)

        record: dict[str, str] = {}
        for field, value in result.items():
            if not isinstance(value, str):
                continue

            record[field] = font_decrypter.decrypt(value)

        page.close()

        if raw is True:
            return record

        record = Utils.dict_mapping(
            record, Dictionary.data_center.goods_effect__overview
        )
        record = Utils.dict_format__strip(record, fields=['成交转化率'], suffix=['%'])
        record = Utils.dict_format__number(record)

        return record

    def get__goods_effect__detail(
        self,
        goods_ids: list[str],
        date: str,
        timeout: float = None,
        set_max_page=False,
        raw=False,
    ):
        """
        [商品数据-商品明细] 数据获取

        Args:
            goods_ids: 商品 ID 列表
            date: 日期，格式：YYYY-MM-DD
            timeout: 超时时间，默认 15 秒
            set_max_page: 是否设置最大页码，默认 False
            raw: 是否返回原始数据，默认 False
        Returns:
            商品明细数据 {'商品ID': {'字段1': '值1', '字段2': '值2',...}}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods_effect__detail,
            method='POST',
            res_type='Fetch',
        )
        page.get(Urls.goods_effect)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('首次进入页面获取数据包超时')

        if not page.ele(
            't:span@@class^goods-content_tabLabel@@text()=商品明细', timeout=2
        ):
            raise RuntimeError('未找到商品明细选项卡')

        tab_container = page.ele('c:div[class^=goods-content_goodsContent]', timeout=5)
        if not tab_container:
            raise RuntimeError('未找到商品明细数据容器')

        # ========== 输入多个商品ID ==========
        goods_ids_str = ','.join([str(goods_id) for goods_id in goods_ids])
        goods_id_input = tab_container.ele(
            't:input@placeholder^请输入商品ID查询', timeout=2
        )
        if not goods_id_input:
            raise RuntimeError('未找到商品ID输入框')

        goods_id_input.input(goods_ids_str, clear=True)
        # ========== 输入多个商品ID ==========

        packet = None
        page.listen.start(
            targets=DataPacketUrls.goods_effect__detail,
            method='POST',
            res_type='Fetch',
        )
        if Utils.date_yesterday() == date:
            # 若获取昨日数据，则直接点击 [昨日] 按钮
            yesterday_btn = tab_container.ele('t:label@@text()=昨日', timeout=2)
            yesterday_btn.click(by_js=True)
        else:
            pick__custom_date(date=date, page=page, container=tab_container)

        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise RuntimeError('获取商品明细数据超时')

        # ========== 修改页码最大值 ==========
        if set_max_page is True:
            page.listen.start(
                targets=DataPacketUrls.goods_effect__detail,
                method='POST',
                res_type='Fetch',
            )
            Pagination.set__max_page_size(page=page)
            packet = page.listen.wait(timeout=_timeout)
            if not packet:
                raise RuntimeError('修改页码后获取商品明细数据超时')
        # ========== 修改页码最大值 ==========

        resp: dict = packet.response.body
        result: dict = resp.get('result')
        if not result:
            raise ValueError('数据包中未找到 result 字段')

        goods_detail_list: list[dict] = result.get('goodsDetailList')
        if not goods_detail_list or not isinstance(goods_detail_list, list):
            raise ValueError('数据包中未找到 result.goodsDetailList 字段或非 list 格式')

        # 下载加密字体
        font_filepath = download__font(page=page)
        font_decrypter = FontDecrypter(font_path=font_filepath)

        records: dict[str, dict] = {}
        for item in goods_detail_list:
            for field, value in item.items():
                if not isinstance(value, str):
                    continue

                item[field] = font_decrypter.decrypt(value)

            records[str(item.get('goodsId'))] = item

        if raw is True:
            return records

        for goods_id, record in records.items():
            _record = Utils.dict_mapping(
                record, Dictionary.data_center.goods_effect__detail
            )
            _record = Utils.dict_format__strip(
                _record, fields=['成交转化率', '下单率', '成交率'], suffix=['%']
            )
            _record = Utils.dict_format__number(_record)
            _record = Utils.dict_format__round(_record)
            records[goods_id] = _record

        page.close()

        return records

    def get__transaction__overview(self, date: str, timeout: float = None, raw=False):
        """
        [交易数据-交易概况-数据概览] 数据获取

        Args:
            date: 日期，格式：YYYY-MM-DD
            timeout: 超时时间，默认 15 秒
            raw: 是否返回原始数据，默认 False
        Returns:
            交易概况数据
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.transaction__overview,
            method='POST',
            res_type='Fetch',
        )
        uri = Urls.transaction__overview.format(date=date)
        page.get(uri)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')
        result = resp['result']
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段非预期的 dict 类型')
        if 'dayList' not in result:
            raise ValueError('数据包中未找到 result.dayList 字段')
        day_list: list[dict] = result['dayList']
        if not isinstance(day_list, list):
            raise TypeError('数据包中的 result.dayList 字段非预期的 list 类型')

        record = next(filter(lambda x: x.get('stateDate') == date, day_list), None)

        page.close()

        if raw is True:
            return record

        record = Utils.dict_mapping(
            record, Dictionary.data_center.transaction__overview
        )
        record = Utils.dict_format__ratio(
            record, fields=['成交转化率', '成交老买家占比']
        )
        record = Utils.dict_format__round(record)

        return record

    def get__service__comment__overview(
        self, date: str, timeout: float = None, raw=False
    ):
        """
        [服务数据-评价数据-总览] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.service__comment__overview + '$',
            is_regex=True,
            method='POST',
            res_type='Fetch',
        )
        uri = Urls.service__comment.format(date=date)
        page.get(uri)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not result:
            raise ValueError('数据包中未找到 result 字段')
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(
            result, Dictionary.data_center.service__comment__overview
        )
        record = Utils.dict_format__round(record, fields=['店铺评价分'])

        return record

    def get__service__exp__overview(self, timeout: float = None, raw=False):
        """
        [服务数据-消费者体验指标-概览] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.service__exp__overview,
            method='POST',
            res_type='Fetch',
        )
        page.get(Urls.service__exp)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(
            result, Dictionary.data_center.service__exp__overview
        )
        record = Utils.dict_format__round(
            record, fields=['消费者服务体验分'], precision=1
        )

        return record

    def get__service__detail__overview(
        self, date: str, timeout: float = None, raw=False
    ):
        """
        [服务数据-售后数据-整体情况] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.service__detail__overview,
            method='POST',
            res_type='Fetch',
        )
        uri = Urls.service__detail.format(date=date)
        page.get(uri)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(
            result, Dictionary.data_center.service__detail__overview
        )
        record = Utils.dict_format__ratio(
            record, fields=['纠纷退款率', '平台介入率', '品质退款率', '成功退款率']
        )
        record = Utils.dict_format__round(
            record, fields=['纠纷退款率', '平台介入率', '品质退款率', '成功退款率']
        )

        return record
