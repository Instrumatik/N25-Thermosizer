; Instalador de Windows de ThermoWell Sizer (Inno Setup 6).
;   iscc /DAppVersion=1.0.0 packaging\installer.iss
; Toma la carpeta generada por PyInstaller en dist\ThermoWellSizer.

#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppId={{6C0E3D4B-2F1A-4E8B-9C57-7A1D2B3E4F50}
AppName=ThermoWell Sizer
AppVersion={#AppVersion}
AppPublisher=InstruMatik
DefaultDirName={autopf}\InstruMatik\ThermoWell Sizer
DefaultGroupName=ThermoWell Sizer
OutputDir=..\dist
OutputBaseFilename=ThermoWellSizer-{#AppVersion}-setup
SetupIconFile=thermowell_sizer.ico
UninstallDisplayIcon={app}\ThermoWellSizer.exe
LicenseFile=..\LICENSE.txt
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequiredOverridesAllowed=dialog
ChangesAssociations=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "assoc"; Description: "Asociar archivos .tws con ThermoWell Sizer"; GroupDescription: "Archivos:"

[Files]
Source: "..\dist\ThermoWellSizer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\examples\*.tws"; DestDir: "{app}\ejemplos"; Flags: ignoreversion
Source: "..\docs\manual-usuario.md"; DestDir: "{app}\docs"; Flags: ignoreversion

[Icons]
Name: "{group}\ThermoWell Sizer"; Filename: "{app}\ThermoWellSizer.exe"
Name: "{group}\Ejemplos"; Filename: "{app}\ejemplos"
Name: "{group}\{cm:UninstallProgram,ThermoWell Sizer}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\ThermoWell Sizer"; Filename: "{app}\ThermoWellSizer.exe"; Tasks: desktopicon

[Registry]
Root: HKA; Subkey: "Software\Classes\.tws"; ValueType: string; ValueName: ""; ValueData: "ThermoWellSizer.Project"; Flags: uninsdeletevalue; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\ThermoWellSizer.Project"; ValueType: string; ValueName: ""; ValueData: "Proyecto de ThermoWell Sizer"; Flags: uninsdeletekey; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\ThermoWellSizer.Project\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\ThermoWellSizer.exe,0"; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\ThermoWellSizer.Project\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\ThermoWellSizer.exe"" ""%1"""; Tasks: assoc

[Run]
Filename: "{app}\ThermoWellSizer.exe"; Description: "{cm:LaunchProgram,ThermoWell Sizer}"; Flags: nowait postinstall skipifsilent
