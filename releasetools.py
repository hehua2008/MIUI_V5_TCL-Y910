import common
import copy
import edify_generator
import time

def RemoveDeviceAssert(info):
    edify = info.script
    edify.AppendExtra('unmount("/custpack");\nui_print("Complete ! by hehua2008...");')
    for i in xrange(len(edify.script)):
        if "ro.product" in edify.script[i]:
          edify.script[i] = '''ui_print("****************************");
ui_print("*         TCL S950         *");
ui_print("*         Baidu OS         *");
ui_print("*        ''' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '''        *");
ui_print("*        by hehua2008      *");
ui_print("****************************");'''
    return

def AddArgsForFormatSystem(info):
    edify = info.script
    for i in xrange(len(edify.script)):
      if "format(" in edify.script[i] and "mmcblk0p7" in edify.script[i]:
        edify.script[i] = '''format("ext4", "EMMC", "/dev/block/mmcblk0p7", "0", "/system");
ui_print("Formatting custpack...");
unmount("/custpack");
format("ext4", "EMMC", "/dev/block/mmcblk0p5", "0", "/custpack");'''
      if "mount(" in edify.script[i] and "mmcblk0p7" in edify.script[i]:
        edify.script[i] += '\nmount("ext4", "EMMC", "/dev/block/mmcblk0p5", "/custpack");'
      if "package_extract_dir(" in edify.script[i] and '"system"' in edify.script[i]:
        edify.script[i] += '''\nui_print("Installing custpack files...");
package_extract_dir("custpack", "/custpack");
set_perm_recursive(0, 0, 0755, 0644, "/custpack");'''
    return

def WriteRecoveryImage(info):
    edify = info.script
    for i in xrange(len(edify.script)):
      if "write_raw_image(" in edify.script[i]:
        edify.script[i] = 'package_extract_file("recovery.img", "/dev/recovery");'
    return

AddorMove_files = {
'CUSTPACK/JRD_custres/media/shutanimation.zip' : 'custpack'
}

def AddorMoveFiles(info):
    for k, v in AddorMove_files.iteritems():
      try:
        common.ZipWriteStr(info.output_zip, v + k[len(v):], info.input_zip.read(k))
        print "^$^ Compressing " + v + k[len(v):]
      except KeyError:
        print "^$^ Warning: No " + v + k[len(v):] + " in target_files, skipping"
    return

custpack_files = {
'CUSTPACK/JRD_custres/media/shutanimation.zip'
}

def CopyCustpackFiles(info):
#    for info1 in custpack_files:
    for info1 in info.input_zip.infolist():
      if info1.filename.startswith("CUSTPACK/"):
        basefilename = info1.filename[9:]
        info2 = copy.copy(info1)
        fn = info2.filename = "custpack/" + basefilename
        if info.output_zip is not None:
          data = info.input_zip.read(info1.filename)
          info.output_zip.writestr(info2, data)
        print "^$^ Copying custpack files: " + fn
    return

def RemoveRecoveryImage(info):
    edify = info.script
    for i in xrange(len(edify.script)):
#      if "install-recovery.sh" in edify.script[i] or ("package_extract_dir(" in edify.script[i] and "recovery" in edify.script[i]):
      if "recovery" in edify.script[i] and not "recovery.img" in edify.script[i]:
        edify.script[i] = 'ui_print("Remove update recovery script written by Baidu");'
    return

def FullOTA_InstallEnd(info):
    RemoveDeviceAssert(info)
    RemoveRecoveryImage(info)
    AddArgsForFormatSystem(info)
    CopyCustpackFiles(info)
#    AddorMoveFiles(info)
#    WriteRecoveryImage(info)

def IncrementalOTA_InstallEnd(info):
    RemoveDeviceAssert(info)
    RemoveRecoveryImage(info)
    AddArgsForFormatSystem(info)
#    AddorMoveFiles(info)
#    WriteRecoveryImage(info)

