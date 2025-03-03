# mq_service.py
file_name = "mq.py"
import json
import logging
import time

import posix_ipc

from vnet.topology import ConnectionsService, NetGroupService, VNet

from .vnet_controller import VNetController

# POSIX 消息队列
MQ_REQUEST = "/vnet_mq_request"
MQ_RESPONSE = "/vnet_mq_response"


def setup_logging():
    logging.basicConfig(
        level=logging.CRITICAL,
        format="%(levelname)s %(message)s",
        handlers=[logging.StreamHandler()],
    )


def mq_service():
    setup_logging()
    logging.info("Starting VNet Message Queue Service")

    # 创建消息队列
    mq_req = posix_ipc.MessageQueue(MQ_REQUEST, posix_ipc.O_CREAT)
    mq_res = posix_ipc.MessageQueue(MQ_RESPONSE, posix_ipc.O_CREAT)

    vnet = VNet()
    vnet.netgrp_service = NetGroupService()
    vnet.conns_service = ConnectionsService()

    vnet_controller = VNetController(vnet)

    try:
        while True:
            try:
                # 等待C程序发送请求
                request, _ = mq_req.receive()
                request_data = json.loads(request.decode())

                # 处理请求并获取响应
                response = vnet_controller.process_request(request_data)

                # 发送响应回C程序
                mq_res.send(response.to_json().encode())

            except posix_ipc.BusyError:
                logging.warning("Message queue is busy, retrying...")
                time.sleep(1)
            except OSError as e:
                logging.error(f"OSError: {e}, retrying...")
                time.sleep(1)
            except json.JSONDecodeError:
                logging.error("Received invalid JSON data")
            except Exception as e:
                logging.exception(f"Unexpected error: {e}")

    except KeyboardInterrupt:
        logging.info("Shutting down VNet Message Queue Service")
    finally:
        # 清理资源
        mq_req.close()
        mq_res.close()
        mq_req.unlink()
        mq_res.unlink()


if __name__ == "__main__":
    mq_service()
