import asyncio
import json
from logging import Logger

import aiohttp
from aiohttp import ClientResponse
import logging

from client3x.client3x import InboundPayload
from client3x.client3x.ClientPayload import CLientPayload
from client3x.client3x.PanelResponse import PanelResponse
from client3x.client3x.payload import Payload
from client3x.client3x.errors import ClientError

class AsyncClient3XUI:
    def __init__(self, login, password, login_key, panel_host, root_url, sub_host, sub_path, inbound_id, panel_port = None, sub_port = None, logging_enabled = False,timeout = 300):


        self.inbound = inbound_id

        self.login_payload = {
            "username": login,
            "password": password,
            "loginSecret": login_key
        }

        self.base_url = f'https://{panel_host}:{panel_port}/{root_url}' if panel_port else f'https://{panel_host}/{root_url}'
        self.sub_url = f'https://{sub_host}:{sub_port}/{sub_path}/' if sub_port else f'https://{sub_host}/{sub_path}/'

        self.logger: Logger | None = None

        if logging_enabled:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
            self.logger.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            self.logger.info('Client logging enabled\n')
            self.logger.info(f'Panel base url : {self.base_url}\n')
            self.logger.info(f'Panel sub url : {self.sub_url}\n')
            self.logger.info('Client initialization complete')
            self.logger.info(f'Start Fetching  cookies from server with timeout of {timeout} seconds')

        self.cookie = None
        self.timeout = timeout
        self.task = None



    def __del__(self):

        if hasattr(self, 'task') and self.task:
            self.task.cancel()
            if self.logger:
                    self.logger.info('Background task was cancelled.')

    async def start(self):
        self.task = asyncio.create_task(self.update_cookies_periodically())


    async def __fetch_cookies(self):
        """Get new cookies from server by /login POST request"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.base_url}/login', data=self.login_payload) as response:
                    if response.status == 200:
                        self.cookie = session.cookie_jar.filter_cookies(f'{self.base_url}')
                        if self.logger:
                            self.logger.info('Updated cookies. ')
                    else:
                        if self.logger:
                            self.logger.error(f'Failed to update cookies. Wrong status : {response.status}')
        except Exception as e:
            if self.logger:
                self.logger.error(f'Failed to update cookies.\nError: {repr(e)}')


    async def update_cookies_periodically(self):
        """Update cookies every  timeout seconds"""
        while True:
            await self.__fetch_cookies()
            await asyncio.sleep(self.timeout)

    async def __post_request(self, url: str, payload: Payload|None) -> ClientResponse:
        if not self.cookie:
            await self.__fetch_cookies()
        """
            Sends an asynchronous POST request to a specified URL with the given payload.

            This function handles the login process before sending the request and ensures
            the session is closed after the request is completed.


            :param url: str : The URL to which the POST request is sent.
            :param payload: Payload: The data to be sent in the body of the POST request.

            :return resp: ClientResponce : The response object from the POST request.

            :raise: ClientError: If there is an issue connecting to the panel or if the client encounters an error.
        """

        async with aiohttp.ClientSession() as session:
            try:

                resp = await session.post(url, data=payload.format(), cookies=self.cookie)
                if self.logger:
                    self.logger.info(f'POST {url} [{resp.status}]')
                return resp

            except Exception as e:
                if self.logger:
                    self.logger.error(f'Failed to send POST request.\nUrl: {url}\nPayload : {payload}\nError: {repr(e)}')
                raise ClientError('Client error: ' + repr(e), resp.status)
            finally:
                await session.close()



    async def __get_request(self, url: str) -> ClientResponse:
        """
        Sends an asynchronous GET request to a specified URL.

        This function handles the login process before sending the request and ensures
        the session is closed after the request is completed.

        Parameters:
        url (str): The URL to which the GET request is sent.

        Returns:
        aiohttp.ClientResponse: The response object from the GET request.

        Raises:
        ClientError: If there is an issue connecting to the panel or if the client encounters an error.
        """
        if not self.cookie:
            await self.__fetch_cookies()
        async with aiohttp.ClientSession() as session:
            try:
                resp = await session.get(url,cookies=self.cookie)
                if self.logger:
                    self.logger.info(f'GET {url} [{resp.status}]')
                return resp
            except Exception as e:
                raise ClientError('Client error: ' + repr(e),0)
            finally:
                await session.close()


    def __check_inbound(self, inbound_id: int | None) -> int:
        """
        Check if the given inbound_id is None and return self.inbound if it is.
        Otherwise, log a warning and return the given inbound_id.

        :param inbound_id: The inbound ID to check
        :return: The inbound ID to use
        """
        if inbound_id is None:
            return self.inbound
        else:
            if self.logger:
                self.logger.warning(f'Using weak inbound_id: {inbound_id}. Consider using the inbound id of client')
            return inbound_id


#-------------------------------------------------- Inbounds -----------------------------------------------------------
    async def get_inbounds(self) -> PanelResponse:
        """
        Get the list of inbounds.
        """

        url = f'{self.base_url}/panel/api/inbounds/list'

        data = await self.__get_request(url)

        return PanelResponse(await data.json())

    async def online_clients(self)  -> PanelResponse:
        """
        Returns a list of clients that are currently online.
        """

        url = f'{self.base_url}/panel/api/inbounds/onlines'

        data = await self.__post_request(url, payload=None)

        return PanelResponse(await data.json())


    async def reset_all_traffics(self):
        """
        Resets all client's traffic data.
        """

        url = f'{self.base_url}/panel/api/inbounds/resetAllTraffics'
        await self.__post_request(url, payload=None)
        if self.logger:
            self.logger.info('All clients traffic data reset')

    async def create_backup(self):
        """
        Creates a backup of the panel
        Make a get request to a panel, that triggers the creation of a system backup and initiates
        the delivery of the backup file to designated administrators via a configured Telegram bot.
        """

        url = f'{self.base_url}/panel/api/inbounds/createbackup'
        await self.__get_request(url)
        if self.logger:
            self.logger.info('Panel backup created')

#-------------------------------------------------- Inbounds -----------------------------------------------------------

#------------------------------------------------ Inbound --------------------------------------------------------------


    async def add_inbound(self, inbound_paload: InboundPayload) -> PanelResponse:
        """
        Add a new Inbound to the panel.
        :param inbound_paload:
        :return: PanelResponse
        """

        url = f'{self.base_url}/panel/api/inbounds/add'

        response = await self.__post_request(url, payload=inbound_paload)

        return PanelResponse(await response.json())


    async def get_inbound(self, inbound_id: int) -> PanelResponse:
        """
        Gets an inbound.

        :param inbound_id: Optional(int) : The ID of the inbound to get.
        :return: PanelResponse : The inbound data.
        """
        inbound_id = self.__check_inbound(inbound_id)

        url = f'{self.base_url}/panel/api/inbounds/get/{inbound_id}'

        response = await self.__get_request(url)

        return PanelResponse(await response.json())

    async def update_inbound(self, inbound_payload: InboundPayload, inbound_id = None) -> PanelResponse:
        """
        Updates an inbound params.

        :param inbound_payload: InboundPayload : The payload of the inbound to update.
        :param inbound_id: Optional(int) : The ID of the inbound to update.
        :return: PanelResponse
        """

        inbound_id = self.__check_inbound(inbound_id)

        url = f'{self.base_url}/panel/api/inbounds/update/{inbound_id}'

        response = await self.__post_request(url, payload=inbound_payload)

        return PanelResponse(await response.json())

    async def delete_inbound(self, inbound_id=None) -> None:
        """
        Deletes an inbound.

        :param inbound_id: Optional(int) : The ID of the inbound to delete.
        """
        inbound_id = self.__check_inbound(inbound_id)

        url = f'{self.base_url}/panel/api/inbounds/del/{inbound_id}'

        await self.__post_request(url, payload=None)


    async def reset_all_clients_in_inbound(self, inbound_id=None) -> None:
        """
        Resets all clients in the specified inbound.

        :param inbound_id: Optional(int) :  Inbound id, if None then uses self.inbound
        """
        inbound_id = self.__check_inbound(inbound_id)
        url = f'{self.base_url}/panel/api/inbounds/resetAllClientTraffics/{inbound_id}'
        await self.__post_request(url, payload=None)


    async def delete_depleted_clients(self, inbound_id=None) -> None:
        """
        Deleting clients whose key has expired
        (it can be used to clean keys when, for example, 60 days are not extended)
        """
        inbound_id = self.__check_inbound(inbound_id)

        post_request_url = f'{self.base_url}/panel/api/inbounds/delDepletedClients/{inbound_id}'

        await self.__post_request(post_request_url, None)


    async def get_clients_in_inbound(self, inbound_id=None) -> list:
        """
        Getting all clients on inbound in list
        :param inbound_id: Optional(int) : inbound id, if None then uses self.inbound
        :return: clients:  List of clients
        """

        inbound_id = self.__check_inbound(inbound_id)

        get_request_url = f'{self.base_url}/panel/api/inbounds/get/{inbound_id}'

        resp = await self.__get_request(get_request_url)
        data = await resp.text()

        if resp.ok:
            data = json.loads(data)
            data = json.loads(data['obj']['settings'])
            clients = data['clients']
            return clients  # возвращает список клиентов

#------------------------------------------------ Inbound --------------------------------------------------------------



#------------------------------------------------ Client ---------------------------------------------------------------

    async def get_client_traffic(self, email: str) -> PanelResponse:
        """
        Retrieves client traffic data

        :param email: str : the unique email of the client.
        :return traffic: PanelResponse : A dictionary containing the client traffic data.
        """

        url = f'{self.base_url}/panel/api/inbounds/getClientTraffics/{email}'

        data = await self.__get_request(url)

        return PanelResponse(await data.json())


    async def  get_client_traffic_by_id(self, client_id :str) -> PanelResponse:
        """
        Retrieves client traffic data by client id.
        :param client_id: str : the unique client id.
        :return traffic: PanelResponse : A dictionary containing the client traffic data.
        """

        url = f'{self.base_url}/panel/api/inbounds/getClientTrafficsById/{client_id}'

        data = await self.__get_request(url)

        return PanelResponse(await data.json())


    async def add_client(self, payload: CLientPayload) -> str:
        """
        Adds a client to the specified inbound.

        :param payload: CLientPayload : The payload containing the client's details.
        :return sublink: str : A sublink
        """


        post_request_url = f"{self.base_url}/panel/api/inbounds/addClient"

        resp = await self.__post_request(post_request_url, payload)

        if resp.ok:
            sublink = self.sub_url + payload.data["settings"]["clients"][0]["subId"]
            return sublink
        else:
            raise ClientError("Couldn't connect to panel", resp.status)


    async def update_client(self, client_id: str, payload: CLientPayload) -> str:
        """
        Update client info in inbound

        :param client_id: str : Client id
        :param payload: DefaultPayload : New client info

        :return: sublink: str :   Link to the subscription
        """
        post_request_url = f'{self.base_url}/panel/api/inbounds/updateClient/{client_id}'
        resp = await self.__post_request(post_request_url, payload)

        if resp.ok:
            sublink = self.sub_url + payload.data["settings"]["clients"][0]["subId"]
            return sublink
        else:
            raise ClientError("Couldn't connect to panel", resp.status)


    async def delete_client(self, client_id: str, inbound_id=None) -> None:
        """
        Deleting a client by its client_id
        :param inbound_id:int : inbound id, if None then uses self.inbound
        :param client_id:str :  Client id
        """

        inbound_id = self.__check_inbound(inbound_id)

        post_request_url = f"{self.base_url}/panel/api/inbounds/{inbound_id}/delClient/{client_id}"

        await self.__post_request(post_request_url, None)


    async def client_ipaddress(self, email: str) -> PanelResponse:
        """
        Retrieves client's IP address.
        :param email: str : The unique email of the client.
        :return ip: PanelResponse : The client's IP address.
        """

        url = f'{self.base_url}/panel/api/inbounds/clientIps/{email}'

        data = await self.__post_request(url,payload=None)
        return PanelResponse(await data.json())


    async def clear_client_ipadresses(self, email : str):
        """
        Clears client's IP address.
        :param email: str : The unique email of the client.
        """

        url = f'{self.base_url}/panel/api/inbounds/clearClientIps/{email}'
        await self.__post_request(url, payload=None)


    async def reset_client_traffic(self,email: str, inbound_id = None) -> None:
        """
        Resets client's traffic data.

        :param email: str : The unique email of the client.
        :param inbound_id: Optional(int) :  Inbound id, if None then uses self.inbound
        """
        inbound_id = self.__check_inbound(inbound_id)
        url = f'{self.base_url}/panel/api/inbounds/{inbound_id}/resetClientTraffic/{email}'
        await self.__post_request(url, payload=None)

# ------------------------------------------------ Client ---------------------------------------------------------------

