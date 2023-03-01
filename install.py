import launch

if not launch.is_installed("pysmb"):
    launch.run_pip("install pysmb==1.2.9.1", "requirements for SMB Connection")

if not launch.is_installed("pydrive2"):
    launch.run_pip("install pydrive2==1.8.1", "requirements for Google Drive Connection")

if not launch.is_installed("paramiko"):
    launch.run_pip("install paramiko==3.0.0", "requirements for SFTP Connection")
