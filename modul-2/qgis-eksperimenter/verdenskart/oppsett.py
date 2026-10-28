# Forenkler QGIS-grensesnittet for undervisning.
# Kjøres av start-oppstarterne (--code) og av makroen i verdenskart.qgz.
# Skriptet er trygt å kjøre flere ganger, og en feil stopper aldri QGIS.
# Sett MODE = 'undo' (gjøres av makroen ved lukking) for å vise alt igjen.

# ---- Innstillinger: endre listene under for å tilpasse ----
SKJUL_VERKTOYLINJER = {
    'mDigitizeToolBar', 'mAdvancedDigitizeToolBar', 'mShapeDigitizeToolBar',
    'mSnappingToolBar', 'mPluginToolBar', 'mDatabaseToolBar', 'mWebToolBar',
    'mVectorToolBar', 'mRasterToolBar', 'mHelpToolBar', 'mLabelToolBar',
    'mAnnotationsToolBar', 'mMeshToolBar',
}
SKJUL_MENYER = {  # sammenlignes med menynavn uten &, med små bokstaver
    'prosessering', 'processing', 'vektor', 'vector', 'raster', 'database',
    'mesh', 'nett', 'web', 'programtillegg', 'plugins', 'plugin',
}
BEHOLD_PANEL = {'layers'}  # objectName på paneler som skal bli stående
# ------------------------------------------------------------

import sys, types

def _tilstand():
    m = sys.modules.get('verdenskart_tilstand')
    if m is None:
        m = types.ModuleType('verdenskart_tilstand')
        m.skjult = []
        sys.modules['verdenskart_tilstand'] = m
    return m

def _skjul(widget_eller_action, tilstand):
    try:
        if widget_eller_action.isVisible():
            widget_eller_action.setVisible(False)
            tilstand.skjult.append(widget_eller_action)
    except Exception:
        pass

def _bruk():
    from qgis.utils import iface
    from qgis.PyQt.QtWidgets import QToolBar, QMenu, QDockWidget
    t = _tilstand()
    if t.skjult:
        return  # allerede brukt
    win = iface.mainWindow()
    for tb in win.findChildren(QToolBar):
        if tb.objectName() in SKJUL_VERKTOYLINJER:
            _skjul(tb, t)
    for menu in win.findChildren(QMenu):
        navn = menu.title().replace('&', '').strip().lower()
        if navn in SKJUL_MENYER and menu.menuAction() is not None:
            _skjul(menu.menuAction(), t)
    docks = win.findChildren(QDockWidget)
    if any(d.objectName().lower() in BEHOLD_PANEL for d in docks):
        for d in docks:
            if d.objectName().lower() in BEHOLD_PANEL:
                d.show()
            else:
                _skjul(d, t)
    win.showMaximized()

def _angre():
    t = _tilstand()
    for w in t.skjult:
        try:
            w.setVisible(True)
        except Exception:
            pass
    t.skjult = []

try:
    if globals().get('MODE') == 'undo':
        _angre()
    else:
        _bruk()
except Exception as e:  # aldri la oppsettet hindre QGIS i å starte
    print('oppsett.py: ' + str(e))
