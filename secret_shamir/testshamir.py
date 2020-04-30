import shamir_exec

l = shamir_exec.create('2of2', 0, '', 128)
print(l)
print(shamir_exec.recover(l))