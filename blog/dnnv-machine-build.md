# Building a machine for Neural Network Verification

We have just built a new machine **"PizzaBox"** for our research group.  Linhan and Hai built it on Oct 31st (Halloween) and it is up running since Nov 1.  The machine will be mainly used for our SE/PL research and especially for **neural network verification**, which is a bit different than an ML machine that focuses on training and therefore requires different hardware components and setup.

This machine is both cheaper than a machine with similar specs from Dell or Lenovo. It also runs a lot faster than computer servers available at GMU that we have access to.  We believe such customized computers are best for our purpose and hope that this post will be useful for others who are interested in building a similar machine.

## The Specs and Cost 

| Hardware | Details     | Cost | Notes |
|----------|-------------|------|-------|
| Motherboard| [ASUS Pro WS WRX80E-SAGE SE WiFi II AMD](https://www.amazon.com/gp/product/B0BZT9NF57/ref=ppx_yo_dt_b_asin_title_o05_s03?ie=UTF8&psc=1) | $1,070.52 | | 
| CPU      | AMD Ryzen™ Threadripper™ PRO 5975WX, 32-core, 64-Thread|  $2,749.98 |  from Microcenter
| GPU      | [GIGABYTE GeForce Nvidia 4090 RTX 24 GB VRAM](https://www.amazon.com/gp/product/B0BGP8FGNZ/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&th=1) |$1,699.99 | |
| RAM     | [Corsair Vengeance LPX 128GB](https://www.amazon.com/gp/product/B085WQXKM2/ref=ppx_yo_dt_b_asin_title_o05_s02?ie=UTF8&th=1) |$259.99 |
| HD  | [Western Digital BLACK 2TB SN850X NVMe](https://www.amazon.com/gp/product/B0B7CMZ3QH/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&th=1) |$119.99 | 
| PSU | [Corsair RM1000E](https://www.amazon.com/gp/product/B0BYQHWJXC/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)|$179.99 | 
| Case | [CORSAIR 7000D AIRFLOW Full-Tower--WHITE](https://www.amazon.com/gp/product/B09444VWX2/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&th=1) | $244.99 | 
| Fan (CPU) | [Cooler Master](https://www.amazon.com/gp/product/B07H25DZ3M/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1) | 119.00 | 
| Fan (Case) | 4 x Noctua 140mm  | $23.95 | | 
|    |         |**$6,468.4**   |    |


The CPU and GPU are the two main components we need for our DNN verification. The other components are flexible.  For CPU, we go with the AMD Threadripper 32 cores (64 threads).  This is the 2nd, not top, of the line because the Threadripper 64 cores costs quite a bit and would require additional paperwork to purchase.  For GPU, we go with the current top of the line for gaming, the NVIDIA RTX 4090.  


## Timeline
- 9/11: order components
- 10/31: complete the build (1 day)

## Building It
- Open the boxes!
- install ssd
- install cpu
- install ram
- install mb
- install psu
- install fans/airflow configuration
- install CPU cooler
- install GPU
- connecting cables/cable management
- test build/install OS



## Pros and Cons

## Thoughts



