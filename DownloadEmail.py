import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from watchdog.observers import Observer

import AI
import Constant
import ParseInvoice
import config
import util
from DriverSingleton import DriverSingleton
from monitor import MyHandler

driver, wait = DriverSingleton.init()
current_page = 1
monitor = MyHandler()
end_flag = False
origin_window_handle = None
fail_invoice_list = {}


def start_monitor():
    observer = Observer()
    observer.schedule(monitor, config.get_location(), recursive=False)
    observer.start()


def download_email():
    begin()
    start_monitor()
    switch_to_frame()
    while not end_flag:
        handle_mail()
        next_page()
    ParseInvoice.parse_invoice()
    print(fail_invoice_list)


def begin():
    global origin_window_handle
    driver.get(Constant.BASE_URL)
    origin_window_handle = driver.current_window_handle
    # driver.get('https://www.hxpdd.com/s/Q3QQGcH49TCm')
    # print(driver.find_element_by_tag_name('body').get_attribute('innerHTML'))


def switch_to_frame():
    if len(driver.window_handles) > 1:
        driver.close()
    driver.switch_to.window(origin_window_handle)
    driver.refresh()
    recv_option = util.getDelayElement(By.PARTIAL_LINK_TEXT, "收件箱")
    recv_option.click()

    main_frame = util.getDelayElement(By.CSS_SELECTOR, "#mainFrame")
    driver.switch_to.frame(main_frame)
    jump_page()


def get_mail_list():
    time.sleep(2)
    return driver.find_elements_by_class_name("M") + driver.find_elements_by_class_name("F")


def record_fail(item):
    if item['mailId'] not in fail_invoice_list:
        fail_invoice_list[item['mailId']] = item['title']


def check_file(item):
    if monitor.get_created() == 0:
        record_fail(item)


def handle_mail():
    global end_flag
    invoice_list = []
    mail_list = get_mail_list()
    mail_num = len(mail_list)
    print(f'mail_num:{mail_num}, page: {current_page}')
    for mail in mail_list:
        mailid = mail.find_element(By.CSS_SELECTOR, 'td.tl.tf ').find_element(By.TAG_NAME, 'nobr').get_attribute(
            'mailid')
        title = mail.find_element_by_class_name("tt").text
        if '发票' in title:
            try:
                mail.find_element(By.CSS_SELECTOR, 'div.cij.Ju')
                invoice_list.append({'title': title, 'mailId': mailid})
            except NoSuchElementException as e:
                invoice_list.append({'title': title, 'mailId': mailid})
    print(f'-------发票: {len(invoice_list)}-------')
    for item in invoice_list:
        monitor.reset_create()
        mailId = item["mailId"]
        tag = driver.find_element_by_xpath(f"//nobr[@mailid='{mailId}']")
        tag.click()
        time.sleep(1)
        if is_out_date():
            end_flag = True
            break
        try:
            if exist_element(By.ID, 'attachment'):
                download_attach()
                check_file(item)
            else:
                handle_no_attach()
                check_file(item)
        except Exception as e:
            record_fail(item)
        switch_to_frame()
        time.sleep(3)


def exist_element(by, key) -> bool:
    try:
        driver.find_element(by, key)
        return True
    except NoSuchElementException as e:
        return False


def is_out_date():
    date = util.getDelayElement(By.ID, 'local-time-caption').text.split('（')[0]
    month_date = util.parse_date(date, '%Y年%m月%d日', '%Y%m')
    return month_date < config.get_out_date()


def download_attach():
    attachment = util.getDelayElement(By.ID, 'attachment')
    attach_items = attachment.find_elements(By.CSS_SELECTOR, 'div.att_bt.attachitem')
    for attach in attach_items:
        util.getDelayElement(By.CSS_SELECTOR, 'div.name_big')
        if '.pdf' in attach.find_element(By.CSS_SELECTOR, 'div.name_big').find_element(By.TAG_NAME, 'span').text:
            attach.find_element_by_partial_link_text('下载').click()
            break
    time.sleep(3)
    switch_to_frame()
    time.sleep(4)


def handle_no_attach():
    global fail_invoice_list
    container = util.getDelayElement(By.ID, 'mailContentContainer')
    html = container.find_element(By.TAG_NAME, 'div').get_attribute('innerHTML')
    text = AI.find_text(html)
    element = util.getDelayElement(By.XPATH, f"//a[contains(text(), '{text}')]")
    element.click()
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    if exist_element(By.TAG_NAME, 'body') and len(
            str(driver.find_element_by_tag_name('body').get_attribute('innerHTML'))) > 0:
        download = util.getDelayElement(By.XPATH, f"//*[contains(text(), '下载')]")
        time.sleep(1)
        download.click()
    time.sleep(2)


def next_page():
    if end_flag:
        return
    global current_page
    current_page += 1
    util.getDelayElement(By.ID, 'nextpage', True)
    element = driver.find_element(By.ID, 'nextpage')
    element.click()
    time.sleep(2)


def jump_page():
    if end_flag:
        return
    for i in range(current_page - 1):
        util.getDelayElement(By.ID, 'nextpage', True)
        nextpage = driver.find_element(By.ID, 'nextpage')
        nextpage.click()
    if current_page > 1:
        time.sleep(2)
