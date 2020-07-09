from flask import Request

from src.app.manager import AppManager


def create_app_manager(incoming_request: Request) -> AppManager:
    return AppManager(requester_ip=incoming_request.remote_addr)
