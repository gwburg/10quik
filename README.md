# 10quik
This is a practice project from 2020/2021 that I used to learn web development during grad school

## Purpose
The aim of 10quik is to combine two of my main hobbies: investing and programming

A core practice of fundamental investing is to read the financial statements of companies you are interested in, which are available for free from the SEC. However, the SEC website is inconvenient and time consuming to navigate, and services that compile these financial statements aren't free. So the goal of 10quik is to allow users to quickly and easily read and analyze financial statements from any public company at no cost.

10quik compiles 10-Q and 10-K filings (hence the name) for every publicly traded company. Each financial table within a filing can be quickly converted to an excel sheet for convenient offline analysis. 10quik also utilizes a machine learning algorithm to identify the most commonly viewed tables -- namely the income statement, balance sheet, and cash flow statement -- and links the user directly to them in the document so no manual searching or scrolling is required :).

## Outline
This is a work in progress and not currently scalable, so it isn't deployed for outside users. Below are some demo images showing the current state of the project.

#### Home page
![home page](https://github.com/gwburg/10quik/blob/main/demo/1.png?raw=true)
#### Search autocomplete from the SEC database
![autocompletes searchbar](https://github.com/gwburg/10quik/blob/main/demo/2.png?raw=true)
#### Pulls in all quarterly and annual filings for selected company
![import all filings](https://github.com/gwburg/10quik/blob/main/demo/3.png?raw=true)
#### Loads selected filing and begins scanning the document
![selected filing loaded](https://github.com/gwburg/10quik/blob/main/demo/4.png?raw=true)
#### Links to key tables appear after scanning
![jump to key table](https://github.com/gwburg/10quik/blob/main/demo/5.png?raw=true)
#### Table is converted to an excel sheet which can be downloaded or copy/pasted directly from the browser
![convert table to excel](https://github.com/gwburg/10quik/blob/main/demo/6.png?raw=true)
