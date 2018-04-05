# -*- coding: utf-8 -*-

import requests
import pymysql
from scrapy.selector import Selector


def crawl_ips():
    # 爬取西刺免费的ip代理
    start_url = "http://www.xicidaili.com/nn/"

    html_text = get_html_text(start_url)
    selector = Selector(text=html_text)
    all_trs = selector.css("#ip_list tr")

    ip_list = []
    for tr in all_trs[1:]:
        speed_str = tr.css(".bar::attr(title)").extract()
        speed = float(speed_str[0].split("秒")[0])
        all_texts = tr.css("td::text").extract()
        ip = all_texts[0]
        port = all_texts[1]
        proxy_type = all_texts[5]
        ip_list.append((ip, port, proxy_type, speed))

    insert2mysql(ip_list)


def insert2mysql(ip_list):
    """
    连接数据库，并插入数据
    :param ip_list:
    :return:
    """
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='ts123456', db='blog_spider',
                           charset='utf8')
    cs = conn.cursor()

    cs.execute('drop table if exists proxy_ip')
    cs.execute(
        "create table proxy_ip(ip varchar(20) not null,port varchar(10) not null,speed float,proxy_type varchar(5),primary key(ip));")

    for i in ip_list:
        cs.execute(
            "insert proxy_ip(ip,port,speed,proxy_type) values('{ip}','{port}',{speed},'{proxy_type}')".format(ip=i[0],
                                                                                                              port=i[1],
                                                                                                              speed=i[
                                                                                                                  3],
                                                                                                              proxy_type=
                                                                                                              i[2]))
        conn.commit()

    cs.close()
    conn.close()


def get_html_text(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0"}
    result = requests.get(url, headers=headers)

    return result.text


class GetIP(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='ts123456', db='blog_spider',
                                    charset='utf8')
        self.cs = self.conn.cursor()

    def get_random_ip(self):
        """
        随机取出一组数据
        :return:
        """
        random_sql = """
        select ip,port from proxy_ip ORDER BY rand() limit 1      
        """
        result = self.cs.execute(random_sql)

        for ip_info in self.cs.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_result = self.judge_ip(ip, port)
            if judge_result:
                return ip, port
            else:
                return self.get_random_ip()

    def delete_ip(self, ip):
        """
        删除无用ip
        :param ip:
        :return:
        """
        delete_sql = """
            delete from proxy_ip where ip='{ip}'
        """.format(ip=ip)

        self.cs.execute(delete_sql)
        self.conn.commit()
        return True

    def judge_ip(self, ip, port):
        """
        判断ip是否可用
        :param ip:
        :param port:
        :return:
        """
        http_url = "http://www.baidu.com"
        proxy_url = "http://{ip}:{port}".format(ip=ip, port=port)

        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
            # return True

        except Exception as e:
            print("invalid ip and port !")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 3:
                print("effective ip !")
                return True
            else:
                print("invalid ip and port !")
                self.delete_ip(ip)
                return False


if __name__ == "__main__":
    getip = GetIP()
    getip.get_random_ip()
