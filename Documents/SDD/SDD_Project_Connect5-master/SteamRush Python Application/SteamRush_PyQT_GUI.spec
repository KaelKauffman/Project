# -*- mode: python -*-

block_cipher = None


a = Analysis(['SteamRush_PyQT_GUI.py'],
             pathex=['C:\\Users\\kauffk\\Documents\\GitHub\\SDD_Project_Connect5\\Documents\\SDD\\SDD_Project_Connect5-master\\SteamRush Python Application'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='SteamRush_PyQT_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SteamRush_PyQT_GUI')
