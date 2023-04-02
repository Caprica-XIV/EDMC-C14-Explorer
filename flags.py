# Flags: 
# Bit Value Hex Meaning 
# 0     1           0000 0001 Docked, (on a landing pad) 
# 1     2           0000 0002 Landed, (on planet surface) 
# 2     4           0000 0004 LandingGearDown 
# 3     8           0000 0008 ShieldsUp 
# 4     16          0000 0010 Supercruise 
# 5     32          0000 0020 FlightAssist Off 
# 6     64          0000 0040 Hardpoints Deployed 
# 7     128         0000 0080 InWing 
# 8     256         0000 0100 LightsOn 
# 9     512         0000 0200 CargoScoopDeployed 
# 10    1024        0000 0400 SilentRunning, 
# 11    2048        0000 0800 ScoopingFuel 
# 12    4096        0000 1000 SrvHandbrake 
# 13    8192        0000 2000 SrvusingTurretview 
# 14    16384       0000 4000 SrvTurretretracted (close to ship) 
# 15    32768       0000 8000 SrvDriveAssist 
# 16    65536       0001 0000 FsdMassLocked 
# 17    131072      0002 0000 FsdCharging 
# 18    262144      0004 0000 FsdCooldown 
# 19    524288      0008 0000 LowFuel ( < 25% ) 
# 20    1048576     0010 0000 OverHeating ( > 100% ) 
# 21    2097152     0020 0000 HasLatLong 
# 22    4194304     0040 0000 IsInDanger 
# 23    8388608     0080 0000 BeingInterdicted 
# 24    16777216    0100 0000 InMainShip 
# 25    33554432    0200 0000 InFighter 
# 26    67108864    0400 0000 InSRV 
# 27    134217728   0800 0000 HudinAnalysismode 
# 28    268435456   1000 0000 NightVision 
# 29    536870912   2000 0000 AltitudefromAverageradius 
# 30    1073741824  4000 0000 fsdJump 
# 31    2147483648  8000 0000 srvHighBeam 

# Flags2 bits: 
# Bit   value   hex         meaning 
# 0     1       0001        OnFoot 
# 1     2       0002        InTaxi (or dropship/shuttle) 
# 2     4       0004        InMulticrew (ie in someone else’s ship) 
# 3     8       0008        OnFootInStation 
# 4     16      0010        OnFootOnPlanet 
# 5     32      0020        AimDownSight 
# 6     64      0040        LowOxygen 
# 7     128     0080        LowHealth 
# 8     256     0100        Cold 
# 9     512     0200        Hot 
# 10    1024    0400        VeryCold 
# 11    2048    0800        VeryHot 
# 12    4096    1000        Glide Mode 
# 13    8192    2000        OnFootInHangar 
# 14    16384   4000        OnFootSocialSpace 
# 15    32768   8000        OnFootExterior 
# 16    65536   0001 0001   BreathableAtmosphere 

class FlagsC14():
    flag2_OnFoot = 1
    flag2_InTaxi = 2
    flag2_InMulticrew = 4
    flag2_OnFootInStation = 8
    flag2_OnFootOnPlanet = 16
    flag2_AimDownSight = 32
    flag2_LowOxygen = 64
    flag2_LowHealth = 128
    flag2_Cold = 256
    flag2_Hot = 512
    flag2_VeryCold = 1024
    flag2_VeryHot = 2048
    flag2_Glide = 4096
    flag2_OnFootInHangar = 8192
    flag2_OnFootSocialSpace = 16384
    flag2_OnFootExterior = 32768
    flag2_BreathableAtmosphere = 65536

    flag_Docked = 1
    flag_Landed = 2
    flag_LandingGearDown = 4
    flag_ShieldsUp = 8
    flag_Supercruise = 16
    flag_FlightAssist = 32
    flag_Hardpoints = 64
    flag_InWing = 128
    flag_LightsOn = 256
    flag_CargoScoopDeployed = 512
    flag_SilentRunning = 1024
    flag_ScoopingFuel = 2048
    flag_SrvHandbrake = 4096
    flag_SrvusingTurretview = 8192
    flag_SrvTurretretracted = 16384
    flag_SrvDriveAssist = 32768
    flag_FsdMassLocked = 65536
    flag_FsdCharging = 131072
    flag_FsdCooldown = 262144
    flag_LowFuel = 524288
    flag_OverHeating = 1048576
    flag_HasLatLong = 2097152
    flag_IsInDanger = 4194304
    flag_BeingInterdicted = 8388608
    flag_InMainShip = 16777216
    flag_InFighter = 33554432
    flag_InSRV = 67108864
    flag_HudinAnalysismode = 134217728
    flag_NightVision = 268435456
    flag_AltitudefromAverageradius = 536870912
    flag_fsdJump = 1073741824
    flag_srvHighBeam = 2147483648