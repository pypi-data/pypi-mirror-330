from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.errors import *
import threading, time, random, statistics
from lxml import html

class DPTool:
    print('本脚本基于DrissionPage提供API运行\n喜欢本功能请给DrissionPage作者g1879买杯咖啡，支持原作者\nDrissionPage Github: https://github.com/g1879/DrissionPage')
    def __init__(self, data, method, proxy: str=None, num_threads: int=1, retry_times: int=1, waiting_time: float=2):
        '''
        method = 0: 收录查询
        method = 1: 标题收集
        method = 2: 相关搜索收集
        '''

        # thread lock
        self.lock = threading.Lock()

        # retry_times
        self.retry_times = retry_times

        # waiting_time
        self.waiting_time = waiting_time

        # proxy
        self.co = ChromiumOptions()
        if proxy:
            self.co.set_proxy(f'http://{proxy}')
        else:
            pass
        
        # browser settings
        self.browser = Chromium(addr_or_opts=self.co)
        
        # create tabs as many as threads
        count = 1
        while count < num_threads:
            self.browser.new_tab()
            count += 1

        # split data into chunks
        self.chunks = []
        cuts = [(i+1)*num_threads for i in range(len(data)//num_threads)]
        cuts.insert(0,0)
        cuts.append(len(data))
        for index, cut in enumerate(cuts[:-1]):
            self.chunks.append(data[cut:cuts[index+1]])

        # create self method 
        self.method = method

        self.results=[]
        self.failed=[]

    def baidu_index_checker(self, tab, url: str):
        fail_count = 0
        while fail_count <= self.retry_times:
            try:
                ele = tab.ele('@@id=kw')
                ele.input(url+'\n', clear = True)
                tab.wait.title_change(url, raise_err = True)
                tab.wait.eles_loaded('tag:div@id=wrapper_wrapper', raise_err = True)
                tree = html.fromstring(tab.html)
                break
            except:
                fail_count += 1
                self.browser.clear_cache()
                tab.get('https://www.baidu.com')

        if fail_count <=self.retry_times:
            # all_ranked_urls = tree.xpath("//div[@id='content_left' and @tabindex='0']/div/@mu")
            all_ranked_urls = tree.xpath("//div[@id='content_left' and @tabindex='0']/div")
            for i in all_ranked_urls:
                try:
                    i_url = i.attrib['mu']
                    image = i.xpath(".//img/@src")
                    if url == i_url:
                        if image:
                            return (url, '已收录', '已出图')
                        else:
                            return (url, '已收录', '未出图')
                except:
                    pass
            return (url, '未收录', '未出图')
        else:
            return None
    
    def baidu_title_collector(self, tab, search_word:str):
        fail_count = 0
        while fail_count <= self.retry_times:
            try:
                ele = tab.ele('@@id=kw')
                ele.input(search_word+'\n', clear = True)
                tab.wait.title_change(search_word, raise_err = True)
                tab.wait.eles_loaded('tag:div@id=wrapper_wrapper', raise_err = True)
                tree = html.fromstring(tab.html)
                break
            except:
                fail_count += 1
                self.browser.clear_cache()
                tab.get('https://www.baidu.com')
        
        if fail_count <=self.retry_times:
            results = {
                'titles':[],
                'sources':[]
            }
            branch = tree.xpath("//div[@id='content_left' and @tabindex='0']/div")    
            for leaf in branch:
                # Baidu Health Box
                raw_title = leaf.xpath(".//div[@class='title-box_3IwNQ']//text()")
                source = leaf.xpath(".//div[@class='wenda-abstract-source_3NRe0']//span/text()")
                if raw_title and source:
                    title = ''.join([x for x in raw_title if x.isprintable()])
                    results['titles'].append(title)
                    results['sources'].append(source)
                    continue
                # Regular Box
                raw_title = leaf.xpath(".//h3[@class='c-title t t tts-title']//text()")
                source = leaf.xpath(".//div//div[@sub-show='true']//span[@class='c-color-gray']/text()")
                if raw_title and source:
                    title = ''.join([x for x in raw_title if x.isprintable()])
                    results['titles'].append(title)
                    results['sources'].append(source)
                    continue
            return results
        else:
            return None
    
    def baidu_rs_collector(self, tab, search_word:str):
        fail_count = 0
        while fail_count <= self.retry_times:
            try:
                ele = tab.ele('@@id=kw')
                ele.input(search_word+'\n', clear = True)
                tab.wait.title_change(search_word, raise_err = True)
                tab.wait.eles_loaded('tag:div@id=wrapper_wrapper', raise_err = True)
                tree = html.fromstring(tab.html)
                break
            except:
                fail_count += 1
                self.browser.clear_cache()
                tab.get('https://www.baidu.com')
        
        if fail_count <=self.retry_times:
            result = tree.xpath("//table[@cellpadding='0' and @class='rs-table_3RiQc']/@data-ushow")
            return (result['query'], result['iteminfo'])
        else:
            return None
        
    def distributor(self, tab_id: str, chunk):
        tab = self.browser.get_tab(tab_id)
        waiting_times = statistics.NormalDist(self.waiting_time, 0.125).samples(len(chunk))
        waiting_times = [x+random.uniform(0,0.5) for x in waiting_times]
        successed = list()
        failed = list()
        if self.method == 0:
            for index, item in enumerate(chunk):
                temp = self.baidu_index_checker(tab, url=item)
                if temp == None:
                    failed.append(item)
                else:
                    successed.append(temp)
                time.sleep(waiting_times[index])
        elif self.method == 1:
            for index, item in enumerate(chunk):
                temp = self.baidu_title_collector(tab, search_word=item)
                if temp == None:
                    failed.append(item)
                else:
                    successed.append(temp)
                time.sleep(waiting_times[index])
        elif self.method == 2:
            for index, item in enumerate(chunk):
                temp = self.baidu_rs_collector(tab, search_word=item)
                if temp == None:
                    failed.append(item)
                else:
                    successed.append(temp)
                time.sleep(waiting_times[index])
        with self.lock:
            self.results.append(successed)
            self.failed.append(failed)
            print(f"网页{tab_id}: 已完成")

    def threads_processor(self):
        threads = []

        for index, tab in enumerate(self.browser.get_tabs()):
            if self.chunks[index].size != 0:
                tab.get('https://www.baidu.com')
                threads.append(threading.Thread(target=self.distributor, args=(tab.tab_id, self.chunks[index])))
                threads[-1].start()

        for thread in threads:
            thread.join()
        