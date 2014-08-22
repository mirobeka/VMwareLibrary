# -*- mode: python -*-
import os

a = Analysis([os.path.join('.','VMwareLibrary','__main__.py')], hiddenimports=[], hookspath=None, runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='robotvmlib',
          debug=False,
          strip=None,
          upx=False,
          console=True )
