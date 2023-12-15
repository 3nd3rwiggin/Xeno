import time
import asyncio
import websockets
import pymysql.cursors

CLIENT_INTERFACE = set()
CLIENT_NODE = set()

async def dbconnection():
    
    con = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='data',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with con.cursor() as cur:
            cur.execute('SELECT * FROM state')
            rows = cur.fetchall()

    finally:
        con.close()
        return rows

async def dbinsert(name, state):
    
    con = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='data',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with con.cursor() as cur:
            timestamp = time.time()
            sql = "INSERT INTO state (name, timestamp, state) VALUES (%s, %s, %s)"
            values = (name, timestamp, state)

            cur.execute(sql, values)
            con.commit()
            
            

    finally:
        con.close()
        return timestamp



async def handle_connection(websocket, path):
    if path == "/interface":
        CLIENT_INTERFACE.add(websocket)
        await interface_handler(websocket)
        print("Interface Client has connected.")
        
        
    if path == "/node":
        CLIENT_NODE.add(websocket)
        await node_handler(websocket)
        print("Node Client has connected.")
    
    
    
async def node_handler(websocket):
    try:
        async for message in websocket:
            if 'mcuinsert' in message:
                msg = message.split(',')
                timestamp = await dbinsert(msg[1], msg[2])
                message = {"name": msg[1], "timestamp": timestamp, "state": msg[2], "type": "details"}
                
                for clientInterface in set(CLIENT_INTERFACE):
                    if clientInterface != websocket and clientInterface.open:
                        await clientInterface.send(str(message))
                

    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed by node")

    
    
async def interface_handler(websocket):
    try:
        async for message in websocket:
           
            
                
            if 'interfaceDetail' in message:
                res = await dbconnection()
                for row in res:
                    data = {
                        "id": row['id'],
                        "name": row['name'],
                        "timestamp": row['timestamp'],
                        "state": row['state'],
                        "type": "details"
                    }
                
                    await websocket.send(f"{data}")
                
            if 'command' in message:
                msg = message.split(',')
                
                for clientNode in CLIENT_NODE:
                    if clientNode != websocket:
                        await clientNode.send(str(msg[1]))
            

            

    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed by interfacec")

async def main():
    
    server = await websockets.serve(
        handle_connection,
        "localhost",
        8763
    )
    print("WebSocket server started on ws://localhost:8763")

    
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
