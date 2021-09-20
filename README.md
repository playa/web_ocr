## Requirements

#### 1. python packages
```sh
pip install -r requirements.txt
```
#### 2. tesseract

Windows installer available [here](https://github.com/UB-Mannheim/tesseract/actions/runs/1119350562)
(required github login)

#### 3. chrome driver

download from [here](https://chromedriver.chromium.org/downloads)

### Options
```
usage: main.py [-h] [--url URL] [--input urls.txt] [--output out.json] [--print]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     pass single url
  --input urls.txt, -i urls.txt
                        get urls from file (one per line)
  --output out.json, -o out.json
                        save results in json format
  --print, -p           print to stdout each page result
```

### Example

#### single url in terminal
```sh
python main.py -u 'http://www.primorsk.vybory.izbirkom.ru/region/izbirkom?action=show&root=12000001&tvd=4014001103304&vrn=100100067795849&prver=0&pronetvd=null&region=1&sub_region=1&type=242&report_mode=null'
```

#### batch processing
```sh
python main.py -i in.txt -o results.json
```

#### JSON output example

```json
{
   "http://www.moscow-city.vybory.izbirkom.ru/region/izbirkom?action=show&root=1000272&tvd=27720002504394&vrn=100100225883172&prver=0&pronetvd=null&region=77&sub_region=77&type=233&report_mode=null":[
      [
         "Дата голосования:  19.09.2021"
      ],
      [
         "Наименование избирательной комиссии",
         "район Замоскворечье"
      ],
      [
         "",
         "Сумма",
         "УИК №38",
         "УИК №39",
         "УИК №40",
         "УИК №41",
         "УИК №42",
         "УИК №43",
         "УИК №44",
         "УИК №45",
         "УИК №46",
         "УИК №47",
         "УИК №48",
         "УИК №3611",
         "УИК №4002"
      ],
      [
         "Число избирателей, внесенных в список избирателей на момент окончания голосования",
         "23060",
         "1678",
         "1928",
         "1963",
         "2121",
         "1837",
         "2067",
         "2370",
         "1750",
         "2566",
         "1940",
         "2349",
         "214",
         "277"
      ],
      [
         "Число избирательных бюллетеней, полученных участковой избирательной комиссией",
         "22500",
         "1500",
         "2000",
         "2000",
         "2000",
         "2000",
         "2000",
         "2000",
         "1500",
         "2000",
         "2000",
         "2000",
         "500",
         "1000"
      ],
      [
         "Политическая партия \"КОММУНИСТИЧЕСКАЯ ПАРТИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ\"",
         "2166",
         "169",
         "172",
         "174",
         "186",
         "172",
         "185",
         "189",
         "177",
         "234",
         "195",
         "197",
         "36",
         "80"
      ],
      [
         "Политическая партия \"Российская экологическая партия \"ЗЕЛЁНЫЕ\"",
         "122",
         "7",
         "11",
         "11",
         "13",
         "8",
         "13",
         "16",
         "9",
         "14",
         "9",
         "6",
         "1",
         "4"
      ],
      [
         "Политическая партия ЛДПР – Либерально-демократическая партия России",
         "450",
         "33",
         "40",
         "29",
         "28",
         "37",
         "42",
         "45",
         "34",
         "49",
         "35",
         "47",
         "7",
         "24"
      ]
  ]
}
```