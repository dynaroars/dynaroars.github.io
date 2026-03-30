


GMU =         [150000, 97242, 50000, 510509, 30000, 1199871, 16000, 32798]
GMU_myshare = [100000, 97242, 50000, 510509, 30000,  399879, 16000, 32798]
GMU_myshare_notpi = []

UNL =         [10000, 142177, 549990, 16000]   #174975 - 32798
UNL_myshare = [10000, 142177, 158850, 16000]   #174975
UNL_myshare_notpi = [158850]


GMU_total = sum(GMU)
UNL_total = sum(UNL)
total = GMU_total + UNL_total

GMU_myshare = sum(GMU_myshare)
UNL_myshare = sum(UNL_myshare)
myshare = GMU_myshare + UNL_myshare


GMU_myshare_aspi = GMU_myshare - sum(GMU_myshare_notpi)
UNL_myshare_aspi = UNL_myshare - sum(UNL_myshare_notpi)
myshare_aspi = GMU_myshare_aspi + UNL_myshare_aspi

print(f"%Total {total:,}")
print(f"%My share {myshare:,}")
print(f"%My share as PI {myshare_aspi:,}")

print(f"%GMU_total {GMU_total:,}")
print(f"%GMU_myshare {GMU_myshare:,}")
print(f"%GMU_myshare_aspi {GMU_myshare_aspi:,}")


