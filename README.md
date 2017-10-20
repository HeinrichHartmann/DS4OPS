# Data Science for Effective Operations

Workshop Material

## Plan

* S1 - Introduction
* S2 - Data Analysis with Python
* S3 - Data Analytics with Graphite and Circonus
* S4 - Math 1 - Descriptive Statistics
* S5 - Math 2 - Comparing Distributions
* S6 - Math 3 - Regressions and Correlation
* S7 - Math 4 - Time Series Analysis
* S8 - Math 5 - Queuing Theory and Universal Scalability

## Material

* docker.sh -- Script to bootstrap work environment (e.g. on [Strigo](http://strigo.io))

* work/S*.ipynb -- Jupyter Notebooks used in presentation

* work/lib/* -- supporting Python libraries

* work/datasets/* -- Example datasets and more

The material in this repository is incomplete, in so far as parts of the material were presented on the whiteboard.
So no digital artifacts are available for that.

## Further Reading and References

* [Wes McKinley -- Python for Data Analysis (O'Reilly 2012)](http://shop.oreilly.com/product/0636920023784.do) -- Python, Jupyter (=IPython), numpy, matplotlib, pandas

* [Jaons Dixon -- Monitoring with Graphite (O'Reilly 2017)](http://shop.oreilly.com/product/0636920035794.do) -- Intro to Graphite. Also covers built in Analytics capabilities.

* [Baron Schwarz - Practical Scalability Analysis with the Universal Scalability Law (ebook, 2015)](https://www.vividcortex.com/resources/universal-scalability-law/)

* [Baron Schwarz - Essential Guide to Queuing Theory (ebook, 2016)](https://www.vividcortex.com/resources/queueing-theory)

* [John Rice -- Mathematical Data Analysis and Statistics (Duxbury Press, 2006)](https://www.amazon.com/Mathematical-Statistics-Analysis-Available-Enhanced/dp/0534399428) -- In depth coverage of Math-1,2,3 sessisons.

## Datasets

| Name | Description | Size |
| --- | --- | --- |
| API_latencies.csv | 4 nodes. Measured once per minute | 8436 records/371kb |
| WebLatency.csv | 5 nodes. Measured once per minute | 10498 records/455kb |
| api_latency_histogram:1W@60sec.csv | 1 node. Distribution histogram. Once per minute | 2020 records/900kb |
| api_latency_samples:1W@60sec.json | 1 node. Raw samples. Once per minute. | 2020 records/6.9Mb |
| cluster_cpu_idle:1w@60s.csv | 10 nodes | 10080 records/1.0Mb |
| http_durations:1w@60s.csv | 15 nodes. Measured once per minute | 10080 records/1.2Mb |
| sycalls:1d@60s.csv | 1 node. 152 syscalls | 1441 records/2.2Mb |
| web_request_rate:4w@5M.csv | Request rate on a single web server | 8060 records/153kb |

## Events

* 2017-10-17,18 [#VelocityLondon](https://conferences.oreilly.com/velocity/vl-eu/public/schedule/speaker/205186)
