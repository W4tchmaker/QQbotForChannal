import sqlite3
import os
import random
import asyncio
from config import resources_path


class AnkeDatabase:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db_directory = os.path.join(resources_path, "anke_database")
        self.db_path = os.path.join(self.db_directory, f"{db_name}.db")
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)
        self.conn = sqlite3.connect(self.db_path)

    async def initialize(self):
        await self.create_themes_table()
        await self.create_ankes_table()

    async def close(self):
        self.conn.close()
        return "已关闭数据库"

    async def create_themes_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS themes (
                id INTEGER PRIMARY KEY,
                theme TEXT,
                status INTEGER,
                channel_id TEXT,
                flag INTEGER,
                chosen_num INTEGER
            )
        ''')
        self.conn.commit()

    # status 0 关闭 1 正在开放 2 暂停等待后续

    async def create_ankes_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ankes (
                id INTEGER PRIMARY KEY,
                theme_id INTEGER,
                num INTEGER,
                userid TEXT,
                content TEXT,
                FOREIGN KEY (theme_id) REFERENCES themes(id)
            )
        ''')
        self.conn.commit()

    async def insert_theme(self, theme: str, channel_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM themes WHERE channel_id=? AND status=1', (channel_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('INSERT INTO themes (theme, status, channel_id, flag, chosen_num) VALUES (?, ?, ?, ?, ?)',
                           (theme, 1, channel_id, 1, 0))
            self.conn.commit()
            return f"已创建安价: {theme}"
        else:
            return "当前频道有安价进行中：\n" + await self.view_anke(channel_id)

    async def insert_anke(self, channel_id, userid: str, content: str):
        theme_id, theme_name, anke_id = await self.current_anke(channel_id)
        if anke_id:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO ankes (theme_id, num, userid, content) VALUES (?, ?, ?, ?)',
                           (theme_id, anke_id, userid, content))
            cursor.execute('UPDATE themes SET flag = flag + 1 WHERE id = ?', (theme_id,))
            self.conn.commit()
            string = await self.view_anke(channel_id)
            string = string + f"添加至选项{anke_id}"
            return string
        else:
            return "当前无安价或安价以结束"

    async def open_close_anke(self, channel_id, reopen=0):
        reply = await self.view_anke(channel_id, is_to_close=(reopen == 0))
        cursor = self.conn.cursor()
        if reopen != 1:
            cursor.execute('UPDATE themes SET status = ? where channel_id = ? and status = 1', (reopen, channel_id,))
            self.conn.commit()
        if reopen == 0:
            reply = reply + "\n该安价已结束。"
        elif reopen == 1:
            cursor.execute('SELECT * FROM themes WHERE channel_id=? AND status=2', (channel_id,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute('UPDATE themes SET status = 1 where channel_id = ? and status = 2',
                               (reopen, channel_id,))
                self.conn.commit()
                return "已重启当前频道安价。"
            else:
                return "当前频道有安价进行中：\n" + await self.view_anke(channel_id)
        elif reopen == 2:
            reply = reply + "\n该安价已暂停收集。"
        return reply

    async def delete_anke(self, userid, channel_id, num, is_admin=False):
        cursor = self.conn.cursor()
        theme_id, theme_name, anke_id = await self.current_anke(channel_id)
        num = int(num)
        try:
            if is_admin:
                cursor.execute('DELETE FROM ankes WHERE num = ? and theme_id = ?;', (num, theme_id,))
            else:
                cursor.execute('DELETE FROM ankes WHERE userid = ? and num = ? and theme_id = ?;',
                               (userid, num, theme_id,))
            self.conn.commit()
            if cursor.rowcount > 0:
                string = f"将{theme_name}的安价 {num}号选项删除。"
            else:
                string = f"无法删除该安价。"
            return string
        except Exception as e:
            print(e)
            return "删除错误"

    async def current_anke(self, channel_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT * FROM themes where channel_id = ? and status = 1', (channel_id,))
            theme = cursor.fetchone()
            return theme[0], theme[1], theme[-2]
        except Exception as e:
            print(e)
            return -1, False, False

    async def view_theme(self, channel_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM themes where channel_id = ?', (channel_id,))
        themes = cursor.fetchall()
        if len(themes) == 0:
            return "当前频道无历史安价。"
        string = "该频道历史安价：\n"
        for theme in themes:
            if theme[2] == 0:
                cursor.execute('SELECT * FROM ankes where theme_id = ? and num = ?', (theme[0], theme[-1]))
                row = cursor.fetchall()
                if row:
                    option_content = row[0][-1]
                    user = row[0][3]
                    string = string + f"{theme[1]}的安价已结束，中奖安价{user}:\n {option_content}\n"
                else:
                    return "安价历史数据库错误"
            else:
                string = string + f"{theme[1]}的安价进行中，输入\"安价 \"进行参与，\"安价查看 \"查看详情"
        return string

    async def view_anke(self, channel_id, is_to_close=False):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id,theme FROM themes WHERE channel_id = ? and status = 1', (channel_id,))
        row = cursor.fetchone()
        if row:
            theme_id = row[0]
            theme = row[1]
        else:
            return "当前频道无正在进行的安价，输入安价历史查看历史安价。"

        cursor.execute('SELECT * FROM ankes where theme_id = ?', (theme_id,))
        ankes = cursor.fetchall()
        string = f"安价 {theme}:\n"
        ranint = random.randint(0, len(ankes) - 1)
        for i in range(len(ankes)):
            string = string + "√ " * (i == ranint) * is_to_close
            string = string + f"{ankes[i][2]}\t{ankes[i][-1]}\n"
        if is_to_close:
            selection = ankes[ranint]
            choice_item = f"1D{len(ankes)}={ranint + 1} <@{selection[3]}>的安价被选中"

            cursor.execute('UPDATE themes SET chosen_num = ? where channel_id = ? and status=1',
                           (selection[2], channel_id,))
            self.conn.commit()
            string = string + choice_item
        return string


aj = AnkeDatabase("anjia_database")
asyncio.run(aj.initialize())
