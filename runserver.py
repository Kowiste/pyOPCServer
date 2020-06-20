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
    args = vars(parser.parse_args()) 
    opc= server()
    await opc.NewOPCServer(args)
    await opc.CreateXML()
    await opc.Start()



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

