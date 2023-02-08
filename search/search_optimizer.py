# This file is part of osint.py program
# @lymbin 2021-2023

cpe_naming = {
    "iis": "internet_information_services",
    "apache http server": "apache:http_server",
    "apache": "apache:http_server",
    "microsoft sharepoint": "microsoft:sharepoint_enterprise_server",
    "microsoft asp.net": "microsoft:.net_framework",
    "outlook web app": "microsoft:exchange_server",
    "synology diskStation": "synology:diskstation_manager"
}


class SearchOptimizer:
    @staticmethod
    def optimize(package: str) -> str:
        package = SearchOptimizer.normalize(package)
        package = SearchOptimizer.rename(package)
        package = package.replace(" ", "_")
        return package

    @staticmethod
    def rename(package: str) -> str:
        if package in cpe_naming:
            package = cpe_naming[package]
        return package

    @staticmethod
    def normalize(package: str) -> str:
        return package.lower()
