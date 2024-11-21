# main.py

from flask import Flask, request, jsonify

from playwright.sync_api import Frame, sync_playwright
from edu_agent import request_chsi_by_playwriht, request_by_ip_agent, test_get_ip
app = Flask(__name__)


# app.route('/', methods=['GET', 'POST'])
# def demo():
#   if request.method == 'GET':
#     return render_template('index.html', input_text = '', res_text = '')
#   else:
#     inputText = request.form.get("input_text")
#     resText = Markup(formatRes(reverseText(inputText)))
#     return render_template('index.html', input_text = inputText, res_text = resText)

def formatRes(textList):
  return '<p>' + '</p><p>'.join(textList) + '</p>'

# A sample
def reverseText(text):
  res = []
  res.append('Original text: %s' %(text))
  res.append('Converted text: %s' %(''.join(reversed(list(text)))))
  return res




@app.route('/api/edu/catch', methods=['POST'])
def catch_edu_page():
    """使用IP代理池及playwright爬取edu_page"""
    # pip install playwright
    # from playwright.sync_api import Frame, sync_playwright
    # from server.edu_agent import request_chsi_by_playwriht, request_by_ip_agent, test_get_ip
    try:
        reqeust_url = request.values.get('reqeust_edu_url')
        print(f"reqeust_edu_url={reqeust_url}")
        # reqeust_url = f'https://www.chsi.com.cn/xlcx/bg.do?vcode={vcode}&srcid=bgcx'

        proxies = request_by_ip_agent()
        print(proxies)
        test_get_ip(proxies)
        print('VVVVVVVVVVVVVVVVVVV')
        # request_chsi_by_request(reqeust_url)

        with sync_playwright() as p:
            page_html = request_chsi_by_playwriht(p, reqeust_url, proxies)
            # print(f"\n\n\n\npage:\n{page}")
            return jsonify(
               message='success',
               data = {
                  'proxie': proxies,
                  'page_html': page_html
               }
            )
    except Exception as e:
        print(e)
        raise e
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)
