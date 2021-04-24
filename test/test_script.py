from datetime import datetime

print(datetime.strptime("20210424-040000UTC", "%Y%m%d-%H%M%S%Z"))
print(datetime.now())