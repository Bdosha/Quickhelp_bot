from datetime import datetime

import sqlite3
	 
con = sqlite3.connect('E:\\Python\\Bots\\маргей\\user_info.db')

def get_names(id):
	cursorObj = con.cursor()
	 
	cursorObj.execute(f'SELECT * FROM user_info WHERE id = {id}')
	
	data = cursorObj.fetchall()
	return data[0][1], data[0][2].split()[1]

def new_report(data):
    cursorObj = con.cursor()
    
    entities = (data['beg_time'], data['author'], data['fixer'], data['loc'], data['message'])
    cursorObj.execute(f'INSERT INTO actual_problems(beg_time, author, fixer, loc, message) VALUES{entities}')
	 
    con.commit()
	 

work_list = ['🖥️ IT специалист', '🧹  Уборщик', '🛠️ Ремонтный мастер', '🔍  Не определен']

def get_work(id):
    cursorObj = con.cursor()
    cursorObj.execute(
        f"SELECT * FROM actual_problems WHERE id = {id}")
    data = cursorObj.fetchall()
    if data == []:
        return "Задание больше не актуально", -1


    data = list(data[0])

    curtime = datetime.now()
    times = f'{str(curtime.hour)}:{str(curtime.minute)}'
    data[2] = times
    data.remove(data[3])
    data = tuple(data)
    cursorObj.execute(f'INSERT INTO problems_in_work(id, beg_time, start_time, author, fixer, loc, message) VALUES{data}')
    cursorObj.execute(f'DELETE from actual_problems where id = {id}')
    con.commit()

    return id

def view_report(id):
    cursorObj = con.cursor()
    cursorObj.execute(f'SELECT work FROM user_info WHERE id != {id}')
    worker = cursorObj.fetchall()[0][0]#
    #print(worker)
    cursorObj.execute(
        f"SELECT * FROM actual_problems WHERE fixer = {worker} AND author != {id} OR fixer = -1 AND author != {id}")
    data = cursorObj.fetchall()
    if data != []:
        data = data[0]
        names = get_names(data[4])
        text = f'Требуется: {work_list[data[5]]}\nМесто: {data[6]} \nКраткое описание: {data[7]}\n\n{data[1]}\n@{names[0]} {names[1]}'
        return text, data[0]
    else:
        return "Не найдено актуальных проблем", -1
        
def prev_page(id, last_check):
    cursorObj = con.cursor()
    cursorObj.execute(f'SELECT work FROM user_info WHERE id != {id}')
    worker = cursorObj.fetchall()[0][0]#
    #print(id, worker)
    cursorObj.execute(
        f"SELECT * FROM actual_problems WHERE fixer = {worker} AND author != {id} OR fixer = -1 AND author != {id}")
    data = cursorObj.fetchall()
    #print(data)
    if data != []:
        arr = []
        for i in data:
            arr.append(i[0])
        try:
            last_check = arr.index(last_check)
            data = data[(last_check - 1) % len(arr)]
        except:
            data = data[0]
        #data = data[best]
        names = get_names(data[4])
        text = f'Требуется: {work_list[data[5]]}\nМесто: {data[6]} \nКраткое описание: {data[7]}\n\n{data[1]}\n@{names[0]} {names[1]}'

        return text, data[0]
    else:
        return "Не найдено актуальных проблем", None
def next_page(id, last_check):
    cursorObj = con.cursor()
    cursorObj.execute(f'SELECT work FROM user_info WHERE id != {id}')
    worker = cursorObj.fetchall()[0][0]#
    #print(id, worker)
    cursorObj.execute(
        f"SELECT * FROM actual_problems WHERE fixer = {worker} AND author != {id} OR fixer = -1 AND author != {id}")
    data = cursorObj.fetchall()
    #print(data)
    if data != []:
        arr = []
        for i in data:
            arr.append(i[0])
        try:
            last_check = arr.index(last_check)
            data = data[(last_check + 1) % len(arr)]
        except:
            data = data[0]
        #data = data[best]
        names = get_names(data[4])
        text = f'Требуется: {work_list[data[5]]}\nМесто: {data[6]} \nКраткое описание: {data[7]}\n\n{data[1]}\n@{names[0]} {names[1]}'

        return text, data[0]
    else:
        return "Не найдено актуальных проблем", None
if __name__ == '__main__':
    #print(view_report(807290671))
    print(next_page(807290671, 10))
    #print(prev_page(807290671, 10))

            

#        text = f'Требуется: {work_list[data[5]]}\nМесто: {data[6]} \nКраткое описание: {data[7]}\n\n{data[4]}\nВы взялись за задание в {data[2]}'
