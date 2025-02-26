# -*- codeing = utf-8 -*-
# @Time :2025/2/20 00:27
# @Author :luzebin
import pandas as pd

from smartpush.export.basic.ExcelExportChecker import check_excel_all, read_excel_and_write_to_list, \
    read_excel_from_oss, read_excel_csv_data, check_excel
from smartpush.export.basic.ReadExcel import read_excel_from_oss
from smartpush.export.basic.ReadExcel import read_excel_and_write_to_dict
from smartpush.export.basic.GetOssUrl import get_oss_address_with_retry

if __name__ == '__main__':
    oss1 = "https://cdn.smartpushedm.com/material_ec2/2025-02-20/ad9e1534b8134dd098e96813f17d4b4d/%E6%B5%8B%E8%AF%95flow%E6%95%B0%E6%8D%AE%E6%8A%A5%E5%91%8A%E5%AF%BC%E5%87%BA%E5%8B%BF%E5%8A%A8%E6%95%B0%E6%8D%AE%E6%A6%82%E8%A7%88.xlsx"
    oss2 = "https://cdn.smartpushedm.com/material_ec2/2025-02-21/bbe660950493411d88b4a75ed0893ec8/%E6%B5%8B%E8%AF%95flow%E6%95%B0%E6%8D%AE%E6%8A%A5%E5%91%8A%E5%AF%BC%E5%87%BA%E5%8B%BF%E5%8A%A8%E6%95%B0%E6%8D%AE%E6%A6%82%E8%A7%88.xlsx"
    # # print(check_excel_all(oss1, oss1))
    # oss3 = "https://cdn.smartpushedm.com/material_ec2/2025-02-25/58c4a3a885884741b22380c360ac2894/【自动化导出】营销活动URL点击与热图.xlsx"
    # oss4 = "https://cdn.smartpushedm.com/material_ec2/2025-02-26/58cee630b4c84eec9572b867af4ce692/%E3%80%90%E8%87%AA%E5%8A%A8%E5%8C%96%E5%AF%BC%E5%87%BA%E3%80%91%E8%90%A5%E9%94%80%E6%B4%BB%E5%8A%A8URL%E7%82%B9%E5%87%BB%E4%B8%8E%E7%83%AD%E5%9B%BE.xlsx"
    expected_oss ="https://cdn.smartpushedm.com/material_ec2/2025-02-26/757df7e77ce544e193257c0da35a4983/%E3%80%90%E8%87%AA%E5%8A%A8%E5%8C%96%E5%AF%BC%E5%87%BA%E3%80%91%E8%90%A5%E9%94%80%E6%B4%BB%E5%8A%A8%E6%95%B0%E6%8D%AE%E6%A6%82%E8%A7%88.xlsx"
    actual_oss = "https://cdn.smartpushedm.com/material_ec2/2025-02-26/757df7e77ce544e193257c0da35a4983/%E3%80%90%E8%87%AA%E5%8A%A8%E5%8C%96%E5%AF%BC%E5%87%BA%E3%80%91%E8%90%A5%E9%94%80%E6%B4%BB%E5%8A%A8%E6%95%B0%E6%8D%AE%E6%A6%82%E8%A7%88.xlsx"
    # # #actual_oss= get_oss_address_with_retry("23161","https://cdn.smartpushedm.com/material_ec2_prod/2025-02-20/dae941ec20964ca5b106407858676f89/%E7%BE%A4%E7%BB%84%E6%95%B0%E6%8D%AE%E6%A6%82%E8%A7%88.xlsx","",'{"page":1,"pageSize":10,"type":null,"status":null,"startTime":null,"endTime":null}')
    # # res=read_excel_and_write_to_dict(read_excel_from_oss(actual_oss))
    # # print(res)
    # # print(read_excel_and_write_to_dict(read_excel_from_oss(oss1), type=".xlsx"))
    print(check_excel(check_type="all", actual_oss=actual_oss, expected_oss=expected_oss))
    # print(check_excel_all(actual_oss=oss1, expected_oss=oss2,skiprows=1))
    # print(check_excel_all(actual_oss=oss1, expected_oss=oss2,ignore_sort =True))
    # read_excel_csv_data(type=)
