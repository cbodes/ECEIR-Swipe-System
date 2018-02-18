# -*- mode: python -*-

block_cipher = None


a = Analysis(['SwipeMain.py'],
             pathex=['C:\\Users\\cam\\PycharmProjects\\untitled\\venv2\\Lib\\site-packages', 'C:\\Users\\cam\\PycharmProjects\\untitled'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SwipeMain',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
