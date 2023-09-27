# Set-ExecutionPolicy RemoteSigned
# Relative path
$directoryPath = ".\agent_output\weights"
# Remove items
Remove-Item -Path $directoryPath\* -Force -Recurse
# .\empty-saved-weights.ps1