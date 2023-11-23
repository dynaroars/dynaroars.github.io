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
> *Before you start*
> - make sure to discharge yourself before touching the parts.


- **Open the boxes!**
- **Install SSD, CPU, RAM:**
  - _It's often a good idea to install smaller parts onto the motherboard first._ Working in the chassis can be more challenging due to limited space.
    - **CPU:**
      - Our CPU (59775wx) uses an sWRX8 socket. The installation is a bit different from the other consumer CPUs we've seen, so it took us a while to read the manual and figure out how.
    - **SSD:**
      - Very typical NVMe SSD installation. We removed a cover from the motherboard to expose the M.2 slot, and installed the SSD in the M.2_1 slot (M.2_1 is usually directly connected to the CPU, which gives better performance).
    - **Install RAM:**
      - Nothing special about the RAM installation, either. The CPU & MB together have 8 RAM slots, each with a dedicated channel, so we used every other slot for better thermal performance. On some MBs, multiple slots might share a channel; when this happens, the MB's manual will tell you what to do.
- **Install MB:**
  - Now we can put the MB into the chassis. The chassis comes with extra standoffs and panels for ATX MBs, so we had to remove them before proceeding (because we're using an Extended-ATX, which is larger). Fit the I/O panel into the slot on the back of the chassis, and align the standoffs to the holes on the MB. Lastly, tighten the screws in an alternating pattern (so the force is evenly distributed).
- **Install PSU:**
  - Our MB was interesting; it has one MB power connector, two CPU power connectors, and one extra PCIe power connector (which is not common). The GPU uses one of the 12VHPWR connectors. We attached the cables to the PSU first, because it will be much harder to add power connectors once the PSU is in the chassis.
- **Install fans/airflow configuration:**
  - We used the conventional airflow configuration, front-to-back/top. The 140 mm fans by Noctua are really powerful yet quiet. When shopping for fans, we aimed for airflow, not air pressure, because we're not using an AIO cooler (AIO needs higher pressure to push the air through the radiators). Once we installed the fans, we routed the wires to the back of the MB, preparing for cable management.
- **Install CPU cooler:**
  - Our cooler comes with thermal paste pre-applied, so all we did was put it on the CPU and tighten the screws in an alternating pattern. This fancy cooler has a 4-pin fan connector and another SATA power connector for RGB (which none of us care about).
- **Install GPU:**
  - To install the GPU, we had to take off the PCIe slot covers. Our GPU uses two slots, so we took off two of the covers, and then we just snapped the GPU into the 1st PCIe slot. Because the 4090 is so heavy, we had to order an additional GPU supporting bracket, or the MB would be at risk.
- **Connecting cables/cable management:**
  - The last step is to connect the cables. It's simple but kind of tedious. The only potentially challenging part is connecting the system panel connectors (power button, restart button, etc.). Cable management is optional but recommended; it requires patience and some skill. 
- **Test build/install OS:**
  - After connecting everything, we pluged in the power cord and gave the system a test drive. The hardware works as expected and everything was detected by the MB. So, we continued to install the OS. However, this didn't work as well as we expected. The system boots into the installation media with no issue, but as soon as we start the installation, the keyboard stops working. After spending a couple of hours looking for a solution online, we found out that disabling SR-IOV does the trick. Strange. [link](https://www.overclock.net/threads/asus-pro-ws-wrx80e-sage-se-wifi-installing-linux.1804562/). 


## Pros and Cons
- **Pros**
    - Fun
    - Easier to upgrade (comparing PCs that uses OEM parts)
    - Full control over your machine
- **Cons**
    - unexpected problems
    - time
    - risk of braking parts
## Thoughts



