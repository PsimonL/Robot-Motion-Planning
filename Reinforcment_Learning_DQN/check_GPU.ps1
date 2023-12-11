$gpuInfo = Get-WmiObject -Namespace "root\CIMv2" -Class Win32_VideoController | Where-Object {$_.Name -like "*NVIDIA*"}

foreach ($gpu in $gpuInfo) {
    Write-Host "Producent: $($gpu.VideoProcessor)"
    Write-Host "Model: $($gpu.Name)"
    Write-Host "Pamięć VRAM: $($gpu.AdapterRAM / 1GB) GB"
    Write-Host "Sterownik: $($gpu.DriverVersion)"
}
