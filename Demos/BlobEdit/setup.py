import sys
print sys.path

from distutils.core import setup
import py2app

setup(
    app=['blobedit.py'],
    data_files=[
    	'Resources/blob.tiff',
    	'Resources/blob_file.icns',
    	'Resources/blob_app.icns'
    ],
    options = dict(
    	py2app = dict(
    		#includes = ['objc', 'Foundation', 'AppKit'],
    		#packages = ['GUI'],
    		plist = dict(
    			#CFBundleSignature = "BLBE", # If you are using mac_creator
    			CFBundleIconFile = "blob_app",
    			CFBundleDocumentTypes = [
    				dict(CFBundleTypeName = "BlobEdit Document",
    					CFBundleTypeRole = "Editor",
    					#CFBundleTypeOSTypes = ["BLOB"], # If you are using mac_type
    					CFBundleTypeExtensions = ["blob"],
    					CFBundleTypeIconFile = "blob_file",
    					)]
    			),
    	),
    )
)
