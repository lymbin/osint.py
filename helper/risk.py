# This file is part of osint.py program
# @lymbin 2021-2022

class RiskResolver:
    @staticmethod
    def calc_risk(severity, exploits):
        result = {'score': 100,
                  'level': 'Low'}
        if severity['low'] > 0:
            result['level'] = 'Elevated'
            result['score'] = result['score'] - severity['low']
            if exploits > 0 or result['score'] < 75:
                result['score'] = 75
        if severity['medium'] > 0:
            result['level'] = 'Medium'
            result['score'] = 75 - severity['medium']
            if exploits > 0 or result['score'] < 50:
                result['score'] = 50
        if severity['high'] > 0:
            result['level'] = 'Severe'
            result['score'] = 50 - severity['high']
            if exploits > 0 or result['score'] < 25:
                result['score'] = 25 - exploits
                if result['score'] < 10:
                    result['level'] = 'Critical'
                    result['score'] = 10
        if severity['critical'] > 0:
            result['level'] = 'Critical'
            result['score'] = 10 - severity['critical']
            if result['score'] < 0:
                result['score'] = 0
        return result

    @staticmethod
    def calc_cve_severity(cvss: float) -> str:
        if cvss >= 9.0:
            return 'critical'
        elif 7.0 <= cvss < 9.0:
            return 'high'
        elif 4.0 <= cvss < 7.0:
            return 'medium'
        elif 0.0 < cvss < 4.0:
            return 'low'
