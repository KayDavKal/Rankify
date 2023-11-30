import aiosqlite

async def table():
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()
  await c.execute('''CREATE TABLE IF NOT EXISTS user (
    guild_id TEXT,
    user_id TEXT,
    xp INTEGER,
    level INTEGER,
    balance INTEGER,
    bank INTERGER
  )''')
  await conn.commit()
  await conn.close()

async def add_user(guild_id, user_id):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()
  await c.execute('''INSERT INTO user (guild_id, user_id, xp, level, balance, bank) VALUES (?, ?, 0, 1, 0, 0)''', (guild_id, user_id, 0, 1, 0, 0))
  await conn.commit()
  await conn.close()

async def get_user(guild_id, user_id):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()
  await c.execute(f'SELECT user_id FROM user WHERE guild_id = ? AND user_id = ?' , (guild_id, user_id))
  user = await c.fetchone()
  if user:
    return True
  else:
    return False
  await conn.close()

async def get_money(guild_id, user_id):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()

  await c.execute('''SELECT balance FROM user WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  if result is None:
    await c.execute('''INSERT INTO user VALUES (?, ?, ?, ?)''', (guild_id, user_id, 0, 0))

  await conn.commit()
  await conn.close()
  return result[0]

async def add_money(guild_id, user_id, money):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()
  await c.execute('''SELECT balance FROM user WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  if result:
    new_balance = result[0] + money
    await c.execute('''UPDATE user SET balance = ? WHERE guild_id = ? AND user_id = ?''', (new_balance, guild_id, user_id))
  else:
    await c.execute('''INSERT INTO user (guild_id, user_id, balance, bank) VALUES (?, ?, ?, ?)''', (guild_id, user_id, money, 0))

  await conn.commit()
  await conn.close()
  return new_balance

async def sub_money(guild_id, user_id, money):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()
  await c.execute('''SELECT balance FROM user WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  if result:
    new_balance = result[0] - money
    await c.execute('''UPDATE user SET balance = ? WHERE guild_id = ? AND user_id = ?''', (new_balance, guild_id, user_id))
  else:
    return False

  await conn.commit()
  await conn.close()
  return new_balance

async def get_bank(guild_id, user_id):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()

  await c.execute('''SELECT bank FROM user WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()

  await conn.close()
  return result[0]

async def add_bank(guild_id, user_id, money):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()
  await c.execute('''SELECT bank FROM user WHERE user_id = ?''', (user_id,))
  result = await c.fetchone()
  if result:
    new_bank = result[0] + money
    await c.execute('''UPDATE user SET bank = ? WHERE user_id = ?''', (new_bank, user_id))
  else:
    await c.execute('''INSERT INTO user (guild_id, user_id, balance, bank) VALUES (?, ?, ?, ?)''', (guild_id, user_id, 0, money))

  await conn.commit()
  await conn.close()
  return new_bank

async def sub_bank(guild_id, user_id, money):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()
  await c.execute('''SELECT bank FROM user WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  if result:
    new_bank = result[0] - money
    await c.execute('''UPDATE user SET bank = ? WHERE guild_id = ? AND user_id = ?''', (new_bank, guild_id, user_id))
  else:
    return False

  await conn.commit()
  await conn.close()
  return new_bank

async def get_xp(guild_id, user_id):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()

  await c.execute('''SELECT xp FROM user WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()

  await conn.commit()
  await conn.close()

  return result

async def add_xp(guild_id, user_id, xp):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()

  await c.execute('''SELECT xp FROM user WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()

  if result:
      current_xp = int(result[0])
      new_xp = current_xp + xp
      await c.execute('''UPDATE user SET xp = ? WHERE guild_id = ? AND user_id = ?''', (new_xp, guild_id, user_id))
  else:
      level = 0
      await c.execute('''INSERT INTO user (guild_id, user_id, level, xp) VALUES (?, ?, ?, ?)''', (guild_id, user_id, level, xp))

  await conn.commit()
  await conn.close()

async def get_level(guild_id, user_id):
  conn = await aiosqlite.connect('user.db')
  c = await conn.cursor()

  await c.execute('''SELECT level FROM user WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))

  result = await c.fetchone()
  if result:
    level = int(result[0])
    return level
  else:
    return None

  await conn.commit()
  await conn.close()
