from databaseTool import userTable
from databaseTool import detailTable

userTable.create()
userTable.insert('dss', '123')
userTable.insert('hdhr', '456')
userTable.insert('fsawe', '789')
userTable.select()
detailTable.create()
'''detailTable.insert('1', 'google.com', 'abc', '123')
detailTable.insert('1', 'youtube.com', 'def', '456')
detailTable.insert('1', 'facebook.com', 'ghi', '789')

detailTable.insert('2', 'google.com', 'abcd', '1234')
detailTable.insert('2', 'youtube.com', 'defg', '4567')
detailTable.insert('2', 'facebook.com', 'ghij', '7890')

detailTable.insert('3', 'google.com', 'abcde', '12345')
detailTable.insert('3', 'youtube.com', 'defgh', '45678')
detailTable.insert('3', 'facebook.com', 'ghijk', '78901')
detailTable.select('1')
detailTable.select('2')
detailTable.select('3')'''
userTable.select()
userTable.delete('1')