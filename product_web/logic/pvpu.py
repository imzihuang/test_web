#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from common.log_client import gen_log
from common.convert import is_date
from db.base import get_session, get_engine, json_dumps_alchemy
from db import api, models

def get_pu(ip="", html="", start="", end=""):
    try:
        session = get_session()
        # verify date
        if start and not is_date(start):
            gen_log.info("start format error:%s, %s"%(start, type(start)))
            return []
        if end and not is_date(end):
            gen_log.info("end format error:%s, %s" % (end, type(start)))
            return []
        query = api.get_pu_count(session, ip, html, start, end)
        results = query.all()
        _ = []
        for result in results:
            _.append({
                "ip": result.ip,
                "html": result.html,
                "count": int(result[2])
            })
        return _
    except Exception as ex:
        gen_log.error("pu query error:%r"%ex)
        return []
    finally:
        session.close()


def get_pv(ip="", html="", start="", end=""):
    try:
        session = get_session()
        # verify date
        if start and not is_date(start):
            gen_log.info("start format error:%s, %s"%(start, type(start)))
            return []
        if end and not is_date(end):
            gen_log.info("end format error:%s, %s" % (end, type(start)))
            return []
        query = api.get_pv_count(session, ip, html, start, end)
        results = query.all()
        _ = []
        for result in results:
            _.append({
                "ip": result.ip,
                "html": result.html,
                "count": int(result[2])
            })
        return _
    except Exception as ex:
        gen_log.error("pv query error:%r"%ex)
        return []
    finally:
        session.close()

def pu_add(ip, html, product_id="", product_name=""):
    try:
        session = get_session()
        current_month = datetime.datetime.now().strftime('%Y-%m-%d')+" 00:00:00"
        query = api.model_query(session, "Product_PU", {"ip": [ip], "html": [html], "visit_date": [current_month]})
        if query.count() == 0:
            data = {
                "ip": ip,
                "html": html,
                "product_id": product_id,
                "product_name": product_name,
                "pu_count": 1,
                "visit_date": current_month
            }
            data = api.convert_model("Product_PU", data)
            session.add(data)
        else:
            current_pu = query.first()
            current_pu.pu_count += 1
            #query.update({
            #    models.Product_PU.pu_count: current_pu.pu_count +1
            #})
        session.commit()
        return True
    except Exception as ex:
        gen_log.error("pu add error:%r" % ex)
        return False
    finally:
        session.close()

"""
def pv_add(ip, html, product_id="", product_name=""):
    try:
        session = get_session()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d') + " 00:00:00"
        query = api.model_query(session, "Product_PV", {"ip": [ip], "html": [html], "visit_date": [current_date]})
        if query.count() == 0:
            data = {
                "ip": ip,
                "html": html,
                "product_id": product_id,
                "product_name": product_name,
                "pv_count": 1,
                "visit_date": current_date
            }
            data = api.convert_model("Product_PV", data)
            session.add(data)
            session.commit()
        return True
    except Exception as ex:
        gen_log.error("pv error:%r"%ex)
        return False
    finally:
        session.close()
"""



