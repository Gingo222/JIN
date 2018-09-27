
import re
import requests
from bs4 import BeautifulSoup


url = "http://103.211.47.130:74/case?caseId=P3385535T20180828R105642&orderBy=study_datetime%3Ades" \
      "c&page=image&search=&straitness="

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
         "Chrome/50.0.2661.102 Safari/537.36'}
print(re.findall(r"caseId=(.+?)&", url))
html = requests.get(url, headers=header)
html.encoding = 'utf8'
print(html.text)
soup = BeautifulSoup(html.text, 'html.parser')
label = soup.find_all('div', class_='dicom-info--left-top')
print(label)

print(soup.body.contents)
for child in soup.body.children:
    print(child)

da = ['<div class="dicom-info--left-top">SS-Freeze 75% - Original Series 301<br/>401<br/><br/>Axial 58/224<br/>BPM 63<br/><span>Value 0</span></div>',
      '<div class="dicom-info--left-top">3D<br/>401<br/><br/>Volume Rendering<br/>BPM 63</div>',
      '<div class="dicom-info--left-top">3D<br/>401<br/><br/>Volume Rendering<br/>BPM 63</div>',
      '<div class="dicom-info--left-top">CPR<br/>401<br/><br/>LAD Angle: 0<br/>BPM 63<br/><span>Value 0</span></div>',
      '<div class="dicom-info--left-top">Xsection<br/>401<br/><br/>LAD<br/>BPM 63<br/><span>Value 0</span></div>',
      '<div class="dicom-info--left-top">Lumen<br/>401<br/><br/>LAD Angle: 0<br/>BPM 63<br/><span>Value 0</span>]</div>']
for x in range(len(da)):
    if re.findall(r"Angle:(.+?)/", da[x]):
        print 'hahhahaha', da[x]


a = {'a': (1, 2), 'b': (2, 2)}
print(a.keys())