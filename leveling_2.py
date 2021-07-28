from ReadWriteMemory import ReadWriteMemory

rwm = ReadWriteMemory()

process = rwm.get_process_by_name('Raid.exe')

health_pointer = process.get_pointer(0x004e4dbc, offsets=[0xf4])

print(process)