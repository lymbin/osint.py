# This file is part of osint.py program
# @lymbin 2021-2023

class SearchOptimizer:
    @staticmethod
    def optimize(cpe: str):
        cpe.replace(" ", "_")
        return cpe

