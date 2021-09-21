import json
from base64 import b64decode
from io import BytesIO
from time import sleep
from typing import List
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

import pytesseract
from PIL import Image
from selenium.webdriver import Chrome, ChromeOptions


def init_driver() -> Chrome:
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(options=options)
    driver.set_window_size(6000, 10000)
    return driver


def get_page_data(driver: Chrome, url: str) -> List[List[str]]:
    driver.delete_all_cookies()
    driver.get(url)
    sleep(1)

    # increase text size, hide some data
    css = """
        body {font-size: 2 em !important;}
        table#fix-columns-table td, table#fix-columns-table th {background: white !important; } 
        table#fix-columns-table td:nth-child(2) ~ * {color: white !important; text-align: center !important } 
        table#fix-columns-table td > nobr { color: black !important; padding: 2px;}
        table#fix-columns-table {height: auto;}
    """
    for style in css.split("\n")[1:-1]:
        driver.execute_script(f'document.styleSheets[0].insertRule("{style}", 0 )')
    #driver.execute_script("document.body.style.zoom = '2'")
    sleep(1)
    results = []
    head_rows = driver.find_elements_by_css_selector('.table-borderless tr')
    for row in head_rows:
        cols = row.find_elements_by_tag_name('td')
        line = []
        for col in cols:
            text = col.text.strip()
            if text:
                line.append(text)
        if line:
            results.append(line)

    
    #driver.execute_script("arguments[0].style.width=arguments[0].style.scrollWidth + 'px'", tb)
    #driver.execute_script("arguments[0].style.height=arguments[0].style.scrollHeight + 'px'", tb)

    #remove scroll container and set height to remove screenshot artifacts
    driver.execute_script("document.getElementsByClassName('table-scroller')[0].removeAttribute('class')")
    driver.execute_script("document.getElementById('fix-columns-table').style.height= 'auto'")
    sleep(1)
    #driver.save_screenshot("screen.png")
    
    rows = driver.find_elements_by_css_selector('table#fix-columns-table tr')
    for i, row in enumerate(rows):

        cols = row.find_elements_by_tag_name('td')
        if len(cols) == 0:
            results.append([cell.text.strip() for cell in row.find_elements_by_tag_name('th')[1:]])
        else:
            name = cols[1].text.strip()
            if '. ' in name[:10]:
                # cut numeration
                name = name.split('. ', 1)[1]
            fullrow = [name]
            for j in range(2, len(cols)):
                #image = Image.open(BytesIO(b64decode(cols[j].screenshot_as_base64)))
                #image.save(f"{i}_{j}_col.png")
                nobr = cols[j].find_elements_by_tag_name('nobr')[0]
                image = Image.open(BytesIO(b64decode(nobr.screenshot_as_base64)))
                #image.save(f"{i}_{j}.png")
                # 7 - single line option, 8 is single word 
                text = pytesseract.image_to_string(image, config='--psm 8 -c "tessedit_char_whitelist=0123456789"')
                fullrow.append(text.strip())
            results.append(fullrow) 
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', metavar='URL', help='pass single url')
    parser.add_argument('--input', '-i', metavar='urls.txt', help='get urls from file (one per line)')
    parser.add_argument('--output', '-o', metavar='out.json', help='save results in json format')
    parser.add_argument('--print', '-p', action='store_true', help='print to stdout each page result')
    args = parser.parse_args()

    if not args.output:
        args.print = True

    if args.input:
        with open(args.input, 'rt') as f:
            urls = f.readlines()
    elif args.url:
        urls = [args.url]
    else:
        print('ERR: specify --url or --input file')
        return

    driver = init_driver()
    results = {}
    for i, url in enumerate(urls):
        if not url:
            continue
        print(f'processing {i + 1} / {len(urls)} url')
        try:
            results[url] = get_page_data(driver, url)
        except Exception as e:
            print(f'ERR: {e!r}')
            continue
        if args.print:
            print(f'URL: {url}')
            for line in results[url]:
                print(line)

    if args.output:
        with open(args.output, 'wt', encoding='utf8') as f:
            json.dump(results, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
