# This file is part of osint.py program
# @lymbin 2021-2022

class RiskResolver:
    @staticmethod
    def calc_risk(severity, exploits):
        result = {'score': 100,
                  'level': 'Low'}
        if severity['Low'] > 0:
            result['level'] = 'Elevated'
            result['score'] = result['score'] - severity['Low']
            if exploits > 0 or result['score'] < 75:
                result['score'] = 75
        if severity['Medium'] > 0:
            result['level'] = 'Medium'
            result['score'] = 75 - severity['Medium']
            if exploits > 0 or result['score'] < 50:
                result['score'] = 50
        if severity['High'] > 0:
            result['level'] = 'Severe'
            result['score'] = 50 - severity['High']
            if exploits > 0 or result['score'] < 25:
                result['score'] = 25 - exploits
                if result['score'] < 10:
                    result['level'] = 'Critical'
                    result['score'] = 10
        if severity['Critical'] > 0:
            result['level'] = 'Critical'
            result['score'] = 10 - severity['Critical']
            if result['score'] < 0:
                result['score'] = 0
        return result

    @staticmethod
    def calc_cve_severity(cvss):
        if cvss >= 9.0:
            return 'Critical'
        elif 7.0 <= cvss < 9.0:
            return 'High'
        elif 4.0 <= cvss < 7.0:
            return 'Medium'
        elif 0.0 < cvss < 4.0:
            return 'Low'
