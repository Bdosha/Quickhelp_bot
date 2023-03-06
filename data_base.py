import sqlite3
from datetime import datetime
 
con = sqlite3.connect('E:\\Python\\Bots\\маргей\\user_info.db')

work_list = ['🖥️ IT специалист', '🧹  Уборщик', '🛠️ Ремонтный мастер', '🔍  Не определен']

def get_from_base(id, table, part):
	cursorObj = con.cursor()
	 
	cursorObj.execute(f'SELECT {part} FROM {table} WHERE id = {id}')
	 
	rows = cursorObj.fetchall()

	return rows[0][0]

def get_names(id):
	cursorObj = con.cursor()
	 
	cursorObj.execute(f'SELECT * FROM user_info WHERE id = {id}')
	
	data = cursorObj.fetchall()
	return data[0][1], data[0][2].split()[1]


def sql_fetch(id = 0):
	 
	cursorObj = con.cursor()
	 
	cursorObj.execute('SELECT id FROM user_info')
	 
	rows = cursorObj.fetchall()
	#print(rows)
	if (id,) in rows:
		return get_from_base(id, 'user_info', 'status')
	return -1

def rereport(id): 
	cursorObj = con.cursor()
	temp = ['exist', 'location', 'fixer', 'dot', 'level', 'message', 'new_user']
	for i in temp:

		cursorObj.execute(f'UPDATE making_problem SET {i} = NULL where id = {id}')
	 
	con.commit()


def edit_problem(id, part, change):
	cursorObj = con.cursor()
	 
	cursorObj.execute(f'UPDATE making_problem SET {part} = "{change}" where id = {id}')
	 
	con.commit()

def edit_task(id, part, change):
	cursorObj = con.cursor()
	 
	cursorObj.execute(f'UPDATE tasks_view SET {part} = "{change}" where id = {id}')
	 
	con.commit()

def edit_base(id, table, part, change):
	cursorObj = con.cursor()
	 
	cursorObj.execute(f'UPDATE {table} SET {part} = "{change}" where id = {id}')
	 
	con.commit()


def view_my_work(id):
	if id == 0:
		return 'У вас нет задания', None
	cursorObj = con.cursor()

	cursorObj.execute(f'SELECT * FROM problems_in_work WHERE id = {str(id)}')
	
	data = cursorObj.fetchall()
	if data == []:
		return 'У вас нет задания', None
	data = list(data[0])
	names = get_names(data[4])
	if len(data[2].split(':')[1]) == 1:
		data[2] = data[2].split(':')[0] + ':0' + data[2].split(':')[1]
	text = f'Требуется: {work_list[data[5]]}\nМесто: {data[6]} \nКраткое описание: {data[7]}\n\n@{names[0]} {names[1]}\nВы взялись за задание в {data[2]}'


	return text, 0

def complite_work(id, problem):
	cursorObj = con.cursor()

	cursorObj.execute(f'DELETE from problems_in_work where id = {problem}')
	con.commit()
	cursorObj.execute(f'UPDATE user_info SET task = 0 where id = {id}')
	con.commit()
	

def cansel_work(id, problem):
	cursorObj = con.cursor()

	
	#print(problem, id)
	cursorObj.execute(f"SELECT * FROM problems_in_work WHERE id = {problem}")

	data = list(cursorObj.fetchall()[0])

	con.commit()
	data.remove(data[3])
	data = tuple(data)
	#print(data)
	cursorObj.execute(f'INSERT INTO actual_problems(id, beg_time, start_time, author, fixer, loc, message) VALUES{data}')
	cursorObj.execute(f'DELETE from problems_in_work where id = {problem}')
	cursorObj.execute(f'UPDATE user_info SET task = 0 where id = {id}')
	con.commit()

def get_names(id):
	cursorObj = con.cursor()
	 
	cursorObj.execute(f'SELECT * FROM user_info WHERE id = {id}')
	
	data = cursorObj.fetchall()
	return data[0][1], data[0][2].split()[1]

def get_ids(status):
	cursorObj = con.cursor()	 
	cursorObj.execute(f'SELECT id FROM user_info WHERE status = {status}')
	return cursorObj.fetchall()

def new_user(username, name, status, work = 0):
	cursorObj = con.cursor()
    
	entities = (username, name, status, work)
	cursorObj.execute(f'INSERT INTO new_users(username, name, status, work) VALUES{entities}')
	 
	con.commit()

def register(id, username):
	cursorObj = con.cursor()	 
	cursorObj.execute(f'SELECT * FROM new_users WHERE username = "{username}"')
	data = cursorObj.fetchall()
	#print(data)
	if data == []:
		return False
	data= data[0]
	entities = (id, data[1], data[2], data[3], data[4], 0)
	#print(data)
	#cursorObj.execute(f'UPDATE user_info SET id = {id} where username = "{username}"')
	cursorObj.execute(f'INSERT INTO user_info(id, username, name, status, work, task) VALUES{entities}')
	cursorObj.execute(f'INSERT INTO tasks_view(id) VALUES({id})')
	cursorObj.execute(f'INSERT INTO making_problem(id) VALUES({id})')
	cursorObj.execute(f'DELETE from new_users where username = "{username}"')
	con.commit()
	return True

if __name__ == '__main__':
	#cansel_work(1132908805, 1)
	pass