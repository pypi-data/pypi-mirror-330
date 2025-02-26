from .database import cache_db_cursor, cache_db
from .helpers import _re_cache
import math
import json
from typing import Optional
from .game_data_classes import Item, Drop, Reward, Resource, Map, Monster, Task, Achievement, AchievementReward
from .log import logger

class Account:
    
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        self.api = api

    # --- Account Functions ---
    def get_bank_details(self) -> dict:
        """Retrieve the details of the player's bank account."""
        endpoint = "my/bank"
        return self.api._make_request("GET", endpoint, source="get_bank_details")

    def get_bank_items(self, item_code=None, page=1) -> dict:
        """Retrieve the list of items stored in the player's bank."""
        query = "size=100"
        query += f"&item_code={item_code}" if item_code else ""
        query += f"&page={page}"
        endpoint = f"my/bank/items?{query}"
        return self.api._make_request("GET", endpoint, source="get_bank_items")

    def get_ge_sell_orders(self, item_code=None, page=1) -> dict:
        """Retrieve the player's current sell orders on the Grand Exchange."""
        query = "size=100"
        query += f"&item_code={item_code}" if item_code else ""
        query += f"&page={page}"
        endpoint = f"my/grandexchange/orders?{query}"
        return self.api._make_request("GET", endpoint, source="get_ge_sell_orders")

    def get_ge_sell_history(self, item_code=None, item_id=None, page=1) -> dict:
        """Retrieve the player's Grand Exchange sell history."""
        query = "size=100"
        query += f"&item_code={item_code}" if item_code else ""
        query += f"&id={item_id}" if item_id else ""
        query += f"&page={page}"
        endpoint = f"my/grandexchange/history?{query}"
        return self.api._make_request("GET", endpoint, source="get_ge_sell_history")

    def get_account_details(self) -> dict:
        """Retrieve details of the player's account."""
        endpoint = "my/details"
        return self.api._make_request("GET", endpoint, source="get_account_details")

class Character:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        self.api = api

    # --- Character Functions ---
    def create_character(self, name: str, skin: str = "men1") -> dict:
        """
        Create a new character with the given name and skin.

        Args:
            name (str): The name of the new character.
            skin (str): The skin choice for the character (default is "men1").

        Returns:
            dict: Response data with character creation details.
        """
        endpoint = "characters/create"
        json = {"name": name, "skin": skin}
        return self.api._make_request("POST", endpoint, json=json, source="create_character")

    def delete_character(self, name: str) -> dict:
        """
        Delete a character by name.

        Args:
            name (str): The name of the character to delete.

        Returns:
            dict: Response data confirming character deletion.
        """
        endpoint = "characters/delete"
        json = {"name": name}
        return self.api._make_request("POST", endpoint, json=json, source="delete_character")

    def get_logs(self, page: int = 1) -> dict:
        """_summary_

        Args:
            page (int): Page number for results. Defaults to 1.

        Returns:
            dict: Response data with character logs
        """
        query = f"size=100&page={page}"
        endpoint = f"my/logs?{query}"
        self.api._make_request("GET", endpoint, source="get_logs")

class Actions:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        self.api = api

    # --- Character Actions ---
    def move(self, x: int, y: int) -> dict:
        """
        Move the character to a new position.

        Args:
            x (int): X-coordinate to move to.
            y (int): Y-coordinate to move to.

        Returns:
            dict: Response data with updated character position.
        """
        endpoint = f"my/{self.api.char.name}/action/move"
        json = {"x": x, "y": y}
        res = self.api._make_request("POST", endpoint, json=json, source="move")
        return res

    def rest(self) -> dict:
        """
        Perform a rest action to regain energy.

        Returns:
            dict: Response data confirming rest action.
        """
        endpoint = f"my/{self.api.char.name}/action/rest"
        res = self.api._make_request("POST", endpoint, source="rest")
        return res

    # --- Item Action Functions ---
    def equip_item(self, item_code: str, slot: str, quantity: int = 1) -> dict:
        """
        Equip an item to a specified slot.

        Args:
            item_code (str): The code of the item to equip.
            slot (str): The equipment slot.
            quantity (int): The number of items to equip (default is 1).

        Returns:
            dict: Response data with updated equipment.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/equip"
        json = {"code": item_code, "slot": slot, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="equip_item")
        return res

    def unequip_item(self, slot: str, quantity: int = 1) -> dict:
        """
        Unequip an item from a specified slot.

        Args:
            slot (str): The equipment slot.
            quantity (int): The number of items to unequip (default is 1).

        Returns:
            dict: Response data with updated equipment.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/unequip"
        json = {"slot": slot, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="unequip_item")
        return res

    def use_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Use an item from the player's inventory.

        Args:
            item_code (str): Code of the item to use.
            quantity (int): Quantity of the item to use (default is 1).

        Returns:
            dict: Response data confirming the item use.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/use"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="use_item")
        return res

    def delete_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Delete an item from the player's inventory.

        Args:
            item_code (str): Code of the item to delete.
            quantity (int): Quantity of the item to delete (default is 1).

        Returns:
            dict: Response data confirming the item deletion.
        """
        endpoint = f"my/{self.api.char.name}/action/delete-item"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="delete_item")
        return res

    # --- Resource Action Functions ---
    def fight(self) -> dict:
        """
        Initiate a fight with a monster.

        Returns:
            dict: Response data with fight details.
        """
        endpoint = f"my/{self.api.char.name}/action/fight"
        res = self.api._make_request("POST", endpoint, source="fight")
        return res

    def gather(self) -> dict:
        """
        Gather resources, such as mining, woodcutting, or fishing.

        Returns:
            dict: Response data with gathered resources.
        """
        endpoint = f"my/{self.api.char.name}/action/gathering"
        res = self.api._make_request("POST", endpoint, source="gather")
        return res

    def craft_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Craft an item.

        Args:
            item_code (str): Code of the item to craft.
            quantity (int): Quantity of the item to craft (default is 1).

        Returns:
            dict: Response data with crafted item details.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/crafting"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="craft_item")
        return res

    def recycle_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Recycle an item.

        Args:
            item_code (str): Code of the item to recycle.
            quantity (int): Quantity of the item to recycle (default is 1).

        Returns:
            dict: Response data confirming the recycling action.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/recycle"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="recycle_item")
        return res

    # --- Bank Action Functions ---
    def bank_deposit_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Deposit an item into the bank.

        Args:
            item_code (str): Code of the item to deposit.
            quantity (int): Quantity of the item to deposit (default is 1).

        Returns:
            dict: Response data confirming the deposit.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/bank/deposit"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="bank_deposit_item")
        return res

    def bank_deposit_gold(self, quantity: int) -> dict:
        """
        Deposit gold into the bank.

        Args:
            quantity (int): Amount of gold to deposit.

        Returns:
            dict: Response data confirming the deposit.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/bank/deposit/gold"
        json = {"quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="bank_deposit_gold")
        return res

    def bank_withdraw_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Withdraw an item from the bank.

        Args:
            item_code (str): Code of the item to withdraw.
            quantity (int): Quantity of the item to withdraw (default is 1).

        Returns:
            dict: Response data confirming the withdrawal.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/bank/withdraw"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="bank_withdraw_item")
        return res

    def bank_withdraw_gold(self, quantity: int) -> dict:
        """
        Withdraw gold from the bank.

        Args:
            quantity (int): Amount of gold to withdraw.

        Returns:
            dict: Response data confirming the withdrawal.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/bank/withdraw/gold"
        json = {"quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="bank_withdraw_gold")
        return res

    def bank_buy_expansion(self) -> dict:
        """
        Purchase an expansion for the bank.

        Returns:
            dict: Response data confirming the expansion purchase.
        """
        endpoint = f"my/{self.api.char.name}/action/bank/buy_expansion"
        res = self.api._make_request("POST", endpoint, source="bank_buy_expansion")
        return res


    # --- Taskmaster Action Functions ---
    def taskmaster_accept_task(self) -> dict:
        """
        Accept a new task from the taskmaster.

        Returns:
            dict: Response data confirming task acceptance.
        """
        endpoint = f"my/{self.api.char.name}/action/tasks/new"
        res = self.api._make_request("POST", endpoint, source="accept_task")
        return res

    def taskmaster_complete_task(self) -> dict:
        """
        Complete the current task with the taskmaster.

        Returns:
            dict: Response data confirming task completion.
        """
        endpoint = f"my/{self.api.char.name}/action/tasks/complete"
        res = self.api._make_request("POST", endpoint, source="complete_task")
        return res

    def taskmaster_exchange_task(self) -> dict:
        """
        Exchange the current task with the taskmaster.

        Returns:
            dict: Response data confirming task exchange.
        """
        endpoint = f"my/{self.api.char.name}/action/tasks/exchange"
        res = self.api._make_request("POST", endpoint, source="exchange_task")
        return res

    def taskmaster_trade_task(self, item_code: str, quantity: int = 1) -> dict:
        """
        Trade a task item with another character.

        Args:
            item_code (str): Code of the item to trade.
            quantity (int): Quantity of the item to trade (default is 1).

        Returns:
            dict: Response data confirming task trade.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/tasks/trade"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="trade_task")
        return res

    def taskmaster_cancel_task(self) -> dict:
        """
        Cancel the current task with the taskmaster.

        Returns:
            dict: Response data confirming task cancellation.
        """
        endpoint = f"my/{self.api.char.name}/action/tasks/cancel"
        res = self.api._make_request("POST", endpoint, source="cancel_task")
        return res
 
class Items:
    def __init__(self, api):
        self.api = api
        self.cache = {}
        self.all_items = []
    
    def _cache_items(self):
        
        if _re_cache(self.api, "item_cache"):
            cache_db_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS item_cache  (
                name TEXT PRIMARY KEY,
                code TEXT,
                type TEXT,
                subtype TEXT,
                description TEXT,
                effects TEXT,
                craft TEXT,
                tradeable BOOL
            )
            """
            )
            cache_db.commit()
                    
            endpoint = "items?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_items")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of items", extra={"char": self.api.char.name})

            all_items = []
            for i in range(pages):
                endpoint = f"items?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_items", include_headers=True)
                item_list = res["json"]["data"]


                for item in item_list:
                    name = item["name"]
                    code = item["code"]
                    type_ = item["type"]
                    subtype = item.get("subtype", "")
                    description = item.get("description", "")
                    effects = json.dumps(item.get("effects", []))  # Serialize the effects as JSON
                    craft = json.dumps(item["craft"]) if item.get("craft") else None  # Serialize craft if available
                    tradeable = item.get("tradeable", False)

                    # Insert the item into the database
                    cache_db.execute("""
                    INSERT OR REPLACE INTO item_cache (name, code, type, subtype, description, effects, craft, tradeable)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (name, code, type_, subtype, description, effects, craft, tradeable))
                    
                    cache_db.commit()


            self.cache = {item.code: item for item in all_items}
            self.all_items = all_items

            logger.debug(f"Finished caching {len(all_items)} items", extra={"char": self.api.char.name})

    def _filter_items(self, craft_material=None, craft_skill=None, max_level=None, min_level=None, 
                      name=None, item_type=None):

        # Base SQL query to select all items
        query = "SELECT * FROM item_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if craft_material:
            query += " AND EXISTS (SELECT 1 FROM json_each(json_extract(item_cache.craft, '$.items')) WHERE json_each.value LIKE ?)"
            params.append(f"%{craft_material}%")
        
        if craft_skill:
            query += " AND json_extract(item_cache.craft, '$.skill') = ?"
            params.append(craft_skill)

        if max_level is not None:
            query += " AND item_cache.level <= ?"
            params.append(max_level)

        if min_level is not None:
            query += " AND item_cache.level >= ?"
            params.append(min_level)

        if name:
            name_pattern = f"%{name}%"
            query += " AND item_cache.name LIKE ?"
            params.append(name_pattern)

        if item_type:
            query += " AND item_cache.type = ?"
            params.append(item_type)

        # Execute the query
        cache_db_cursor.execute(query, params)
        rows = cache_db_cursor.fetchall()


        # Close the connection
        cache_db_cursor.close()
        cache_db.close()

        # Return the filtered items
        return rows

    def get(self, item_code=None, **filters):
        """
        Get a specific item by its code or filter items based on the provided parameters.

        Args:
            item_code (str, optional): The code of a specific item to retrieve.
            filters (dict, optional): A dictionary of filter parameters. Supported filters:
                - craft_material (str): Filter by the code of the craft material used by the item.
                - craft_skill (str): Filter by the craft skill required for the item.
                - max_level (int): Filter items with a level less than or equal to the specified value.
                - min_level (int): Filter items with a level greater than or equal to the specified value.
                - name (str): Search for items whose names match the given pattern (case-insensitive).
                - item_type (str): Filter by item type (e.g., 'weapon', 'armor', etc.).

        Returns:
            dict or list: Returns a single item if `item_code` is provided, or a list of items
            matching the filter criteria if `filters` are provided.
        """

        if not self.all_items:
            self._cache_items()
        if item_code:
            return self.cache.get(item_code)
        return self._filter_items(**filters)

class Maps:
    def __init__(self, api):
        self.api = api
        self.cache = {}
        self.all_maps = []

    def _cache_maps(self):
        if _re_cache(self.api, "map_cache"):
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS map_cache (
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                content_code TEXT,
                content_type TEXT,
                PRIMARY KEY (x, y)
            )
            """)
            cache_db.commit()

            endpoint = "maps?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_maps")
            pages = math.ceil(int(res["pages"]) / 100)
            
            logger.debug(f"Caching {pages} pages of maps", extra={"char": self.api.char.name})
            
            all_maps = []
            for i in range(pages):
                endpoint = f"maps?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_maps")
                map_list = res["data"]
                
                for map_item in map_list:
                    x = map_item['x']
                    y = map_item['y']
                    content_code = map_item.get('content_code', '')
                    content_type = map_item.get('content_type', '')
                    
                    # Insert or replace the map into the database
                    cache_db.execute("""
                    INSERT OR REPLACE INTO map_cache (x, y, content_code, content_type)
                    VALUES (?, ?, ?, ?)
                    """, (x, y, content_code, content_type))
                    cache_db.commit()
                    
                    all_maps.append(map_item)

                logger.debug(f"Fetched {len(map_list)} maps from page {i+1}", extra={"char": self.api.char.name})

            self.cache = {f"{item['x']}/{item['y']}": item for item in all_maps}
            self.all_maps = all_maps

            logger.debug(f"Finished caching {len(all_maps)} maps", extra={"char": self.api.char.name})

    def _filter_maps(self, map_content=None, content_type=None):
        # Base SQL query to select all maps
        query = "SELECT * FROM map_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if map_content:
            query += " AND content_code LIKE ?"
            params.append(f"%{map_content}%")

        if content_type:
            query += " AND content_type = ?"
            params.append(content_type)

        # Execute the query
        cache_db_cursor.execute(query, params)
        rows = cache_db_cursor.fetchall()

        # Return the filtered maps
        return rows

    def get(self, x=None, y=None, **filters):
        """
        Retrieves a specific map by coordinates or filters maps based on provided parameters.
        
        Args:
            x (int, optional): Map's X coordinate.
            y (int, optional): Map's Y coordinate.
            **filters: Optional filter parameters. Supported filters:
                - map_content: Search maps by content (case-insensitive).
                - content_type: Filter maps by content type.

        Returns:
            dict or list: A specific map if coordinates are provided, else a filtered list of maps.
        """
        if not self.all_maps:
            self._cache_maps()
        if x is not None and y is not None:
            return self.cache.get(f"{x}/{y}")
        return self._filter_maps(**filters)

class Monsters:
    def __init__(self, api):
        self.api = api
        self.cache = {}
        self.all_monsters = []

    def _cache_monsters(self):
        if _re_cache(self.api, "monster_cache"):
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS monster_cache (
                code TEXT PRIMARY KEY,
                name TEXT,
                level INTEGER,
                hp INTEGER,
                attack_fire INTEGER,
                attack_earth INTEGER,
                attack_water INTEGER,
                attack_air INTEGER,
                res_fire INTEGER,
                res_earth INTEGER,
                res_water INTEGER,
                res_air INTEGER,
                min_gold INTEGER,
                max_gold INTEGER,
                drops TEXT
            )
            """)
            cache_db.commit()

            endpoint = "monsters?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_monsters")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of monsters", extra={"char": self.api.char.name})

            all_monsters = []
            for i in range(pages):
                endpoint = f"monsters?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_monsters")
                monster_list = res["data"]

                for monster in monster_list:
                    code = monster["code"]
                    name = monster["name"]
                    level = monster["level"]
                    hp = monster["hp"]
                    attack_fire = monster["attack_fire"]
                    attack_earth = monster["attack_earth"]
                    attack_water = monster["attack_water"]
                    attack_air = monster["attack_air"]
                    res_fire = monster["res_fire"]
                    res_earth = monster["res_earth"]
                    res_water = monster["res_water"]
                    res_air = monster["res_air"]
                    min_gold = monster["min_gold"]
                    max_gold = monster["max_gold"]
                    drops = json.dumps([Drop(**drop).__dict__ for drop in monster["drops"]])  # Serialize drops as JSON

                    # Insert or replace the monster into the database
                    cache_db.execute("""
                    INSERT OR REPLACE INTO monster_cache (
                        code, name, level, hp, attack_fire, attack_earth, attack_water, attack_air,
                        res_fire, res_earth, res_water, res_air, min_gold, max_gold, drops
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (code, name, level, hp, attack_fire, attack_earth, attack_water, attack_air,
                        res_fire, res_earth, res_water, res_air, min_gold, max_gold, drops))
                    cache_db.commit()

                    all_monsters.append(monster)

                logger.debug(f"Fetched {len(monster_list)} monsters from page {i+1}", extra={"char": self.api.char.name})

            self.cache = {monster["code"]: monster for monster in all_monsters}
            self.all_monsters = all_monsters

            logger.debug(f"Finished caching {len(all_monsters)} monsters", extra={"char": self.api.char.name})
            
    def _filter_monsters(self, drop=None, max_level=None, min_level=None):
        # Base SQL query to select all monsters
        query = "SELECT * FROM monster_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if drop:
            query += " AND EXISTS (SELECT 1 FROM json_each(json_extract(monster_cache.drops, '$')) WHERE json_each.value LIKE ?)"
            params.append(f"%{drop}%")

        if max_level is not None:
            query += " AND monster_cache.level <= ?"
            params.append(max_level)

        if min_level is not None:
            query += " AND monster_cache.level >= ?"
            params.append(min_level)

        # Execute the query
        cache_db_cursor.execute(query, params)
        rows = cache_db_cursor.fetchall()

        # Return the filtered monsters
        return rows

    def get(self, monster_code=None, **filters):
        """
        Retrieves a specific monster or filters monsters based on provided parameters.
        
        Args:
            monster_code (str, optional): Retrieve monster by its unique code.
            **filters: Optional filter parameters. Supported filters:
                - drop: Filter monsters that drop a specific item.
                - max_level: Filter by maximum monster level.
                - min_level: Filter by minimum monster level.

        Returns:
            dict or list: A single monster if monster_code is provided, else a filtered list of monsters.
        """
        if not self.all_monsters:
            self._cache_monsters()
        if monster_code:
            return self.cache.get(monster_code)
        return self._filter_monsters(**filters)

class Resources:
    def __init__(self, api):
        self.api = api
        self.cache = {}
        self.all_resources = []

    def _cache_resources(self):
        if _re_cache(self.api, "resource_cache"):
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS resource_cache (
                code TEXT PRIMARY KEY,
                name TEXT,
                skill TEXT,
                level INTEGER,
                drops TEXT
            )
            """)
            cache_db.commit()

            endpoint = "resources?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_resources")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of resources", extra={"char": self.api.char.name})

            all_resources = []
            for i in range(pages):
                endpoint = f"resources?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_resources")
                resource_list = res["data"]

                for resource in resource_list:
                    code = resource["code"]
                    name = resource["name"]
                    skill = resource.get("skill")
                    level = resource["level"]
                    drops = json.dumps([Drop(**drop).__dict__ for drop in resource.get("drops", [])])  # Serialize drops as JSON

                    # Insert or replace the resource into the database
                    cache_db.execute("""
                    INSERT OR REPLACE INTO resource_cache (
                        code, name, skill, level, drops
                    ) VALUES (?, ?, ?, ?, ?)
                    """, (code, name, skill, level, drops))
                    cache_db.commit()

                    all_resources.append(resource)

                logger.debug(f"Fetched {len(resource_list)} resources from page {i+1}", extra={"char": self.api.char.name})

            self.cache = {resource["code"]: resource for resource in all_resources}
            self.all_resources = all_resources

            logger.debug(f"Finished caching {len(all_resources)} resources", extra={"char": self.api.char.name})

    def _filter_resources(self, drop=None, max_level=None, min_level=None, skill=None):
        # Base SQL query to select all resources
        query = "SELECT * FROM resource_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if drop:
            query += " AND EXISTS (SELECT 1 FROM json_each(json_extract(resource_cache.drops, '$')) WHERE json_each.value LIKE ?)"
            params.append(f"%{drop}%")

        if max_level is not None:
            query += " AND resource_cache.level <= ?"
            params.append(max_level)

        if min_level is not None:
            query += " AND resource_cache.level >= ?"
            params.append(min_level)

        if skill:
            query += " AND resource_cache.skill = ?"
            params.append(skill)

        # Execute the query
        cache_db_cursor.execute(query, params)
        rows = cache_db_cursor.fetchall()

        # Return the filtered resources
        return rows

    def get(self, resource_code=None, **filters):
        """
        Retrieves a specific resource or filters resources based on provided parameters.
        
        Args:
            resource_code (str, optional): Retrieve resource by its unique code.
            **filters: Optional filter parameters. Supported filters:
                - drop: Filter resources that drop a specific item.
                - max_level: Filter by maximum resource level.
                - min_level: Filter by minimum resource level.
                - skill: Filter by craft skill.

        Returns:
            dict or list: A single resource if resource_code is provided, else a filtered list of resources.
        """
        if not self.all_resources:
            self._cache_resources()
        if resource_code:
            return self.cache.get(resource_code)
        return self._filter_resources(**filters)

class Tasks:
    def __init__(self, api):
        self.api = api
        self.cache = {}
        self.all_tasks = []

    def _cache_tasks(self):
        if _re_cache(self.api, "task_cache"):
            # Create table if it doesn't exist
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_cache (
                code TEXT PRIMARY KEY,
                level INTEGER,
                type TEXT,
                min_quantity INTEGER,
                max_quantity INTEGER,
                skill TEXT,
                rewards TEXT
            )
            """)
            cache_db.commit()

            endpoint = "tasks/list?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_tasks")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of tasks", extra={"char": self.api.char.name})

            all_tasks = []
            for i in range(pages):
                endpoint = f"tasks/list?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_tasks")
                task_list = res["data"]

                for task in task_list:
                    code = task["code"]
                    level = task["level"]
                    task_type = task.get("type")
                    min_quantity = task["min_quantity"]
                    max_quantity = task["max_quantity"]
                    skill = task.get("skill")
                    rewards = json.dumps({
                        "items": [{"code": item["code"], "quantity": item["quantity"]} for item in task["rewards"].get("items", [])],
                        "gold": task["rewards"].get("gold", 0)
                    }) if task.get("rewards") else None

                    # Insert or replace the task into the database
                    cache_db.execute("""
                    INSERT OR REPLACE INTO task_cache (
                        code, level, type, min_quantity, max_quantity, skill, rewards
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (code, level, task_type, min_quantity, max_quantity, skill, rewards))
                    cache_db.commit()

                    all_tasks.append(task)

                logger.debug(f"Fetched {len(task_list)} tasks from page {i+1}", extra={"char": self.api.char.name})

            self.cache = {task["code"]: task for task in all_tasks}
            self.all_tasks = all_tasks

            logger.debug(f"Finished caching {len(all_tasks)} tasks", extra={"char": self.api.char.name})

    def _filter_tasks(self, skill=None, task_type=None, max_level=None, min_level=None, name=None):
        # Base SQL query to select all tasks
        query = "SELECT * FROM task_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if skill:
            query += " AND task_cache.skill = ?"
            params.append(skill)

        if task_type:
            query += " AND task_cache.type = ?"
            params.append(task_type)

        if max_level is not None:
            query += " AND task_cache.level <= ?"
            params.append(max_level)

        if min_level is not None:
            query += " AND task_cache.level >= ?"
            params.append(min_level)

        if name:
            query += " AND task_cache.code LIKE ?"
            params.append(f"%{name}%")

        # Execute the query
        cache_db_cursor.execute(query, params)
        rows = cache_db_cursor.fetchall()

        # Reconstruct tasks from the database rows
        filtered_tasks = []
        for row in rows:
            task = Task(
                code=row[0],
                level=row[1],
                type=row[2],
                min_quantity=row[3],
                max_quantity=row[4],
                skill=row[5],
                rewards=json.loads(row[6]) if row[6] else None
            )
            filtered_tasks.append(task)

        return filtered_tasks

    def get(self, task_code=None, **filters):
        """
        Retrieves a specific task or filters tasks based on provided parameters.
        
        Args:
            task_code (str, optional): Retrieve task by its unique code.
            **filters: Optional filter parameters. Supported filters:
                - skill: Filter by task skill.
                - task_type: Filter by task type.
                - max_level: Filter by maximum task level.
                - min_level: Filter by minimum task level.
                - name: Filter by task name (case-insensitive).

        Returns:
            dict or list: A single task if task_code is provided, else a filtered list of tasks.
        """
        if not self.all_tasks:
            self._cache_tasks()
        if task_code:
            return self.cache.get(task_code)
        return self._filter_tasks(**filters)

class Rewards:
    def __init__(self, api):
        self.api = api
        self.cache = {}
        self.all_rewards = []

    def _cache_rewards(self):
        if _re_cache(self.api, "reward_cache"):
            # Create table if it doesn't exist
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS reward_cache (
                code TEXT PRIMARY KEY,
                rate INTEGER,
                min_quantity INTEGER,
                max_quantity INTEGER
            )
            """)
            cache_db.commit()

            endpoint = "tasks/rewards?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_task_rewards")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of task rewards", extra={"char": self.api.char.name})

            all_rewards = []
            for i in range(pages):
                endpoint = f"tasks/rewards?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_task_rewards")
                reward_list = res["data"]

                for reward in reward_list:
                    code = reward["code"]
                    rate = reward["rate"]
                    min_quantity = reward["min_quantity"]
                    max_quantity = reward["max_quantity"]

                    # Insert or replace the reward into the database
                    cache_db.execute("""
                    INSERT OR REPLACE INTO reward_cache (
                        code, rate, min_quantity, max_quantity
                    ) VALUES (?, ?, ?, ?)
                    """, (code, rate, min_quantity, max_quantity))
                    cache_db.commit()

                    all_rewards.append(reward)

                logger.debug(f"Fetched {len(reward_list)} task rewards from page {i+1}", extra={"char": self.api.char.name})

            self.rewards_cache = {reward["code"]: reward for reward in all_rewards}
            self.all_rewards = all_rewards

            logger.debug(f"Finished caching {len(all_rewards)} task rewards", extra={"char": self.api.char.name})

    def _filter_rewards(self, name=None):
        # Base SQL query to select all rewards
        query = "SELECT * FROM reward_cache WHERE 1=1"
        params = []

        if name:
            query += " AND reward_cache.code LIKE ?"
            params.append(f"%{name}%")

        # Execute the query
        cache_db_cursor.execute(query, params)
        rows = cache_db_cursor.fetchall()

        # Reconstruct rewards from the database rows
        filtered_rewards = []
        for row in rows:
            reward = Reward(
                code=row[0],
                rate=row[1],
                min_quantity=row[2],
                max_quantity=row[3]
            )
            filtered_rewards.append(reward)

        return filtered_rewards

    def get_all_rewards(self, **filters):
        logger.debug(f"Getting all task rewards with filters: {filters}", extra={"char": self.api.char.name})
        
        if not self.all_rewards:
            logger.debug("Rewards cache is empty, calling _cache_rewards() to load rewards.", 
                        extra={"char": self.api.char.name})
            self._cache_rewards()

        return self._filter_rewards(**filters)

    def get(self, task_code=None):
        """
        Retrieves a specific reward or filters rewards based on provided parameters.
        
        Args:
            reward_code (str, optional): Retrieve reward by its unique code.

        Returns:
            dict or list: A single reward if reward_code is provided, else a filtered list of rewards.
        """
        if not self.all_rewards:
            logger.debug("Rewards cache is empty, calling _cache_rewards() to load rewards.", 
                        extra={"char": self.api.char.name})
            self._cache_rewards()

        if task_code:
            reward = self.rewards_cache.get(task_code)
            if reward:
                logger.debug(f"Found reward with code {task_code}", extra={"char": self.api.char.name})
            else:
                logger.debug(f"Reward with code {task_code} not found in cache", extra={"char": self.api.char.name})
            return reward

class Achievements:
    def __init__(self, api):
        self.api = api
        self.cache = {}
        self.all_achievements = []

    def _cache_achievements(self):
        if _re_cache(self.api, "achievement_cache"):
            # Create table if it doesn't exist
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievement_cache (
                code TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                points INTEGER,
                type TEXT,
                target INTEGER,
                total INTEGER,
                rewards_gold INTEGER
            )
            """)
            cache_db.commit()

            endpoint = "achievements?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_achievements")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of achievements", extra={"char": self.api.char.name})

            all_achievements = []
            for i in range(pages):
                endpoint = f"achievements?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_achievements")
                achievement_list = res["data"]

                for achievement in achievement_list:
                    code = achievement["code"]
                    name = achievement["name"]
                    description = achievement["description"]
                    points = achievement["points"]
                    achievement_type = achievement["type"]
                    target = achievement["target"]
                    total = achievement["total"]
                    rewards_gold = achievement["rewards"].get("gold", 0)

                    # Insert or replace the achievement into the database
                    cache_db.execute("""
                    INSERT OR REPLACE INTO achievement_cache (
                        code, name, description, points, type, target, total, rewards_gold
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (code, name, description, points, achievement_type, target, total, rewards_gold))
                    cache_db.commit()

                    all_achievements.append(achievement)

                logger.debug(f"Fetched {len(achievement_list)} achievements from page {i+1}", extra={"char": self.api.char.name})

            self.cache = {achievement["code"]: achievement for achievement in all_achievements}
            self.all_achievements = all_achievements

            logger.debug(f"Finished caching {len(all_achievements)} achievements", extra={"char": self.api.char.name})

    def _filter_achievements(self, achievement_type=None, name=None, description=None, reward_type=None,
                            reward_item=None, points_min=None, points_max=None):
        # Base SQL query to select all achievements
        query = "SELECT * FROM achievement_cache WHERE 1=1"
        params = []

        if achievement_type:
            query += " AND achievement_cache.type = ?"
            params.append(achievement_type)
        if name:
            query += " AND achievement_cache.name LIKE ?"
            params.append(f"%{name}%")
        if description:
            query += " AND achievement_cache.description LIKE ?"
            params.append(f"%{description}%")
        if reward_type:
            query += " AND EXISTS (SELECT 1 FROM reward_cache WHERE reward_cache.type = ? AND reward_cache.code IN (SELECT reward_code FROM achievement_rewards WHERE achievement_code = achievement_cache.code))"
            params.append(reward_type)
        if reward_item:
            query += " AND EXISTS (SELECT 1 FROM reward_cache WHERE reward_cache.code = ? AND reward_cache.code IN (SELECT reward_code FROM achievement_rewards WHERE achievement_code = achievement_cache.code))"
            params.append(reward_item)
        if points_min is not None:
            query += " AND achievement_cache.points >= ?"
            params.append(points_min)
        if points_max is not None:
            query += " AND achievement_cache.points <= ?"
            params.append(points_max)

        # Execute the query
        cache_db_cursor.execute(query, params)
        rows = cache_db_cursor.fetchall()

        # Reconstruct achievements from the database rows
        filtered_achievements = []
        for row in rows:
            achievement = Achievement(
                name=row[1],
                code=row[0],
                description=row[2],
                points=row[3],
                type=row[4],
                target=row[5],
                total=row[6],
                rewards=AchievementReward(gold=row[7])
            )
            filtered_achievements.append(achievement)

        return filtered_achievements

    def get(self, achievement_code=None, **filters):
        """
        Retrieves a specific achievement or filters achievements based on provided parameters.
        
        Args:
            achievement_code (str, optional): Retrieve achievement by its unique code.
            **filters: Optional filter parameters. Supported filters:
                - achievement_type: Filter by achievement type.
                - name: Filter by achievement name (case-insensitive).
                - description: Filter by achievement description (case-insensitive).
                - reward_type: Filter by reward type.
                - reward_item: Filter by reward item code.
                - points_min: Filter by minimum achievement points.
                - points_max: Filter by maximum achievement points.

        Returns:
            dict or list: A single achievement if achievement_code is provided, else a filtered list of achievements.
        """
        if not self.all_achievements:
            self._cache_achievements()
        if achievement_code:
            return self.cache.get(achievement_code)
        return self._filter_achievements(**filters)

class Effects:
    def __init__(self, api):
        self.api = api
        self.cache = {}
        self.all_effects = []

    def _cache_effects(self):
        """
        Fetches all effects from the API and caches them in a local SQLite database.
        """
        global cache_db, cache_db_cursor

        # Check if the cache needs to be refreshed
        if _re_cache(self.api, "effects_cache"):
            # Create the effects_cache table if it doesn't exist
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS effects_cache (
                code TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                attributes TEXT
            )
            """)
            cache_db.commit()

            # Fetch all effects from the API
            endpoint = "effects?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_effects")
            total_pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {total_pages} pages of effects", extra={"char": self.api.char.name})

            all_effects = []
            for i in range(total_pages):
                endpoint = f"effects?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_effects")
                effect_list = res["data"]

                for effect in effect_list:
                    code = effect["code"]
                    name = effect["name"]
                    description = effect.get("description", "")
                    attributes = json.dumps(effect.get("attributes", {}))  # Serialize attributes as JSON

                    # Insert or replace the effect into the database
                    cache_db.execute("""
                    INSERT OR REPLACE INTO effects_cache (
                        code, name, description, attributes
                    ) VALUES (?, ?, ?, ?)
                    """, (code, name, description, attributes))
                    cache_db.commit()

                    all_effects.append(effect)

                logger.debug(f"Fetched {len(effect_list)} effects from page {i+1}", extra={"char": self.api.char.name})

            self.cache = {effect["code"]: effect for effect in all_effects}
            self.all_effects = all_effects

            logger.debug(f"Finished caching {len(all_effects)} effects", extra={"char": self.api.char.name})

    def _filter_effects(self, name=None, attribute_key=None, attribute_value=None):
        """
        Filters effects based on provided criteria.

        Args:
            name (str, optional): Filter effects by name.
            attribute_key (str, optional): Filter effects that have a specific attribute key.
            attribute_value (str, optional): Filter effects where a specific attribute key has a specific value.

        Returns:
            list: A list of filtered effects.
        """
        global cache_db_cursor

        # Base SQL query to select all effects
        query = "SELECT * FROM effects_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")

        if attribute_key and attribute_value:
            query += """
            AND EXISTS (
                SELECT 1 FROM json_each(attributes)
                WHERE json_each.key = ? AND json_each.value = ?
            )
            """
            params.append(attribute_key)
            params.append(attribute_value)
        elif attribute_key:
            query += """
            AND EXISTS (
                SELECT 1 FROM json_each(attributes)
                WHERE json_each.key = ?
            )
            """
            params.append(attribute_key)

        # Execute the query
        cache_db_cursor.execute(query, params)
        rows = cache_db_cursor.fetchall()

        # Convert rows to dictionaries
        filtered_effects = []
        for row in rows:
            effect = {
                "code": row[0],
                "name": row[1],
                "description": row[2],
                "attributes": json.loads(row[3])  # Deserialize attributes from JSON
            }
            filtered_effects.append(effect)

        return filtered_effects

    def get(self, effect_code=None, **filters):
        """
        Retrieves a specific effect or filters effects based on provided parameters.

        Args:
            effect_code (str, optional): Retrieve effect by its unique code.
            **filters: Optional filter parameters. Supported filters:
                - name: Filter effects by name.
                - attribute_key: Filter effects that have a specific attribute key.
                - attribute_value: Filter effects where a specific attribute key has a specific value.

        Returns:
            dict or list: A single effect if effect_code is provided, else a filtered list of effects.
        """
        if not self.all_effects:
            self._cache_effects()
        if effect_code:
            return self.cache.get(effect_code)
        return self._filter_effects(**filters)
    
class Events:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        self.api = api
    # --- Event Functions ---
    def get_active(self, page: int = 1) -> dict:
        """
        Retrieve a list of active events.

        Args:
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with a list of active events.
        """
        query = f"size=100&page={page}"
        endpoint = f"events/active?{query}"
        return self.api._make_request("GET", endpoint, source="get_active_events").get("data")

    def get_all(self, page: int = 1) -> dict:
        """
        Retrieve a list of all events.

        Args:
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with a list of events.
        """
        query = f"size=100&page={page}"
        endpoint = f"events?{query}"
        return self.api._make_request("GET", endpoint, source="get_all_events").get("data")

class GE:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        self.api = api
    # --- Grand Exchange Functions ---
    def get_history(self, item_code: str, buyer: Optional[str] = None, seller: Optional[str] = None, page: int = 1, size: int = 100) -> dict:
        """
        Retrieve the transaction history for a specific item on the Grand Exchange.

        Args:
            item_code (str): Code of the item.
            buyer (Optional[str]): Filter history by buyer name.
            seller (Optional[str]): Filter history by seller name.
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the item transaction history.
        """
        query = f"size={size}&page={page}"
        if buyer:
            query += f"&buyer={buyer}"
        if seller:
            query += f"&seller={seller}"
        endpoint = f"grandexchange/history/{item_code}?{query}"
        return self.api._make_request("GET", endpoint, source="get_ge_history").get("data")

    def get_sell_orders(self, item_code: Optional[str] = None, seller: Optional[str] = None, page: int = 1, size: int = 100) -> dict:
        """
        Retrieve a list of sell orders on the Grand Exchange with optional filters.

        Args:
            item_code (Optional[str]): Filter by item code.
            seller (Optional[str]): Filter by seller name.
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the list of sell orders.
        """
        query = f"size={size}&page={page}"
        if item_code:
            query += f"&item_code={item_code}"
        if seller:
            query += f"&seller={seller}"
        endpoint = f"grandexchange/orders?{query}"
        return self.api._make_request("GET", endpoint, source="get_ge_sell_orders").get("data")

    def get_sell_order(self, order_id: str) -> dict:
        """
        Retrieve details for a specific sell order on the Grand Exchange.

        Args:
            order_id (str): ID of the order.

        Returns:
            dict: Response data for the specified sell order.
        """
        endpoint = f"grandexchange/orders/{order_id}"
        return self.api._make_request("GET", endpoint, source="get_ge_sell_order").get("data")
    
    # --- Grand Exchange Actions Functions ---
    def buy(self, order_id: str, quantity: int = 1) -> dict:
        """
        Buy an item from the Grand Exchange.

        Args:
            order_id (str): ID of the order to buy from.
            quantity (int): Quantity of the item to buy (default is 1).

        Returns:
            dict: Response data with transaction details.
        """
        endpoint = f"my/{self.api.char.name}/action/grandexchange/buy"
        json = {"id": order_id, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="ge_buy")
        return res

    def sell(self, item_code: str, price: int, quantity: int = 1) -> dict:
        """
        Create a sell order on the Grand Exchange.

        Args:
            item_code (str): Code of the item to sell.
            price (int): Selling price per unit.
            quantity (int): Quantity of the item to sell (default is 1).

        Returns:
            dict: Response data confirming the sell order.
        """
        endpoint = f"my/{self.api.char.name}/action/grandexchange/sell"
        json = {"code": item_code, "item_code": price, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="ge_sell")
        return res

    def cancel(self, order_id: str) -> dict:
        """
        Cancel an active sell order on the Grand Exchange.

        Args:
            order_id (str): ID of the order to cancel.

        Returns:
            dict: Response data confirming the order cancellation.
        """
        endpoint = f"my/{self.api.char.name}/action/grandexchange/cancel"
        json = {"id": order_id}
        res = self.api._make_request("POST", endpoint, json=json, source="ge_cancel_sell")
        return res
    
class Leaderboard:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        self.api = api
    # --- Leaderboard Functions ---
    def get_characters_leaderboard(self, sort: Optional[str] = None, page: int = 1) -> dict:
        """
        Retrieve the characters leaderboard with optional sorting.

        Args:
            sort (Optional[str]): Sorting criteria (e.g., 'level', 'xp').
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the characters leaderboard.
        """
        query = "size=100"
        if sort:
            query += f"&sort={sort}"
        query += f"&page={page}"
        endpoint = f"leaderboard/characters?{query}"
        return self.api._make_request("GET", endpoint, source="get_characters_leaderboard")

    def get_accounts_leaderboard(self, sort: Optional[str] = None, page: int = 1) -> dict:
        """
        Retrieve the accounts leaderboard with optional sorting.

        Args:
            sort (Optional[str]): Sorting criteria (e.g., 'points').
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the accounts leaderboard.
        """
        query = "size=100"
        if sort:
            query += f"&sort={sort}"
        query += f"&page={page}"
        endpoint = f"leaderboard/accounts?{query}"
        return self.api._make_request("GET", endpoint, source="get_accounts_leaderboard")

class Accounts:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        self.api = api
    # --- Accounts Functions ---
    def get_account_achievements(self, account: str, completed: Optional[bool] = None, achievement_type: Optional[str] = None, page: int = 1) -> dict:
        """
        Retrieve a list of achievements for a specific account with optional filters.

        Args:
            account (str): Account name.
            completed (Optional[bool]): Filter by completion status (True for completed, False for not).
            achievement_type (Optional[str]): Filter achievements by type.
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the list of achievements for the account.
        """
        query = "size=100"
        if completed is not None:
            query += f"&completed={str(completed).lower()}"
        if achievement_type:
            query += f"&achievement_type={achievement_type}"
        query += f"&page={page}"
        endpoint = f"/accounts/{account}/achievements?{query}"
        return self.api._make_request("GET", endpoint, source="get_account_achievements") 


    def get_account(self, account: str):
        endpoint = f"/acounts/{account}"
        return self.api._make_request("GET", endpoint, source="get_account")
