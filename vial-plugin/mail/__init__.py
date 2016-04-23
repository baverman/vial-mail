import vial


def init():
    vial.register_function('VialMailOmni(findstart, base)', '.plugin.omnifunc')
    vial.register_command('VialMailUpdate', '.plugin.update')
