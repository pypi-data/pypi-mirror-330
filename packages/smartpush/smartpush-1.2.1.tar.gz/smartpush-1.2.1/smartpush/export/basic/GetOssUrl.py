import json
import urllib

import requests
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
from smartpush.utils.StringUtils import StringUtils


# 用于技术第几次重试，无需修改
def log_attempt(retry_state):
    """
    回调函数，在每次重试时记录并打印重试次数
    """
    attempt_number = retry_state.attempt_number
    print(f"当前重试次数: {attempt_number}")


def get_oss_address_with_retry(target_id, url, requestHeader, requestParam, **kwargs) -> str:
    """
    创建带有动态重试配置的获取 OSS 地址
    **kwargs 可传参：tries=10, delay=2, backoff=1
    :param requestParam:
    :param url:
    :param target_id:
    :param requestHeader:
    :return: 带有重试配置的获取 OSS 地址的
    """
    tries = kwargs.get('tries', 20)  # 重试次数
    delay = kwargs.get('delay', 2)

    @retry(stop=stop_after_attempt(tries), wait=wait_fixed(delay), after=log_attempt)
    def get_oss_address():
        _url = url + '/bulkOps/query'
        result = None
        if StringUtils.is_empty(target_id):
            print(f"缺少参数:target_id")
            return
        try:
            response = requests.request(url=_url, headers=requestHeader, data=json.dumps(requestParam),
                                        method="post")
            response.raise_for_status()
            result = response.json()
            id_url_dict = {item["id"]: item["url"] for item in result["resultData"]["datas"]}
            if target_id in id_url_dict:
                if len(id_url_dict[target_id]) == 1:
                    target_url = urllib.parse.unquote(id_url_dict[target_id][0])
                    print(f"target_id [{target_id}] 的oss链接为： {target_url}")
                    return target_url
                else:
                    raise ValueError(f"存在多条 id 为 {target_id} 的记录，记录为：{id_url_dict[target_id]}")
            else:
                raise ValueError(f"未找到 id 为 {target_id} 的记录，未包含有效的 OSS 地址,")
        except (KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"响应数据格式错误,响应结果: {result},异常: {e}")
        except requests.RequestException as e:
            print(f"请求发生异常: {e}，正在重试...")
            raise

    def cancel_export_file(_target_id):
        """
        用于失败后取消导出
        :param _target_id:
        :return:
        """
        cancel_url = url + '/bulkOps/cancel'
        response = requests.request(url=cancel_url, headers=requestHeader, params={'id': _target_id}, method="get")
        response.raise_for_status()
        result = response.json()
        print(f"获取Oss Url失败，取消 {_target_id} 的导出记录，响应：{result}")
        return result

    try:
        return get_oss_address()
    except Exception as e:
        # print(f"最终失败，错误信息: {e}")
        if isinstance(e, RetryError):
            cancel_export_file(target_id)
        return None
