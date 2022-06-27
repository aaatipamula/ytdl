import sqlite3

connection = sqlite3.connect('/home/aaatipamula/vscode_projects/yt-dlp-bot/file-server/database/db.sqlite')
cursor = connection.cursor()

# cursor.execute('''CREATE TABLE ids(reqids varchar(500), idone varchar(500), idtwo varchar(500))''')

# req_id = "jfjfjfjf"
# content_ids = "slslslslslsl"

# cursor.execute("INSERT INTO ids (reqids, idone) VALUES (\'%s\',\' %s\')" %(req_id, content_ids[1]))
# connection.commit()


b = cursor.execute('SELECT * FROM ids')
result = [x for x in b]
print(result)

connection.commit()
connection.close()
