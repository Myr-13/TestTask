import aiosqlite


class Database:
	def __init__(self):
		self.connection: aiosqlite.Connection = ...
		self._last_row_id: int = 0

	async def open_connection(self, path: str) -> None:
		self.connection = await aiosqlite.connect(path, autocommit=True)

	async def close_connection(self) -> None:
		await self.connection.close()

	async def execute_query(self, query: str, params: tuple = None) -> None:
		cursor: aiosqlite.Cursor = await self.connection.cursor()
		await cursor.execute(query, params)
		await self.connection.commit()
		self._last_row_id = cursor.lastrowid

	async def execute_get_query(self, query: str, params: tuple = None):
		cursor: aiosqlite.Cursor = await self.connection.cursor()
		await cursor.execute(query, params)
		return await cursor.fetchall()

	@property
	def last_id(self):
		return self._last_row_id


class ProjectDatabase(Database):
	def __init__(self):
		super().__init__()

	async def get_or_create_user(self, tg_id: int, create_if_not_found: bool = True):
		res = await self.execute_get_query("SELECT * FROM users WHERE id = ?", (tg_id,))
		if len(res) == 0 and create_if_not_found:
			await self.execute_query("INSERT INTO users(id) VALUES (?)", (tg_id,))
			return (await self.execute_get_query("SELECT * FROM users WHERE id = ?", (tg_id,)))[0]
		return res[0] if len(res) != 0 else []

	async def get_subscriptions(self):
		return await self.execute_get_query("SELECT * FROM subscriptions")

	async def get_subscription(self, subscription_id: int):
		return (await self.execute_get_query("SELECT * FROM subscriptions WHERE id = ?", (subscription_id,)))[0]

	async def get_subscription_models(self, subscription_id: int):
		return await self.execute_get_query("SELECT model_id FROM s_models WHERE sub_id = ?", (subscription_id,))

	async def get_model(self, model_id: int):
		return (await self.execute_get_query("SELECT * FROM models WHERE id = ?", (model_id,)))[0]

	async def set_user_subscription(self, user_id: int, sub_id: int, time: str):
		await self.execute_query("UPDATE users SET sub_type = ?, sub_time = ? WHERE id = ?", (sub_id, time, user_id))

	async def get_user_context(self, user_id: int):
		return await self.execute_get_query("SELECT * FROM u_context WHERE user_id = ?", (user_id,))

	async def add_context_message(self, user_id: int, message: str, role: str, image_data: str | None = None):
		return await self.execute_query("INSERT INTO u_context(user_id, role, image_data, content) VALUES (?, ?, ?, ?)", (user_id, role, image_data, message))

	async def clear_context(self, user_id: int):
		await self.execute_query("DELETE FROM u_context WHERE user_id = ?", (user_id,))

	async def set_credits_info(self, user_id: int, amount: int, time: float):
		await self.execute_query("UPDATE users SET credits = ?, next_credits_time = ? WHERE id = ?", (amount, time, user_id))

	async def set_user_setting(self, user_id: int, name: str, value: int | str | float):
		await self.execute_query(f"UPDATE users SET {name} = ? WHERE id = ?", (value, user_id))

	async def limit_user_context_length(self, user_id: int, limit: int):
		await self.execute_query(
			"DELETE FROM u_context WHERE timestamp NOT IN ("
			"SELECT timestamp FROM u_context WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?"
			")",
			(user_id, limit))


DATABASE = ProjectDatabase()
