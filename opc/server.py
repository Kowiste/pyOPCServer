from asyncua import ua, uamethod, Server
import asyncio
import logging
from math import sin
import time
import json

class server:
    
    def __init__(self):
        logging.info("Creating a opc server")
        self._server = Server()
        self._config = False
        self.nsindex = ""
 
    async def NewOPCServer(self,IP):
        # now setup our server
        await self._server.init()
        self._server.disable_clock()  #for debuging
        self.IP = IP.strip()

        self.mynodes = []
        self._server.set_endpoint(self.IP) #ip removing whitespace Address to pass "opc.tcp://0.0.0.0:4840/freeopcua/server/"
        self._server.set_server_name("OPC Server Name")

        # set all possible endpoint policies for clients to connect through
        self._server.set_security_policy([
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign])


    def checkdata(self,data):
        if len(data) < 5:
            return False
        if len(data['measure']) < 1:
            return False
        #TODO implement more data check
            
    async def LoadConfig(self,path):

        with open(path) as f:
            data = json.load(f)
        if not self.checkdata(data):
            return False
        # setup our own namespace
        await self._server.register_namespace(self.nsindex)
        self._config = False
        self.scan=data['scaninterval']
        self.nsindex = data['namespaceindex']
        self.namespace = data['namespace']
        self.devices = data['device']

        #   create a new node type we can instantiate in our address space
        dev = await self._server.nodes.base_object_type.add_object_type(int(self.nsindex), self.devices)

        #Creating the nodes
        
        i=0
        for element in data['measure']: 
            self.mynodes.append(await dev.add_variable(ua.NodeId.from_string('ns='+ self.nsindex + ';s='+ self.namespace +'.'+ self.devices + '.' + element['name']),element['name'],0))
            await self.mynodes[i].set_writable()
            i+=1

        myevgen = await self._server.get_event_generator()
        myevgen.event.Severity = 300
        logging.info("Configuration loaded")
        self._config = True

    async def Start(self):
        if self._config:
            async with self._server:
                #print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
                logging.info("Server Started")
                while True:
                    await asyncio.sleep(self.scan)
                    for element in self.mynodes: 
                        #updating values
                        await self._server.write_attribute_value(element.nodeid, ua.DataValue(sin(time.time()))) 
        logging.warning("The server need to be configure it first")

    async def CreateXML(self):
        ipremove  = self.IP.replace("opc.tcp://", "")    
        port= ipremove[ipremove.index(":") + 1:]
        #creating the xml
        await self._server.export_xml_by_ns("gen/Configuration" + port +".xml",int(self.nsindex))
        logging.info("XML File created successfully")


