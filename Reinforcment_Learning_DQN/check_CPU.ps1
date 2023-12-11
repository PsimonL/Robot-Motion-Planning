$cpuInfo = Get-WmiObject -Class Win32_Processor

foreach ($cpu in $cpuInfo) {
    Write-Host "Producent: $($cpu.Manufacturer)"
    Write-Host "Model: $($cpu.Name)"
    Write-Host "Liczba rdzeni: $($cpu.NumberOfCores)"
    Write-Host "Liczba wątków: $($cpu.NumberOfLogicalProcessors)"
    Write-Host "Taktowanie bazowe: $($cpu.MaxClockSpeed) MHz"
}
