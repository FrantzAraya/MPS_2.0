# -*- mode: python -*-
block_cipher = None

a = Analysis(['client/main.py'],
             hiddenimports=['pystan', 'prophet'],
             datas=[('assets', 'assets')])
p = PYZ(a.pure)
exe = EXE(p, a.scripts, a.binaries, a.zipfiles, a.datas,
          name='CafeDeAltura_MPS',
          debug=False,
          strip=False,
          upx=True,
          console=False)
