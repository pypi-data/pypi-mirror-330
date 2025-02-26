from tempfile import gettempdir
from time import sleep
from uuid import uuid4

from DrissionPage._pages.mix_tab import MixTab
from DrissionPage._units.downloader import DownloadMission


def pick__custom_date_range(begin_date: str, end_date: str, page: MixTab):
    """选择自定义日期范围"""

    date_picker_ele = page.ele(
        't:input@@class=ovui-input@@placeholder=开始日期', timeout=3
    )
    date_picker_ele.click(by_js=True)
    sleep(0.8)
    for date in [begin_date, end_date]:
        date_cell_ele = page.ele(
            f't:td@@class^ovui-date__cell@@title={date}',
            timeout=2,
        )
        if not date_cell_ele:
            raise ValueError(f'日期范围选择其中 {date} 选项不存在')

        date_cell_ele.click(by_js=True)
        sleep(0.3)


def pick__custom_statistic_dimension(page: MixTab, dimension_name: str):
    """
    修改指定统计维度

    Args:
        dimension_name: 统计维度名称
    """

    picker_ele = page.ele(
        'c:input[class="ovui-input"][placeholder="请选择"]', timeout=3
    )
    if not picker_ele:
        raise RuntimeError('未找到 [统计维度] 选择器元素')

    picker_ele.click(by_js=True)
    sleep(0.8)

    type_ele = page.ele(
        f't:span@@class^oc-typography@@text()={dimension_name}', timeout=3
    )
    if not type_ele:
        raise RuntimeError(f'未找到 [统计维度-{dimension_name}] 选项元素')

    type_ele.click(by_js=True)


def download__report(page: MixTab, timeout: float = None):
    """
    下载报表文件

    Returns:
        下载后的文件路径
    """

    download_btn_ele = page.ele('c:div.oc-button-wrap.download-btn', timeout=3)
    if not download_btn_ele:
        raise RuntimeError('未找到 [下载] 按钮元素')

    _timeout = timeout if isinstance(timeout, (int, float)) else 120

    download_mission: DownloadMission = download_btn_ele.child(
        't:button'
    ).click.to_download(
        save_path=gettempdir(),
        rename=str(uuid4()),
        by_js=True,
        timeout=_timeout,
    )
    download_mission.wait()

    if download_mission.state != 'completed':
        raise RuntimeError('报表文件下载失败')

    return download_mission.final_path
