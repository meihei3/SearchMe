# SearchMe

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/yameholo/SearchMe/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/yameholo/SearchMe/?branch=master)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

***
safariの履歴のデータベーズを持ってきて、出現する単語（名詞）でwordcloudを使って可視化する。  

## Requests
OS: macOS  
python: python 3.x  
pyhton package: wordcloud-1.3.1  
pyhton package: tqdm-4.19.5  

## Usage
First, create your history wordcloud  
`python SearchMe.py [size]`  
You can get 'wordcloud.png'. And open it.  

The argv[1] (=size) provide you the histories from the latest to (the latest - size)  
If you don't set size, The initial value is `50`.