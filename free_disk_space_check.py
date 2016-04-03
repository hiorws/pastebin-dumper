import os
from collections import namedtuple

_ntuple_diskusage = namedtuple('usage', 'total used free')

human_readble_divisor = 1024 * 1024

def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in gigabytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total / human_readble_divisor, used / human_readble_divisor, free / human_readble_divisor)


if __name__ == "__main__":
    root_disk_usage = disk_usage("/")
    print("Total Space: " + str(root_disk_usage.total) + " (GB)")
    print("Used Space: " + str(root_disk_usage.used) + " (GB)")
    print("Free Space: " + str(root_disk_usage.free) + " (GB)")
