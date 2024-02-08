import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import Constant
import ParseInvoice
import config
import util
from DriverSingleton import DriverSingleton

driver, wait = DriverSingleton.init()
current_page = 1
end_flag = False


def download_email():
    begin()
    # switch_to_frame()
    # while not end_flag:
    #     handle_mail()
    #     next_page()
    # ParseInvoice.parse_invoice()


def begin():
    # driver.get(Constant.BASE_URL)
    driver.get('https://www.hxpdd.com/s/Q3QQGcH49TCm')
    print(driver.find_element_by_tag_name('body').get_attribute('innerHTML'))


def switch_to_frame():
    recv_option = util.getDelayElement(By.PARTIAL_LINK_TEXT, "收件箱")
    recv_option.click()

    main_frame = util.getDelayElement(By.CSS_SELECTOR, "#mainFrame")
    driver.switch_to.frame(main_frame)
    jump_page()


def get_mail_list():
    driver.implicitly_wait(7)
    return driver.find_elements_by_class_name("M") + driver.find_elements_by_class_name("F")


def handle_mail():
    global end_flag
    no_attach_invoice_list = []
    attach_invoice_list = []
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
                attach_invoice_list.append(mailid)
            except NoSuchElementException as e:
                no_attach_invoice_list.append(mail)
    print(len(attach_invoice_list))
    print('-------有附件的发票-------')
    for item in attach_invoice_list:
        print(f'{item}')
        tag = driver.find_element_by_xpath(f"//nobr[@mailid='{item}']")
        tag.click()
        time.sleep(1)
        if is_out_date():
            end_flag = True
            break
        download_attach()


def exist_attach(by, key) -> bool:
    try:
        driver.find_element(by, key)
        return True
    except NoSuchElementException as e:
        return False


def is_out_date():
    date = util.getDelayElement(By.ID, 'local-time-caption').text.split('（')[0]
    month_date = util.parse_date(date, '%Y年%m月%d日', '%Y%m')
    print(f'{date}, month_date: {month_date}')
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
    # driver.back()
    driver.refresh()
    switch_to_frame()
    time.sleep(4)


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
