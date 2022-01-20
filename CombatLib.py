import json
from pyautogui import alert


def damage(dmgrank: int, rescheck: int, filename: str):
    if rescheck < dmgrank:
        deg = ((dmgrank - rescheck - 1) // 5) + 1

        file = open(f'Sheets/{filename}.json', 'r')
        data = json.load(file)
        file.close()

        condits = data['conditions']

        if 'Dying' in condits['conds']:
            condits['conds'].append('DEAD')
            alert(f'{filename} is dead.')

        elif 'Incapacitated' in condits['conds']:
            condits['conds'].append('Dying')
            alert(f'{filename} is now Dying.')

        elif deg == 1:
            condits['resMod'] -= 1
            alert(f'{filename} now has -1 to resistance checks.')

        elif deg == 2:
            condits['resMod'] -= 1
            if 'Dazed(DMG)' not in condits['conds']:
                condits['conds'].append('Dazed(DMG)')
                alert(f'{filename} is now Dazed until their next turn and has -1 to resistance checks.')
            else:
                alert(f'{filename} now has -1 to resistance checks.')

        elif deg == 3:
            condits['resMod'] -= 1
            if 'Staggered(DMG)' not in condits['conds']:
                condits['conds'].append('Staggered(DMG)')
                alert(f'{filename} is now Staggered and has -1 to resistance checks.')
            else:
                condits['conds'].append('Incapacitated')
                alert(f'{filename} is now Incapacitated and has -1 to resistance checks.')
        else:
            condits['conds'].append('Incapacitated')
            alert(f'{filename} is now Incapacitated.')

        file = open(f'Sheets/{filename}.json', 'w')
        json.dump(data, file, indent=2)
        file.close()
        del file


def heal(healcheck: int, filename: str):
    if healcheck >= 10:
        deg = (healcheck - 10) // 5 + 1

        file = open(f'Sheets/{filename}.json', 'r')
        data = json.load(file)
        file.close()
        condits = data['conditions']

        while deg > 0:
            if 'DEAD' in condits['conds']:
                alert(f'{filename} is dead and cannot be healed.')
                break
            elif 'Dying' in condits['conds']:
                condits['conds'].remove('Dying')
                deg -= 1
            elif 'Incapacitated' in condits['conds']:
                condits['conds'].remove('Incapacitated')
                deg -= 1
            elif 'Staggered(DMG)' in condits['conds']:
                condits['conds'].remove('Staggered(DMG)')
                deg -= 1
            elif 'Dazed(DMG)' in condits['conds']:
                condits['conds'].remove('Dazed(DMG)')
                deg -= 1
            elif condits['resMod'] == 0:
                break
            else:
                condits['resMod'] += 1
                deg -= 1

        file = open(f'Sheets/{filename}.json', 'w')
        json.dump(data, file, indent=2)
        file.close()
        del file