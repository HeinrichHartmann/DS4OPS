# Data Science for Effective Operations

This workshop has been held at differnt occasions with slightly different content.
Please look into the corresponding sub-folders to access the persented material.

* [Velocity London 2017](2017-10-17-Velocity-London/)

* [DevOpsDays Kiel 2018](2018-05-15-DOD-Kiel/)

## Bootstrap

If you have access to a machine with docker installed, you can boostrap
an interactive working environment with a single command:

```
$ ./docker.sh --run
[...]
#
# Data Science 4 Effective Operations
#
# starting jupyter notebook&lab ...
done
#
# Notebook:
# * local url: http://0.0.0.0:9999/?token=F2AlHtJBvHIqoLFEVfbMnUVFkcpFlJuZ
# * public url: http://11.22.33.192:9999/?token=F2AlHtJBvHIqoLFEVfbMnUVFkcpFlJuZ
#
# Lab:
# * local url: http://0.0.0.0:9998/?token=F2AlHtJBvHIqoLFEVfbMnUVFkcpFlJuZ
# * public url: http://11.22.33.192:9998/?token=F2AlHtJBvHIqoLFEVfbMnUVFkcpFlJuZ
```

## Datasets

* [Wes McKinley -- Python for Data Analysis (O'Reilly 2012)](http://shop.oreilly.com/product/0636920023784.do) -- Python, Jupyter (=IPython), numpy, matplotlib, pandas

* [Jaons Dixon -- Monitoring with Graphite (O'Reilly 2017)](http://shop.oreilly.com/product/0636920035794.do) -- Intro to Graphite. Also covers built in Analytics capabilities.

* [Baron Schwarz - Practical Scalability Analysis with the Universal Scalability Law (ebook, 2015)](https://www.vividcortex.com/resources/universal-scalability-law/)

* [Baron Schwarz - Essential Guide to Queuing Theory (ebook, 2016)](https://www.vividcortex.com/resources/queueing-theory)

* [John Rice -- Mathematical Data Analysis and Statistics (Duxbury Press, 2006)](https://www.amazon.com/Mathematical-Statistics-Analysis-Available-Enhanced/dp/0534399428) -- In depth coverage of Math-1,2,3 sessisons.

Also check out my writings on Statistics for Enginners

* [Statistics For Engineers (Atricle ACM-Queue/CACM)](http://queue.acm.org/detail.cfm?id=2903468)

* [Statistics For Engineers (Course Material on GitHub)](https://github.com/HeinrichHartmann/Statistics-for-Engineers)

## Further Reading and References

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
