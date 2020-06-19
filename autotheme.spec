# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['autotheme.py'],
             pathex=['D:\\Dropbox\\aaa Proyectos\\Python\\autotheme'],
             binaries=[],
             datas=[
		# the icons in the options window
		('icons\\32\\B32moon.png', 'icons\\32'),
		('icons\\32\\B32sun.png', 'icons\\32'),
		# App color icon
		('icons\\16.ico', 'icons'),
		('icons\\32.ico', 'icons'),
		('icons\\32.png', 'icons'),
		# the images in the About box
		('icons\\btn\\GitHub-Mark-24px.png', 'icons\\btn'),
		('icons\\btn\\PP_logo.png', 'icons\\btn'),
		# documentation and license
		('About.md', '.'),
		('license.txt', '.'),
		('readme.md', '.'),
		# the icons used in the system tray
	     	('icons\\16\\B16moon.ico', 'icons\\16'),
	     	('icons\\16\\B16sun.ico', 'icons\\16'),
	     	('icons\\16\\W16moon.ico', 'icons\\16'),
	     	('icons\\16\\W16sun.ico', 'icons\\16')
	     ],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='autotheme',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
	  icon='icons\\16.ico' )
