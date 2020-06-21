import asyncio
import logging
import sys 
import argparse
from opc.server import server

sys.path.insert(0, "..")
 


#modify to method the variable

async def main():

    # getting arguments
    parser = argparse.ArgumentParser(description='OPC Server')
    parser.add_argument('-i', '--IP',help='EndPoint of the server to deploy')
    parser.add_argument('-c', '--conf',help='Configuration of the server to deploy', required=True)
    args = vars(parser.parse_args()) 
    opc= server()
    IP=args['IP']
    if IP == "":
        IP="0.0.0.0"
        logging.warning("IP not set the server will be deploy in 0.0.0.0")
    await opc.NewOPCServer(IP)
    if not await opc.LoadConfig(args['conf'].strip()):
        logging.error("Cannot load the configuration file")
        return
    await opc.CreateXML()
    await opc.Start()
    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

