#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.log_client import gen_log
from db.base import get_session
from db import api

def get_product(**kwargs):
    id = kwargs.get("id", "")
    name = kwargs.get("name", "")
    offset = kwargs.get("offset", 0)
    limit = kwargs.get("limit", 0)
    try:
        session = get_session()
        if id:
            query = api.model_query(session, "Product", {"id": [id]})
            result = query.first()
            return result.to_dict()
        if name:
            query = api.model_query(session, "Product", {"name": [name]})
            result = query.first()
            return result.to_dict()
        query = api.model_query(session, "Product", {})
        results = query.order_by("sort_num").all()
        return [result.to_dict() for result in results]
    except Exception as ex:
        gen_log.error("get product error:%r"%ex)
    finally:
        session.close()

def get_product_like_name(product_keyword, offset=0, limit=0):
    """
    获取产品列表，根据关键字模糊查询
    :param product_keyword:
    :return:
    """
    try:
        if not product_keyword:
            return
        session = get_session()
        query = api.get_product_like_name(session, product_keyword)
        results = query.order_by("sort_num").all()
        return [result.to_dict() for result in results]
    except Exception as ex:
        gen_log.error("like query product error: %r"% ex)
    finally:
        session.close()

def verify_product(session, name):
    """
    验证产品名是否已经存在
    :param session:
    :param name:
    :return:
    """
    if name:
        query = api.model_query(session, "Product", {"name": [name]})
        if query.count()>0:
            return 1
    return 0

def add_product(productinfo):
    try:
        name = productinfo.get("name", "")
        session = get_session()
        _ = verify_product(session, name)
        if _ != 0:
            return False

        sort_num = productinfo.get("sort_num", 10000)
        if sort_num==0:
            productinfo.update({"sort_num": 10000})
        if sort_num > 0 and sort_num<10000:
            api.set_product_sort_num(session, sort_num)

        model_user = api.convert_model("Product", productinfo)
        session.add(model_user)
        session.commit()
        return True
    except Exception as ex:
        gen_log.error("add user error:%r"%ex)
        raise ex
    finally:
        session.close()

def update_product(productinfo, con_dic):
    """
    更新产品
    :param productinfo:{"name": "sdfds"}
    :param con_dic: {"name": ["sdfdsd"]}
    :return:
    """
    try:
        session = get_session()
        sort_num = productinfo.get("sort_num", 10000)
        if sort_num==0:
            productinfo.update({"sort_num": 10000})
        if sort_num > 0 and sort_num<10000:
            api.set_product_sort_num(session, sort_num)

        query = api.model_query(session, "Product", con_dic)
        query.update(productinfo, synchronize_session=False)
        session.commit()
        return True
    except Exception as ex:
        gen_log.error("update user error:%r"%ex)
        return False
    finally:
        session.close()

def del_product(product_name):
    try:
        session = get_session()
        query = api.model_query(session, "Product", {"name": [product_name]})
        query.delete(synchronize_session=False)
        session.commit()
        return True
    except Exception as ex:
        gen_log.error("del product error:%r"%ex)
        return False
    finally:
        session.close()

