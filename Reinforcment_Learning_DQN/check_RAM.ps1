$memoryInBytes = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory
$memoryInGB = $memoryInBytes / 1GB

Write-Host "Ilość pamięci RAM: $memoryInGB GB"
