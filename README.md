![autoEmail_logo.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4454ca3f731d47c1abc17b86720429ca~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1676&h=924&s=45733&e=png&b=fcfcfc)
> 背景:因为每个月有报销发票的需求，但每次到报销发票的时候，都需要去邮箱上一个个把发票下载下来，然后分类整理。这些都是耗时且重复的动作，就想着能不能把它自动化，同时看看能不能结合上最近大火的AI

> 目标：能够按要求自动下载发票文件，同时解析重命名发票文件
## 自动下载邮件中附件
这一步是很简单的啦，用Selenium就可以实现，我的是QQ邮箱。我们只需要打开浏览器按下F12一步步的查找从登录到进入邮件下载附件都需要点击哪些元素，然后用Selenium代替我们操作就行
### 登录
```python
BASE_URL = 'https://mail.qq.com/'
def begin():
    global origin_window_handle
    driver.get(Constant.BASE_URL)
    origin_window_handle = driver.current_window_handle
```
这里登录就没有做的那么麻烦，自己扫码或者输入账号密码即可。
### 获取邮件
登录到QQ邮箱后，通过F12可以看到主要功能区是在iframe里面，因此我们要先点击收件箱然后切换到iframe中，否则没法找到元素


![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/eb2db1c1b10d4cf0b42921d0493f6540~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2766&h=1186&s=621910&e=png&b=adcaea)

```python
def switch_to_frame():
    recv_option = util.getDelayElement(By.PARTIAL_LINK_TEXT, "收件箱")
    recv_option.click()
    main_frame = util.getDelayElement(By.CSS_SELECTOR, "#mainFrame")
    driver.switch_to.frame(main_frame)
```
接着就获取邮件，每次只能获取当前页数的邮件，我这里是把未读和已读都获取到了
```python
def get_mail_list():
    return driver.find_elements_by_class_name("M") + driver.find_elements_by_class_name("F")
```
### 处理邮件
因为我只要处理发票的邮件，用了最简单的方式，只处理当前邮件标题是否包含发票两字，同时发票邮件包括两种，带有附件和不带有附件的，带有附件的是邮件里直接附上了发票文件。不带有附件的是邮件里给了一个链接，需要点击后才能下载或者跳转到其他网站下载。因为两种方式的处理方式不同，所以需要分开存储哪些是带有附件的哪些没带有附件。同时为了避免同名标题不同发票的情况，我们使用mailId来进行存储，后续通过mailId来定位每一个邮件

![image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/697c77f3bff345359803e27cd6fbc6fb~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1794&h=128&s=75361&e=png&b=fbfafa)
```python
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
        title = item["title"]
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
```
#### 处理带有附件的邮件
附件可能会有多个附件，我们只需要下载PDF文件即可


![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/43c2ff0e8bc54b1ba8f2fe43edda5240~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1060&h=378&s=130324&e=png&b=fefefe)
```python
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
```
#### 处理没有附件的邮件
这个才是本次的重点，对于没有附件只有下载链接的邮件，如何让selenium知道该点哪里。不同的邮件他们的展示也不同

![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2ceca4249b644bbd986c8e1031aacfd4~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1662&h=1196&s=338087&e=png&b=fdfdfd)

![image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1ff8c06bec4a4056bd28607a7489fb9e~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1478&h=1204&s=521278&e=png&b=effafd)
解决方法就是让AI来告诉selenium该点哪里，通过F12可以发现，邮件的内容都是在一个固定的Div里面

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/708aca92c9f245a18a93d73aa5084945~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2774&h=1042&s=1073964&e=png&b=fefefe)
那我们就可以获取这个Div里面的HTML片段，然后告诉AI，让它根据HTML片段解析出带有发票下载链接的标签文本，然后返回，selenium根据这个文本点击，以下是对于prompt
``` python
prompt = '''
你是一名HTML解析助手，你需要解析用户上传的HTML片段。
1.解析出片段中带有发票下载链接的超链接标签文本。
2.如果有多个下载链接，则找出下载为PDF格式的超链接标签文本即可。
例如: 
输入: 
<p style="display: flex;justify-content: flex-start;align-items: flex-start;font-size:14px;line-height:20px;">
          <span style="white-space: nowrap;color: #333">下载PDF文件：</span>
          <img width="20" src="https://img.pdd-fapiao.com/biz/bG9uZ2p1bmd3YW5n.png">
          <a href="https://www.hxpdd.com/s/Q3QQGcH49TCm" style="word-break:break-all;margin-left: 10px;color: #3786c7" rel="noopener" target="_blank">HelloWorld</a>
</p>
输出:
{"text":"HelloWorld"}
注意只需要返回对应的标签文本即可，不需要其他内容。结果输出为JSON:{'text':'xxx'}"}
'''
```
点击过后，一般会有两种结果，一种是点击后能够直接下载发票,另一种是跳转到其他网站后，再点击下载才能下载

![image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d66bdeff62ec48f1be6b3d6bd848bed5~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2198&h=1242&s=869543&e=png&b=faf7f7)
针对这种我们就可以全文搜索带有下载字样的标签进行点击下载。经过上面这一套下来，基本90%的都能成功下载下来
#### 解析整理发票
下载下来的发票命名各异

![image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2604399dd07a44749a8108b84f57bd24~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1376&h=776&s=195129&e=png&b=020202)
我希望能够通过文件名就能知道该发票的类型，金额和开票日期，这里用上了OCR+AI，用OCR来解析发票文件，然后将解析结果送给AI让其根据结果分析该发票属于哪种类别。最后再重命名发票
```python
def parse_invoice():
    invoice_list = get_invoice_list()
    location = config.get_location()
    for invoice in invoice_list:
        file_path = os.path.join(location, invoice)
        invoice_info = OcrUtil.ocr_invoice(file_path)
        new_file_name = get_new_file_name(invoice_info)
        util.rename(invoice, new_file_name)
        print(f'{invoice} : {new_file_name}')


def get_new_file_name(invoice_info):
    date = util.parse_date(invoice_info['Date'], '%Y年%m月%d日', '%Y%m%d')
    summary = get_summary(invoice_info)
    return summary + '_' + invoice_info['Number'] + '_' + invoice_info['Total'].split('.')[0] + '_' + date


def get_summary(item):
    if 'VatElectronicItems' in item:
        info = json.loads(json.dumps(item['VatElectronicItems']))
    else:
        info = json.loads(json.dumps(item['VatInvoiceItemInfos']))
    return AI.ai_summary(info[0]['Name'])
```
最后就是这个样子

![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1fecd159a7484d41971e1c6e4b4c0981~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1000&h=768&s=188681&e=png&b=010101)

#### 使用方法
> 在config.json文件设置文件下载地址和日期，日期的作用是在下载附件时只下载日期之后的附件，在OcrUtil.py文件里设置腾讯云的secret_id和secret_key，在AI.py文件里设置GPT的api_key后，然后运行main.py，等待浏览器拉起后，手动登录后即可

![image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9a96d7b239e145ae848e9dbc0e62b104~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=572&h=868&s=103498&e=png&b=2b2d30)


目前只实现了下载和解析重命名，邮箱目前只支持QQ邮箱，AI目前只支持GPT，后续会支持多个邮箱和AI
同时还在考虑可以加入哪些功能，有建议和优化欢迎大家在GitHub给我提，如果有帮助的话帮忙**Star**一下
> **地址：[GitHub-autoEmail](https://github.com/WRCoding/autoEmail)**
 
