import sqlite3
from Functions import quick_sort

con = sqlite3.connect('game_results.db')
cur = con.cursor()


def add(nick, level, coins):
    res = cur.execute(f"""SELECT nickname, level, coins FROM RESULTS WHERE nickname = '{nick}'""").fetchone()
    if res:
        nick1 = res[0]
        level1 = res[1]
        coins1 = res[2]
        if nick == nick1 and level == level1:  # Если этот ник уже есть в бд
            if coins > coins1:  # А монет собрано больше
                cur.execute(f"""UPDATE RESULTS  
                                    SET coins = {coins}
                                    WHERE nickname = '{nick}' AND level = {level}""")  # Обновляем результат
        else:  # Если такого ника ещё нет
            que = 'INSERT INTO RESULTS(nickname, level, coins) ' \
                  'VAlUES("' + nick + '", ' + str(level) + ', ' + str(coins) + ')'
            cur.execute(que)  # Добавляем в БД
        con.commit()
    else:  # Если такого ника ещё нет
        que = 'INSERT INTO RESULTS(nickname, level, coins) ' \
              'VAlUES("' + nick + '", ' + str(level) + ', ' + str(coins) + ')'
        cur.execute(que)  # Добавляем в БД
    con.commit()  # Подтверждаем изменение


def conclusion(nick, level):
    return cur.execute(f"""SELECT nickname, coins FROM RESULTS
    WHERE nickname = '{nick}' AND level = {level}""").fetchone()


def top5(level):
    res = cur.execute(f"""SELECT nickname, coins FROM RESULTS
    WHERE level = {level}""").fetchall()
    res_sort = quick_sort(res)
    return res_sort
